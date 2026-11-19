import sys
import os
import asyncio
import json
import time
import socket
import ipaddress
from collections import defaultdict
from urllib.parse import urlparse

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.ollama_client import stream_reasoning, get_completion
from core.prompts import generate_verdict, generate_fixes
from core.scorer import calculate_agent_score, calculate_delphi_score
from agents.sentinel import run_sentinel
from agents.stranger import run_stranger
from agents.oracle import run_oracle

app = FastAPI(title="DELPHI Intelligence Engine", version="1.1.0")

# Configurable CORS
cors_env = os.environ.get("CORS_ORIGINS", "").strip()
allowed_origins = [o.strip() for o in cors_env.split(",") if o.strip()] if cors_env and cors_env != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SSRF Protection & Rate Limiting Configuration
BLOCKED_HOSTNAMES = {
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "::1",
    "metadata.google.internal",
    "instance-data",
}

RATE_LIMIT_WINDOW = 60
RATE_LIMIT_MAX = 10
_rate_limits: dict[str, list[float]] = defaultdict(list)

def is_rate_limited(ip: str) -> bool:
    now = time.time()
    _rate_limits[ip] = [t for t in _rate_limits[ip] if now - t < RATE_LIMIT_WINDOW]
    if len(_rate_limits[ip]) >= RATE_LIMIT_MAX:
        return True
    _rate_limits[ip].append(now)
    return False

def validate_and_sanitize_url(url: str) -> tuple[bool, str]:
    if not url or not isinstance(url, str):
        return False, "Target URL is required."
    clean_url = url.strip()
    if len(clean_url) > 2048:
        return False, "URL length exceeds maximum permitted limit."
    
    parsed = urlparse(clean_url)
    if parsed.scheme.lower() not in ("http", "https"):
        return False, f"Unsupported scheme '{parsed.scheme}'. Only http and https URLs are allowed."
    
    hostname = parsed.hostname
    if not hostname:
        return False, "Could not determine hostname from URL."
    
    if hostname.lower() in BLOCKED_HOSTNAMES or hostname.lower().endswith(".local") or hostname.lower().endswith(".internal"):
        return False, f"Access to internal/loopback hostname '{hostname}' is prohibited (SSRF protection)."
    
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False, f"Unable to resolve host '{hostname}'."
    except Exception as e:
        return False, f"DNS resolution failed: {e}"
    
    for entry in addr_info:
        ip_str = entry[4][0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError:
            return False, f"Invalid resolved IP '{ip_str}'."
        
        if (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_reserved
            or ip_obj.is_multicast
            or ip_obj.is_unspecified
        ):
            return False, f"Target resolves to private/internal IP address ({ip_str}), blocked by SSRF policy."
    
    return True, clean_url

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, agent: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[agent] = websocket

    def disconnect(self, agent: str):
        if agent in self.active_connections:
            del self.active_connections[agent]

    async def broadcast(self, message: dict):
        for ws in list(self.active_connections.values()):
            try:
                await ws.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

class AnalyzePayload(BaseModel):
    url: str

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "DELPHI Security Intelligence Engine",
        "active_websockets": list(manager.active_connections.keys()),
    }

@app.post("/api/analyze")
async def start_analysis(payload: AnalyzePayload, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    if is_rate_limited(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded: maximum 10 analysis requests per minute per IP."
        )

    valid, result = validate_and_sanitize_url(payload.url)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Security Policy Rejection: {result}"
        )

    sanitized_url = result

    # Capture connections immediately
    ws_sentinel = manager.active_connections.get("sentinel")
    ws_stranger = manager.active_connections.get("stranger")
    ws_oracle = manager.active_connections.get("oracle")

    # Run agents asynchronously with direct references
    asyncio.create_task(run_all_agents(sanitized_url, ws_sentinel, ws_stranger, ws_oracle))
    return {"status": "Analysis started", "target": sanitized_url}

async def run_all_agents(url: str, ws_sentinel, ws_stranger, ws_oracle):
    print(f"Sentinel WS: {ws_sentinel}")
    print(f"Stranger WS: {ws_stranger}")
    print(f"Oracle WS: {ws_oracle}")

    if not ws_sentinel or not ws_stranger or not ws_oracle:
        print("ERROR: One or more WebSocket connections missing!")
        return

    t1 = asyncio.create_task(run_sentinel(url, ws_sentinel))
    t2 = asyncio.create_task(run_stranger(url, ws_stranger))
    t3 = asyncio.create_task(run_oracle(url, ws_oracle))

    # Collect results from agents with timeout (45s)
    try:
        results = await asyncio.wait_for(asyncio.gather(t1, t2, t3, return_exceptions=True), timeout=45.0)
    except asyncio.TimeoutError:
        print("Analysis timed out after 45 seconds")
        results = [[], [], []]
    
    # Extract findings from results - ensuring they are lists
    sentinel_findings = results[0] if isinstance(results[0], list) else []
    stranger_findings = results[1] if isinstance(results[1], list) else []
    oracle_findings = results[2] if isinstance(results[2], list) else []
    
    # Calculate scores
    sentinel_score = calculate_agent_score(sentinel_findings)
    stranger_score = calculate_agent_score(stranger_findings)
    oracle_score = calculate_agent_score(oracle_findings)
    
    all_findings = []
    all_findings.extend(sentinel_findings)
    all_findings.extend(stranger_findings)
    all_findings.extend(oracle_findings)
    top_finding_texts = [f['text'] for f in all_findings if f.get('severity') in ['CRITICAL', 'HIGH']]
    
    # Generate the text summary via LLM
    verdict_prompt = generate_verdict(sentinel_score, stranger_score, oracle_score, top_finding_texts)
    summary_text = await get_completion(verdict_prompt)
    
    # Generate fixes via LLM
    fixes_prompt = generate_fixes(all_findings)
    fixes_json_str = await get_completion(fixes_prompt)
    
    try:
        # Clean up possible markdown or whitespace
        clean_json = fixes_json_str.strip()
        if "```" in clean_json:
            clean_json = clean_json.split("```")[1]
            if clean_json.startswith("json"):
                clean_json = clean_json[4:]
        fixes = json.loads(clean_json)
    except Exception as e:
        print(f"Failed to parse fixes JSON: {e}")
        fixes = [] # Fallback
    
    final_message = {
        "agent": "system",
        "type": "judgment",
        "content": {
            "sentence": summary_text,
            "overallScore": calculate_delphi_score(sentinel_score, stranger_score, oracle_score),
            "survivalProbability": calculate_delphi_score(sentinel_score, stranger_score, oracle_score) - 10,
            "scores": {
                "sentinel": sentinel_score,
                "stranger": stranger_score,
                "oracle": oracle_score
            },
            "fixes": fixes
        }
    }
    
    await manager.broadcast(final_message)

@app.websocket("/ws/sentinel")
async def websocket_sentinel(websocket: WebSocket):
    await websocket_endpoint(websocket, "sentinel")

@app.websocket("/ws/stranger")
async def websocket_stranger(websocket: WebSocket):
    await websocket_endpoint(websocket, "stranger")

@app.websocket("/ws/oracle")
async def websocket_oracle(websocket: WebSocket):
    await websocket_endpoint(websocket, "oracle")

async def websocket_endpoint(websocket: WebSocket, agent_name: str):
    await manager.connect(agent_name, websocket)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(agent_name)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False, loop="asyncio")

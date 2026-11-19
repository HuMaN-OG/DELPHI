import asyncio
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
        return None

async def stream_reasoning(prompt: str, websocket, agent: str):
    loop = asyncio.get_event_loop()
    client = get_groq_client()

    if not client:
        fallback_words = ["Reasoning", "provider", "offline:", "GROQ_API_KEY", "not", "configured."]
        for word in fallback_words:
            message = json.dumps({
                "agent": agent,
                "type": "reasoning",
                "content": {
                    "text": word + " ",
                    "severity": "LOW",
                    "category": "reasoning",
                    "value": 0
                }
            })
            await websocket.send_text(message)
            await asyncio.sleep(0.05)
        return

    def call_groq():
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM error: {e}"

    full_text = await loop.run_in_executor(None, call_groq)

    words = full_text.split()
    for word in words:
        message = json.dumps({
            "agent": agent,
            "type": "reasoning",
            "content": {
                "text": word + " ",
                "severity": "LOW",
                "category": "reasoning",
                "value": 0
            }
        })
        await websocket.send_text(message)
        await asyncio.sleep(0.05)

async def get_completion(prompt: str):
    loop = asyncio.get_event_loop()
    client = get_groq_client()
    if not client:
        return "Analysis verdict generated via heuristic rule-set. To enable deep LLM reasoning summaries, provide a valid GROQ_API_KEY in the environment."

    def call_groq():
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Heuristic evaluation completed. LLM synthesis unavailable: {e}"

    return await loop.run_in_executor(None, call_groq)
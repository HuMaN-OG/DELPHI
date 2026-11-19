import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app, validate_and_sanitize_url, is_rate_limited, _rate_limits

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "active_websockets" in data

def test_ssrf_rejects_localhost_and_private_ips():
    bad_urls = [
        "http://localhost:8000",
        "http://127.0.0.1/admin",
        "http://0.0.0.0:80",
        "http://169.254.169.254/latest/meta-data",
        "http://10.0.0.1",
        "http://192.168.1.1",
        "http://172.16.0.1",
        "ftp://example.com/test",
        "file:///etc/passwd",
        "gopher://127.0.0.1:6379",
    ]
    for url in bad_urls:
        valid, msg = validate_and_sanitize_url(url)
        assert not valid, f"Expected {url} to be rejected, but it was accepted: {msg}"
        res = client.post("/api/analyze", json={"url": url})
        assert res.status_code == 400, f"Expected 400 for {url}, got {res.status_code}"

def test_ssrf_accepts_valid_public_url():
    valid, sanitized = validate_and_sanitize_url("https://example.com")
    assert valid
    assert sanitized == "https://example.com"

def test_rate_limiting():
    _rate_limits.clear()
    test_ip = "198.51.100.99"
    # Should allow up to 10 requests
    for i in range(10):
        assert not is_rate_limited(test_ip)
    # 11th request must be rate limited
    assert is_rate_limited(test_ip)

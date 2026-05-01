"""
rate_limiter.py — In-memory rate limiter to protect AI endpoints from abuse.
"""
from fastapi import Request, HTTPException
import time
from collections import defaultdict

# IP -> list of request timestamps
_request_history = defaultdict(list)

# Max 20 requests per minute per IP for AI endpoints
MAX_REQUESTS = 20
WINDOW_SECONDS = 60

async def ai_rate_limiter(request: Request):
    """Dependency to limit AI endpoint usage."""
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    
    # Clean up old requests
    history = _request_history[client_ip]
    history = [t for t in history if now - t < WINDOW_SECONDS]
    
    if len(history) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded for AI features. Please try again in a minute."
        )
    
    history.append(now)
    _request_history[client_ip] = history

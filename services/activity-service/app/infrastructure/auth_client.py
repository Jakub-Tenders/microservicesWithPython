# Module 6 — used when the gateway requires a JWT on every request.
#
# activity-service calls user-service internally (to validate users).
# Once the gateway validates tokens on all requests, those internal calls
# also need a valid token — but they are not acting on behalf of any user.
# This is the Machine-to-Machine (M2M) flow: the service authenticates as itself.
#
# Before this file will work you need to add two settings to your config.py:
#
#   auth_service_url: str = "http://localhost:8005"
#   m2m_secret: str = "m2m-secret"
#
# The password must match the one in auth-service/app/users.py for "activity-service".

import httpx

from app.config import settings

# Simple in-memory token cache.
# In production you would inspect the "exp" claim and refresh before expiry.
# For this course, reusing the token until the process restarts is fine.
_token_cache: str | None = None


async def get_m2m_token() -> str:
    """
    Fetch a service-to-service JWT from auth-service.

    activity-service authenticates with hardcoded client credentials
    (username="activity-service", password=settings.m2m_secret) and receives
    a token with role="service".

    This token is then attached to outbound calls so the gateway lets them through.

    Note: this call goes directly to auth-service (port 8005), not through the gateway.
    M2M token exchange is internal — it must not require a token to get a token.
    """
    global _token_cache
    if _token_cache:
        return _token_cache

    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.post(
            f"{settings.auth_service_url}/v1/auth/token",
            data={"username": "activity-service", "password": settings.m2m_secret},
        )
        resp.raise_for_status()
        _token_cache = resp.json()["access_token"]
        return _token_cache


async def get_auth_headers() -> dict[str, str]:
    """
    Convenience wrapper — returns headers ready to pass to an httpx request.

    Usage:
        headers = await get_auth_headers()
        resp = await client.get(url, headers=headers)
    """
    token = await get_m2m_token()
    return {"Authorization": f"Bearer {token}"}

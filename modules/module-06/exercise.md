# Module 6 Exercise — Security

> This module adds Keycloak infrastructure:
> ```bash
> docker compose -f docker-compose.infra.yml up -d keycloak
> ```

## Keycloak Setup
Keycloak is pre-configured by `infra/keycloak/realm-export.json`.

### Test credentials
- User: `testuser` / `password`
- Admin: `admin` / `admin`

## Part A: Get a token

```bash
# Resource Owner Password Credentials (testing only — not for production)
curl -X POST http://localhost:8080/realms/gamehub/protocol/openid-connect/token \
  -d "client_id=gamehub-client" \
  -d "client_secret=change_me_in_prod" \
  -d "grant_type=password" \
  -d "username=testuser" \
  -d "password=password" \
  -d "scope=openid"
```

Decode the JWT at https://jwt.io and identify:
- `sub` — user ID
- `realm_access.roles` — assigned roles
- `exp` — expiry

## Part B: Add JWT middleware to user-service

Create `services/user-service/app/security.py`:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import httpx
from app.config import settings

bearer_scheme = HTTPBearer()


async def get_keycloak_public_key() -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.keycloak_url}/realms/{settings.keycloak_realm}"
        )
        return resp.json()["public_key"]


async def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    token = credentials.credentials
    try:
        public_key = await get_keycloak_public_key()
        pem_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
        payload = jwt.decode(
            token, pem_key, algorithms=[settings.jwt_algorithm],
            options={"verify_aud": False}
        )
        return payload
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


def require_role(role: str):
    async def checker(claims: dict = Depends(require_auth)) -> dict:
        roles = claims.get("realm_access", {}).get("roles", [])
        if role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Role '{role}' required")
        return claims
    return checker
```

Protect the DELETE endpoint:
```python
@app.delete("/v1/users/{user_id}", dependencies=[Depends(require_role("admin"))])
async def delete_user(...):
    ...
```

## Part C: Machine-to-Machine auth (Client Credentials)

```bash
curl -X POST http://localhost:8080/realms/gamehub/protocol/openid-connect/token \
  -d "client_id=gamehub-m2m" \
  -d "client_secret=m2m_secret_change_me" \
  -d "grant_type=client_credentials"
```

Use this token in activity-service when calling user-service internally.

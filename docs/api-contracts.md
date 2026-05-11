# API Contracts

This document is the source of truth for every endpoint the GameHub frontend consumes.

Students must match these shapes exactly — field names, types, and nesting included.
The frontend will break visibly if a shape is wrong, which is intentional.

> This document may be updated as the frontend evolves. Check git history for changes.

---

## Conventions

- All endpoints are prefixed with `/v1/`
- Dates are ISO 8601 strings: `"2025-03-01T10:00:00Z"`
- IDs are UUIDs: `"3fa85f64-5717-4562-b3fc-2c963f66afa6"`
- List endpoints return a paginated envelope (never a bare array)
- HTTP errors return `{ "detail": "<message>" }`

## Entry point

From Module 3 onward, **all client requests go through the gateway on port 8000**.
Never call a service port directly from client code.

```
http://localhost:8000/v1/users      → user-service
http://localhost:8000/v1/games      → game-service
http://localhost:8000/v1/activities → activity-service
http://localhost:8000/v1/auth/token → auth-service
http://localhost:8000/v1/consent/.. → logging-service
http://localhost:8000/v1/logs/..    → logging-service
```

The port numbers listed per service below are for reference and local debugging only.

---

## user-service — port 8001

### POST /v1/users
Create a new user.

**Request:**
```json
{
  "username": "nova",
  "email": "nova@example.com",
  "password": "secret"
}
```

**Response 201:**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "username": "nova",
  "email": "nova@example.com",
  "is_active": true,
  "created_at": "2025-03-01T10:00:00Z"
}
```

---

### GET /v1/users
List all users.

**Query params:** `limit` (default 20), `offset` (default 0)

**Response 200:**
```json
{
  "items": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "username": "nova",
      "email": "nova@example.com",
      "is_active": true,
      "created_at": "2025-03-01T10:00:00Z"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

---

### GET /v1/users/{user_id}
Get a single user.

**Response 200:** same shape as a single item above.
**Response 404:** `{ "detail": "User not found" }`

---

## game-service — port 8002

### POST /v1/games
Add a game to the catalogue.

**Request:**
```json
{
  "title": "Hollow Knight",
  "genre": "metroidvania",
  "platform": "PC",
  "release_year": 2017,
  "cover_url": "https://example.com/cover.jpg"
}
```

**Response 201:**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Hollow Knight",
  "genre": "metroidvania",
  "platform": "PC",
  "release_year": 2017,
  "cover_url": "https://example.com/cover.jpg",
  "created_at": "2025-03-01T10:00:00Z"
}
```

---

### GET /v1/games
List all games.

**Query params:** `limit` (default 20), `offset` (default 0)

**Response 200:**
```json
{
  "items": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "title": "Hollow Knight",
      "genre": "metroidvania",
      "platform": "PC",
      "release_year": 2017,
      "cover_url": "https://example.com/cover.jpg",
      "created_at": "2025-03-01T10:00:00Z"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

---

### GET /v1/games/{game_id}
Get a single game.

**Response 200:** same shape as a single item above.
**Response 404:** `{ "detail": "Game not found" }`

---

### GET /v1/games/search
Search games by title.

**Query params:** `q` (required)

**Response 200:** same envelope shape as `GET /v1/games`

---

### GET /v1/games/{game_id}/summary
Fast read from Redis cache. Returns a lighter shape.

**Response 200:**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Hollow Knight",
  "genre": "metroidvania",
  "platform": "PC"
}
```

---

## activity-service — port 8003

### POST /v1/activities
Log a user activity.

**Request:**
```json
{
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "game_id": "4fa85f64-5717-4562-b3fc-2c963f66afa6",
  "action": "played",
  "duration_minutes": 90
}
```

Valid `action` values: `"played"`, `"completed"`, `"reviewed"`, `"wishlist_added"`

**Response 201:**
```json
{
  "id": "5fa85f64-5717-4562-b3fc-2c963f66afa6",
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "action": "played",
  "duration_minutes": 90,
  "created_at": "2025-03-01T10:00:00Z",
  "game": {
    "id": "4fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Hollow Knight",
    "genre": "metroidvania",
    "platform": "PC",
    "cover_url": "https://example.com/cover.jpg"
  }
}
```

> activity-service fetches game data from game-service via httpx at request time.
> If game-service is unreachable, return the activity with `"game": null` — do not fail the request.

---

### GET /v1/activities
List all recent activities (global feed).

**Query params:** `limit` (default 20), `offset` (default 0)

**Response 200:**
```json
{
  "items": [
    {
      "id": "5fa85f64-5717-4562-b3fc-2c963f66afa6",
      "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "action": "played",
      "duration_minutes": 90,
      "created_at": "2025-03-01T10:00:00Z",
      "game": {
        "id": "4fa85f64-5717-4562-b3fc-2c963f66afa6",
        "title": "Hollow Knight",
        "genre": "metroidvania",
        "platform": "PC",
        "cover_url": "https://example.com/cover.jpg"
      }
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

---

### GET /v1/activities/user/{user_id}
Get activity feed for a specific user.

**Response 200:** same envelope shape as above.

---

## notification-service — port 8004 (Node.js + SQLite)

### GET /v1/notifications/{user_id}
List notifications for a user.

**Query params:** `limit` (default 20), `offset` (default 0)

**Response 200:**
```json
{
  "items": [
    {
      "id": "6fa85f64-5717-4562-b3fc-2c963f66afa6",
      "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "type": "activity_notification",
      "message": "nova just played Hollow Knight",
      "read": false,
      "created_at": "2025-03-01T10:00:00Z"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

---

### PATCH /v1/notifications/{notification_id}/read
Mark a notification as read.

**Response 200:**
```json
{
  "id": "6fa85f64-5717-4562-b3fc-2c963f66afa6",
  "read": true
}
```

---

## logging-service — port 8006

### POST /v1/consent/{user_id}
Record a user's GDPR consent decision.

**Request:**
```json
{
  "granted": true
}
```

**Response 200:**
```json
{
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "granted": true,
  "updated_at": "2025-03-01T10:00:00Z"
}
```

---

### GET /v1/consent/{user_id}
Check a user's current consent status.

**Response 200:**
```json
{
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "granted": true,
  "updated_at": "2025-03-01T10:00:00Z"
}
```

**Response 404:** `{ "detail": "No consent record found" }` — treat as not granted.

---

### DELETE /v1/consent/{user_id}
Withdraw consent (sets `granted: false`).

**Response 200:**
```json
{
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "granted": false,
  "updated_at": "2025-03-01T10:00:00Z"
}
```

---

### DELETE /v1/logs/{user_id}
GDPR right to erasure — permanently delete all log entries for a user.

**Response 200:**
```json
{
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "deleted_entries": 42
}
```

---

## auth-service — port 8005

### POST /v1/auth/token
Obtain a JWT access token (OAuth2 password flow).

**Request** (form-encoded, not JSON):
```
username=testuser&password=password
```

**Response 200:**
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

**Response 401:** `{ "detail": "Incorrect username or password" }`

---

### GET /v1/auth/me
Return the payload of the current token. Used to verify auth is working.

**Headers:** `Authorization: Bearer <token>`

**Response 200:**
```json
{
  "sub": "testuser",
  "role": "gamer",
  "exp": 1234567890
}
```

**Response 401:** `{ "detail": "Invalid token" }`

---

## Health endpoints

Every service exposes `GET /health` directly on its own port. The gateway also exposes `GET /health` on port 8000 — this is the endpoint the frontend uses.

The gateway `/health` response evolves across modules:

**Module 3–9** — gateway status only:
```
GET http://localhost:8000/health
```
```json
{
  "status": "ok",
  "service": "gateway"
}
```

**Module 10** — aggregate: gateway calls each downstream service and returns combined status:
```
GET http://localhost:8000/health
```
```json
{
  "status": "ok",
  "service": "gateway",
  "services": {
    "users": "ok",
    "games": "ok",
    "activities": "ok",
    "notifications": "ok",
    "auth": "ok",
    "logging": "ok"
  }
}
```

Each service's own health shape (for direct/ops access):

### GET /health — individual service
**Response 200:**
```json
{
  "status": "ok",
  "service": "user-service"
}
```

The frontend calls `GET http://localhost:8000/health` only — it never contacts service ports directly. The per-service status panel is powered by the Module 10 aggregate response.

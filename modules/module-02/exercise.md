# Module 2 Exercise — FastAPI Service Design

## What you'll build
A fully layered FastAPI service following DDD structure:
- Domain layer: SQLAlchemy models
- Application layer: Pydantic schemas + service class
- Infrastructure layer: async database + repository

## Steps

### Step 1: Run user-service locally (no Docker)
```bash
cp .env.example .env
cd services/user-service
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

The service uses SQLite by default — no database server needed. A `user_service.db` file will be created automatically.

### Step 2: Explore the auto-generated API docs
Open http://localhost:8001/docs

Try:
- POST /v1/users — create a user
- GET /v1/users — list users
- GET /v1/users/{id} — get by ID

### Step 3: Run Alembic migrations
```bash
# Auto-generate from models
alembic revision --autogenerate -m "create users table"
alembic upgrade head
```

### Step 4: Run tests
```bash
pytest tests/ -v
```

### Step 5: Build the game-service
Create `services/game-service/` following the same structure as user-service.

Implement:
- `POST /v1/games` — add a game to the catalogue
- `GET /v1/games` — list games
- `GET /v1/games/{id}` — get by ID
- `GET /v1/games/search?q=<term>` — search by name

**Hint:** Use SQLAlchemy `ilike` for the search endpoint.

Run it on port 8002:
```bash
cd services/game-service
uvicorn app.main:app --reload --port 8002
```

## Verification
Both services should be running locally and responding:
```bash
curl http://localhost:8001/v1/users
curl http://localhost:8002/v1/games
```

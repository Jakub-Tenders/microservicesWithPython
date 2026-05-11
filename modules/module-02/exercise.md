# Module 2 — FastAPI Service Design

**Duration**: 2h in class
**Branch to submit**: `module-02/<team-name>`

---

## Objective

You will build two services: explore the fully-built `user-service` as a reference, then build `game-service` yourself using the same structure. By the end of this module, both services run locally and respond to requests.

The architecture follows Domain-Driven Design (DDD) with three layers:
- **Domain** — SQLAlchemy models (what the data looks like in the database)
- **Application** — Pydantic schemas + service class (what the API sends and receives)
- **Infrastructure** — repository + database session (how data is read and written)

---

## What's provided

`user-service` is fully implemented and documented. Read it before building anything — every file has comments explaining which DDD layer it belongs to and why.

Start it with:
```bash
cd services/user-service
cp .env.example .env
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8001
```

Open http://localhost:8001/docs and try the endpoints before writing any code.

---

## What you need to build

### game-service

Create `services/game-service/` following the exact same structure as `user-service`.

Your service must expose these four endpoints:

| Method | Path | Description |
|---|---|---|
| POST | `/v1/games` | Add a game to the catalogue |
| GET | `/v1/games` | List all games |
| GET | `/v1/games/{id}` | Get a game by ID |
| GET | `/v1/games/search?q=<term>` | Search games by name |

**A `Game` has at minimum**: `id`, `title`, `genre`, `platform`, `cover_url`.

For the search endpoint, use SQLAlchemy's `ilike` operator — it does a case-insensitive partial match.

Run it on port 8002:
```bash
cd services/game-service
uvicorn app.main:app --reload --port 8002
```

---

## Verify both services are running

```bash
curl http://localhost:8001/v1/users
curl http://localhost:8002/v1/games
```

Both should return a valid JSON response (empty list is fine).

Run the tests:
```bash
cd services/user-service && pytest tests/ -v
cd services/game-service && pytest tests/ -v
```

---

## Minimum to submit this branch

- [ ] `game-service` running on port 8002 with all 4 endpoints working
- [ ] Alembic migration for the `games` table committed
- [ ] At least one test passing in `game-service/tests/`
- [ ] `REFLECTION.md` completed and committed

If you run out of time: the search endpoint is optional. The other three are not.

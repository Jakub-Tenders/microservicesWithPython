# Module 5 — Data Management & CQRS

**Duration**: 2h in class
**Branch to submit**: `module-05/<team-name>`

---

## Objective

Not all data is the same. Some data needs to be written once and read accurately (a user's account). Other data needs to be read thousands of times per second and can tolerate being slightly stale (a game's summary).

This module introduces two ideas: **CQRS** (separating read and write models) and the **GDPR consent lifecycle** (which forces you to think about what you are even allowed to store).

Redis is already running in the infrastructure container.

---

## What's provided

- The `game-service` CQRS scaffolding is in place: SQLite is the write model, Redis is the read model. The cache write logic is implemented — you wire up the read side.
- The `logging-service` skeleton is provided (Flask, not FastAPI — intentional). The Kafka consumer is scaffolded. You implement the consent endpoints.
- `logging-service` uses Flask: routes are `@app.route(...)`, no Pydantic, run with `flask run --port 8006`.

---

## Part A — CQRS in game-service *(~40 min)*

When a game is added, it writes to two places:
- **SQLite** — the authoritative write model
- **Redis** — a denormalised projection for fast reads

Two endpoints serve the same game differently:
- `GET /v1/games/{id}` — reads from SQLite (full, accurate data)
- `GET /v1/games/{id}/summary` — reads from Redis (fast, potentially stale)

Your task: wire up the `/summary` endpoint to read from Redis. The cache key format and the write side are already implemented — find them in `game-service/app/infrastructure/cache.py` and follow the same pattern.

Test the difference by adding a game, then calling both endpoints. Confirm the summary comes back faster (or at all) when SQLite is bypassed.

---

## Part B — GDPR consent lifecycle in logging-service *(~45 min)*

The `logging-service` consumes Kafka events from `activity-service`. Before writing any log entry, it must check that the user has given consent.

Implement the four consent endpoints in `logging-service/app/main.py`:

| Method | Path | Description |
|---|---|---|
| POST | `/v1/consent/{user_id}` | User opts in to activity logging |
| GET | `/v1/consent/{user_id}` | Check consent status |
| DELETE | `/v1/consent/{user_id}` | User withdraws consent |
| DELETE | `/v1/logs/{user_id}` | GDPR right to erasure — delete all logs for this user |

The Kafka consumer already calls `has_consent(user_id)` before writing — implement that function in the consent model.

Register `logging-service` in the gateway (port 8006). It needs two route entries — one for `consent`, one for `logs` — both pointing to the same service:

```python
# gateway/app/config.py
logging_service_url: str = "http://localhost:8006"

# gateway/app/main.py ROUTES
"consent": settings.logging_service_url,
"logs":    settings.logging_service_url,
```

Test the full flow:
1. Log an activity — confirm no log is written (no consent yet)
2. `POST /v1/consent/{user_id}` — opt in
3. Log another activity — confirm the log appears
4. `DELETE /v1/consent/{user_id}` — withdraw consent
5. `DELETE /v1/logs/{user_id}` — erase all logs for that user

---

## Discussion *(~15 min)*

- You now have two models for a game's data. What happens if a game's title is updated in SQLite but the Redis projection is not refreshed? Who notices first — the developer or the user?
- The GDPR consent check is inside `logging-service`, not at the gateway. Why there and not earlier in the chain?
- What is the difference between CQRS and Event Sourcing? (No implementation needed — just the concept.)

---

## Minimum to submit this branch

- [ ] `GET /v1/games/{id}/summary` returns data from Redis
- [ ] All four consent endpoints working and reachable via the gateway
- [ ] Kafka consumer skips log entries when consent is not given
- [ ] `logging-service` registered in the gateway under both `consent` and `logs`
- [ ] `REFLECTION.md` completed and committed

---

## Optional — Event Sourcing

If you finish early, explore the `game_events` table scaffolded in `game-service/app/models.py`. Try implementing `replay_game_state(game_id)` — it reconstructs the current state of a game by replaying all events rather than reading the current row. This is the core idea behind Event Sourcing.

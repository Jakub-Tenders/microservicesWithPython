# Module 5 Exercise — Data Management & CQRS

> This module adds Redis infrastructure. Start it alongside messaging:
> ```bash
> docker compose -f docker-compose.infra.yml up -d redis
> ```

## CQRS in game-service

The game-service implements the CQRS pattern:
- **Write side**: SQLite via SQLAlchemy (commands: add game, update game info)
- **Read side**: Redis projections (queries: game details, search results)

### Task 1: Verify the pattern
1. Add a game → it writes to SQLite AND Redis
2. `GET /v1/games/{id}/summary` — served from Redis (fast, denormalized)
3. `GET /v1/games/{id}` — served from SQLite (authoritative, full data)

Benchmark the difference:
```bash
# Install hey (HTTP load tool)
# Read model (Redis)
hey -n 1000 -c 50 http://localhost:8002/v1/games/{id}/summary

# Write model (SQLite)
hey -n 1000 -c 50 http://localhost:8002/v1/games/{id}
```

### Task 2: Event Sourcing exploration
Instead of storing the current state, store events as the source of truth.

Add a `game_events` table:
```python
class GameEvent(Base):
    __tablename__ = "game_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    game_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[str] = mapped_column(Text)  # JSON
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

Implement `replay_game_state(game_id)` that reconstructs game state from events.

### Task 3: Logging-service GDPR consent flow
Implement the full consent lifecycle in logging-service:

1. `POST /v1/consent/{user_id}` — user opts in to activity logging
2. `GET /v1/consent/{user_id}` — check consent status
3. `DELETE /v1/consent/{user_id}` — user withdraws consent
4. `DELETE /v1/logs/{user_id}` — GDPR right to erasure (delete all logs for user)

The Kafka consumer in logging-service must check consent before writing any log entry.

### Task 4: Kafka as event log
Add a Kafka consumer in game-service that reads `activity.logged` events and
rebuilds a separate analytics projection (e.g., most-played games in Redis).

## Discussion
- What is the difference between CQRS and Event Sourcing?
- When does eventual consistency become a problem for the user experience?
- How would you handle schema evolution in Kafka events?

# Module 10 Exercise — Resilience, Performance & CI/CD

## Part A: Circuit Breaker

### Part A.1 — Circuit breaker inside activity-service

Add a circuit breaker to the activity-service → logging-service call.

Create `services/activity-service/app/infrastructure/circuit_breaker.py`:
```python
import asyncio
import time
from enum import Enum
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog

log = structlog.get_logger()


class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing — reject calls immediately
    HALF_OPEN = "half_open"  # Testing recovery


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.last_failure_time: float | None = None
        self.recovery_timeout = recovery_timeout

    def _should_attempt(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                log.info("circuit breaker: half-open — testing recovery")
                return True
            return False
        return True  # HALF_OPEN: allow one attempt

    def record_success(self) -> None:
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        log.info("circuit breaker: closed (recovered)")

    def record_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.monotonic()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            log.warning("circuit breaker: open", failures=self.failure_count)

    async def call(self, coro):
        if not self._should_attempt():
            raise Exception("Circuit breaker OPEN — logging-service unavailable")
        try:
            result = await coro
            self.record_success()
            return result
        except Exception as e:
            self.record_failure()
            raise


logging_circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=30.0)
```

### Test it
```bash
# Get a token first
TOKEN=$(curl -s -X POST http://localhost:8000/v1/auth/token -d "username=testuser&password=password" | jq -r .access_token)

# Stop logging-service
docker compose stop logging-service

# Log 5+ activities through the gateway — watch circuit open
for i in $(seq 1 6); do
  curl -X POST http://localhost:8000/v1/activities \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"user_id": "u1", "game_id": "g1", "action": "played"}'
done

# Restart logging-service — circuit should recover
docker compose start logging-service
```

### Part A.2 — Circuit breaker at the gateway

The gateway makes one outbound call per request. If a downstream service is degraded,
every client request hitting that route will hang until timeout — cascading the failure upward.

Add a per-service circuit breaker to `gateway/app/main.py`.

The gateway is a separate project — it cannot import from `activity-service`.
Implement the same `CircuitBreaker` class in `gateway/app/circuit_breaker.py`
(same logic, same interface, different file).

Each service gets its own instance:

```python
breakers = {
    "users": CircuitBreaker(failure_threshold=5, recovery_timeout=30.0),
    "games": CircuitBreaker(failure_threshold=5, recovery_timeout=30.0),
    "activities": CircuitBreaker(failure_threshold=5, recovery_timeout=30.0),
    # ...
}
```

In the proxy route, wrap the `httpx` call with the relevant breaker before forwarding.
When the circuit is OPEN, return `503 Service Unavailable` immediately — no network call made.

### Test it

```bash
# Get a token first — gateway requires JWT
TOKEN=$(curl -s -X POST http://localhost:8000/v1/auth/token -d "username=testuser&password=password" | jq -r .access_token)

# Stop game-service
docker compose stop game-service

# Send 5+ requests — watch the circuit open
for i in $(seq 1 6); do
  curl http://localhost:8000/v1/games -H "Authorization: Bearer $TOKEN"
done

# Requests to other services still work — isolation is key
curl http://localhost:8000/v1/users -H "Authorization: Bearer $TOKEN"

# Restart game-service — circuit recovers after 30s
docker compose start game-service
```

### Discussion

- Part A.1 protects a service from its own dependency. Part A.2 protects clients from a failing service. Why do you need both?
- Why does each service get its own circuit breaker instance rather than one shared breaker?
- What should the gateway return in the response body when the circuit is OPEN?

---

## Part A.3 — Aggregate health endpoint on the gateway

The gateway has served `GET /health` since Module 3, returning only its own status.
Now that every service has a circuit breaker, upgrade it to report the real state of the system.

In `gateway/app/main.py`, replace the simple health route with one that fans out to all services concurrently:

```python
@app.get("/health")
async def health():
    results = {}
    async with httpx.AsyncClient(timeout=2.0) as client:
        for name, url in settings_urls.items():
            try:
                resp = await client.get(f"{url}/health")
                results[name] = "ok" if resp.status_code == 200 else "degraded"
            except Exception:
                results[name] = "unreachable"
    overall = "ok" if all(v == "ok" for v in results.values()) else "degraded"
    return {"status": overall, "service": "gateway", "services": results}
```

Where `settings_urls` is a dict of `{ resource_name: base_url }` built from your `Settings`.

The response matches the contract in `docs/api-contracts.md`:
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

### Test it
```bash
# All services running
curl http://localhost:8000/health

# Stop one service and check again
docker compose stop game-service
curl http://localhost:8000/health
# → "games": "unreachable", "status": "degraded"
```

The frontend's status panel reads this single endpoint. No service port is ever exposed to the client.

---

## Part B: Redis Caching

Game-service already uses cache-aside. Add cache warming on startup:

```python
async def warm_cache() -> None:
    """Pre-populate cache with top 100 games on startup."""
    async with AsyncSessionFactory() as session:
        repo = GameRepository(session)
        games, _ = await repo.list(limit=100)
    async with Redis.from_url(settings.redis_url) as redis:
        cache = GameCache(redis)
        for game in games:
            response = GameResponse.model_validate(game)
            await cache.set(game.id, response.model_dump())
    log.info("cache warmed", count=len(games))
```

---

> **CI/CD and load testing (GitHub Actions + Locust) are covered in Lesson 13.**
> That lesson is a flex session: it runs as a full lesson if the course is on pace,
> or absorbs overflow time if not. No content is lost either way.

# Module 10 Exercise — Resilience, Performance & CI/CD

## Part A: Circuit Breaker

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
# Stop logging-service
docker compose stop logging-service

# Log 5+ activities — watch circuit open
for i in $(seq 1 6); do
  curl -X POST http://localhost:8003/v1/activities -H "Content-Type: application/json" \
    -d '{"user_id": "u1", "game_id": "g1", "action": "played"}'
done

# Restart logging-service — circuit should recover
docker compose start logging-service
```

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

## Part C: GitHub Actions CI/CD

The pipeline at `.github/workflows/user-service.yml` runs on every push to `services/user-service/**`.

### Steps in the pipeline
1. **lint** — ruff + mypy
2. **test** — pytest with Testcontainers
3. **build** — docker build + push to GHCR
4. **deploy** — helm upgrade on minikube (or k3d in CI)

### Required GitHub Secrets
- `GHCR_TOKEN` — GitHub Container Registry token
- `KUBE_CONFIG` — base64-encoded kubeconfig

### Trigger a pipeline run
```bash
git add services/user-service/app/main.py
git commit -m "feat: add /health/ready endpoint"
git push origin main
```

Watch the pipeline at: GitHub → Actions → "user-service CI/CD"

## Part D: Load Testing with Locust

```bash
pip install locust
locust -f locustfile.py --host=http://localhost --users=100 --spawn-rate=10
```

Create `locustfile.py`:
```python
from locust import HttpUser, task, between

class GameHubUser(HttpUser):
    wait_time = between(0.5, 2)

    @task(3)
    def list_games(self):
        self.client.get("/api/games")

    @task(1)
    def log_activity(self):
        self.client.post("/api/activities", json={
            "user_id": "test-user-id",
            "game_id": "test-game-id",
            "action": "played",
        })
```

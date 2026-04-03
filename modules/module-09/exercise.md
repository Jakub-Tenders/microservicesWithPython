# Module 9 Exercise — Observability

## Services are already instrumented with OpenTelemetry.
The `app/observability.py` in each service sets up:
- Traces → Jaeger (OTLP gRPC)
- Metrics → Prometheus (via prometheus-fastapi-instrumentator)
- Logs → stdout (picked up by Promtail → Loki)

## Part A: Metrics with Prometheus + Grafana

1. Start the full stack:
```bash
docker compose -f docker-compose.infra.yml \
               -f modules/module-09/docker-compose.override.yml up --build
```

2. Generate some traffic:
```bash
# Install hey
# macOS: brew install hey
# Linux: wget https://hey-release.s3.us-east-2.amazonaws.com/hey_linux_amd64

hey -n 200 -c 10 http://localhost/api/users
hey -n 200 -c 10 http://localhost/api/games
```

3. Open Grafana at http://localhost:3000 (admin/admin)
4. Create a dashboard with RED metrics for user-service:
   - **Rate**: `rate(http_requests_total{service="user-service"}[1m])`
   - **Errors**: `rate(http_requests_total{service="user-service",status=~"5.."}[1m])`
   - **Duration**: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{service="user-service"}[5m]))`

## Part B: Distributed Tracing with Jaeger

1. Open Jaeger UI at http://localhost:16686
2. Log an activity (which calls user validation):
```bash
curl -X POST http://localhost:8003/v1/activities \
  -H "Content-Type: application/json" \
  -d '{"user_id": "...", "game_id": "...", "action": "played"}'
```
3. Find the trace for `POST /v1/activities` in Jaeger
4. Expand the waterfall — identify which service took the longest

## Part C: Logs with Loki

In Grafana, go to **Explore → Loki** and query:
```
{service="activity-service"} |= "activity_id"
```

Correlate a log line timestamp with a trace in Jaeger.

## Bonus: Add a slow endpoint
Add an artificial delay to one endpoint:
```python
import asyncio
@app.get("/v1/games/slow")
async def slow_game():
    await asyncio.sleep(2)  # simulate slow DB query
    return {"result": "slow"}
```
Find this in the Jaeger trace and the Grafana P95 latency chart.

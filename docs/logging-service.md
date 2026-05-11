# logging-service

GDPR-compliant logging-service. Runs on **port 8006**.

> **Storage**: SQLite in Modules 1–7, PostgreSQL from Module 8 onward.

## Tech Stack

| | |
|---|---|
| **Framework** | Flask |
| **ORM** | SQLAlchemy |
| **Migrations** | Flask-Migrate (Alembic) |
| **Database** | SQLite (Modules 1–7), PostgreSQL (Module 8 onward) |
| **Message broker** | Kafka (consumer for `activity.logged` events) |

> To demonstrate polyglot microservices architecture, logging-service uses **Flask** instead of FastAPI. The choice of framework is transparent to clients — all other services, the gateway, and the API contracts remain unchanged.

## Responsibilities

- **Consent management** — stores opt-in/opt-out status per user (the "decision" record)
- **Kafka consumer** — receives `activity.logged` events from activity-service; if user opted in → writes a structured entry to an append-only JSONL audit log file; if opted out → skips silently
- **Feature gating** — activity-service and game-service query consent before publishing events or serving personalised content; no consent = no recommendations, no activity feed

## REST endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/v1/consent/{user_id}` | Record consent decision (opt in or out) |
| `GET` | `/v1/consent/{user_id}` | Check current consent status |
| `DELETE` | `/v1/consent/{user_id}` | Withdraw consent (sets `granted: false`) |
| `DELETE` | `/v1/logs/{user_id}` | GDPR right to erasure — delete all log entries for user |

## Log file format

JSONL — one line per event, append-only:

```json
{ "timestamp": "2025-03-01T10:00:00Z", "user_id": "abc123", "action": "game.viewed", "service": "game-service", "ip_hash": "e3b0c44..." }
```

IP is hashed (not stored raw) — GDPR Art. 25 data minimisation.

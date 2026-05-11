# Module 8 — Containerisation

**Duration**: 2h in class
**Branch to submit**: `module-08/<team-name>`

---

## Objective

For seven modules, the phrase "it works on my machine" was acceptable. From this module on, it is not. Services are packaged into containers and run against a real database (PostgreSQL) instead of SQLite.

This is the module where the system stops being a local development project and starts looking like something you could actually deploy.

---

## What's provided

- Dockerfiles for all Python services (including the gateway) are already written — multi-stage builds, production-ready.
- `docker-compose.infra.yml` now includes PostgreSQL.
- `modules/module-08/docker-compose.override.yml` wires everything together.
- `notification-service` stays local (Node.js). It is intentionally never containerised.

---

## Part A — Read the Dockerfile *(~20 min)*

Open the Dockerfile in any Python service. It has two stages: `builder` and `runtime`.

Read it and answer these questions in your head (they will come up in REFLECTION.md and the oral presentation):
- Why does the `runtime` stage not run `pip install` directly?
- What does the `builder` stage put in `/install`, and why does `runtime` copy from there?
- Why is `notification-service` excluded from containerisation? Is that a shortcut or a deliberate choice?

No writing required here — just read and understand.

---

## Part B — SQLite → PostgreSQL *(~40 min)*

Each Python service needs to connect to PostgreSQL instead of SQLite. The change is in `config.py` — swap the `DATABASE_URL`:

```python
# Before
DATABASE_URL = "sqlite+aiosqlite:///./service.db"

# After
DATABASE_URL = "postgresql+asyncpg://gamehub:gamehub_pass@postgres:5432/<service>_db"
```

Start PostgreSQL first, then run Alembic migrations for each service:
```bash
docker compose -f docker-compose.infra.yml up -d postgres
# then from each service directory:
alembic upgrade head
```

Make sure migrations succeed for all Python services before moving on.

---

## Part C — Build and run everything in Docker *(~30 min)*

```bash
docker compose \
  -f docker-compose.infra.yml \
  -f modules/module-08/docker-compose.override.yml \
  up --build
```

Start `notification-service` locally as before:
```bash
node app.js   # port 8004
```

Verify the full system is reachable through the gateway:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/v1/users
curl http://localhost:8000/v1/games
curl http://localhost:8000/v1/activities
curl http://localhost:8000/v1/notifications
```

The gateway container is now the only port clients need to know about.

---

## Kubernetes — Instructor Demo *(no hands-on)*

Watch the instructor demo. No setup required.

| Object | What it does |
|---|---|
| Pod | Smallest deployable unit — one or more containers |
| Deployment | Declares how many replicas to run and how to update them |
| Service | Stable network address in front of a set of Pods |
| Ingress | Routes external HTTP traffic to Services |

Things to watch for: how rolling updates work, what happens when a Pod crashes, and how this compares to just running `docker compose up`.

---

## Discussion *(~15 min)*

- Your code did not change between Module 7 and Module 8 — only the packaging and the database changed. What does that tell you about the value of separating concerns?
- `notification-service` is never containerised. Is that a problem for the system, or an acceptable design choice?
- What is the risk of running database migrations (Alembic) as part of service startup rather than as a separate step?

---

## Minimum to submit this branch

- [ ] All Python services running in Docker with PostgreSQL (not SQLite)
- [ ] Alembic migrations applied successfully for all services
- [ ] Gateway reachable at port 8000, all routes working
- [ ] `notification-service` still reachable via gateway (running locally)
- [ ] `REFLECTION.md` completed and committed

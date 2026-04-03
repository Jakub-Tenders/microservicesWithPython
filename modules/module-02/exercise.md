# Module 2 Exercise — FastAPI Service Design

## What you'll build
A fully layered FastAPI service following DDD structure:
- Domain layer: SQLAlchemy models
- Application layer: Pydantic schemas + service class
- Infrastructure layer: async database + repository

## Steps

### Step 1: Run the services
```bash
cp .env.example .env
docker compose -f docker-compose.infra.yml up -d postgres redis
cd services/user-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

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

### Step 5: Extend the product-service
Add a `GET /v1/products/search?q=<term>` endpoint that searches by name.

**Hint:** Add a new method in `ProductRepository.search()` using SQLAlchemy `ilike`.

## Capstone Integration
Once both services pass tests, bring them up together:
```bash
docker compose -f docker-compose.infra.yml \
               -f modules/module-02/docker-compose.override.yml up --build
```
Verify Traefik routes at http://localhost:8088

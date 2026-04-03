# ShopMicro — Your Microservices Capstone

> EPITA · Microservices with Python

You are going to build a real distributed system from scratch — one service at a time.

By the end of this course, you will have a running e-commerce backend where:
- A customer logs in, browses products, and places an order
- Stock is updated automatically via an event stream
- A notification is sent asynchronously via a message queue
- Every request is traceable across services in a single dashboard
- The whole thing deploys with one command

**You build every piece of this yourself.** The modules give you the instructions and the concepts. The code is yours.

---

## How this works

Each module lives in `modules/module-XX/`. Open `exercise.md` to get started.

You will write your services inside the `services/` folder. It is empty on purpose.

Infrastructure (databases, message brokers, observability tools) is provided for you in `docker-compose.infra.yml` — you focus on the services, not the plumbing.

```
modules/
├── module-01/   ← Start here
├── module-02/
├── ...
└── module-10/

services/        ← You build this
```

---

## Prerequisites

- Docker + Docker Compose
- Python 3.12
- Node.js 20 (used in Module 4)
- A working terminal

---

## Starting the infrastructure

```bash
# Copy the environment config
cp .env.example .env

# Start all infrastructure services
docker compose -f docker-compose.infra.yml up -d
```

Once infrastructure is running, each module's `docker-compose.override.yml` adds your services on top:

```bash
docker compose -f docker-compose.infra.yml \
               -f modules/module-02/docker-compose.override.yml \
               up --build
```

---

## What you will have built by Module 10

```
                    ┌─────────────┐
    HTTP ──────────▶│   Traefik   │  API Gateway
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   ┌────────────┐  ┌───────────────┐  ┌─────────────┐
   │user-service│  │product-service│  │order-service│
   │ PostgreSQL │  │ PostgreSQL    │  │ PostgreSQL  │
   └────────────┘  │ + Redis       │  │ + Redis     │
                   └───────────────┘  └──────┬──────┘
                                             │ Kafka
                             ┌───────────────┴──────────────┐
                             ▼                              ▼
                  ┌──────────────────┐       ┌─────────────────────┐
                  │inventory-service │       │notification-service │
                  │ PostgreSQL       │       │ MongoDB             │
                  │ Kafka consumer   │       │ RabbitMQ consumer   │
                  └──────────────────┘       │ Node.js             │
                                             └─────────────────────┘
```

---

## Access points (once running)

| Tool | URL |
|---|---|
| User Service | http://localhost:8001/docs |
| Product Service | http://localhost:8002/docs |
| Order Service | http://localhost:8003/docs |
| Inventory Service | http://localhost:8004/docs |
| Notification Service | http://localhost:8005 |
| Traefik dashboard | http://localhost:8088 |
| RabbitMQ UI | http://localhost:15672 |
| Grafana | http://localhost:3000 |
| Jaeger | http://localhost:16686 |
| Keycloak | http://localhost:8080 |

---

## Final checklist

You are done when you can demonstrate all six:

- [ ] `docker compose up` → all services healthy
- [ ] Log in via Keycloak → place an order → inventory decremented → notification stored
- [ ] Grafana shows RED metrics (Rate, Errors, Duration) for each service
- [ ] Jaeger shows a full distributed trace for one order request
- [ ] Stop `inventory-service` → circuit breaker opens → restart → circuit recovers
- [ ] Push a commit → GitHub Actions builds and tests automatically

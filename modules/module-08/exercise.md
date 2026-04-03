# Module 8 Exercise — Docker + Kubernetes

> **This is where services get containerized.** Until now, Python services ran locally with uvicorn + SQLite. From this module onward, they run in Docker with PostgreSQL.
>
> **Exception:** notification-service stays local (Node.js + SQLite) — it is never containerized.

## Part A: Multi-stage Dockerfile review
Examine any service Dockerfile. Note the two stages:
1. **builder**: installs dependencies into `/install`
2. **runtime**: copies only installed packages + source code

Questions:
- Why does the runtime stage not run `pip install` directly?
- What is the benefit of `--prefix=/install`?
- How does `PYTHONDONTWRITEBYTECODE=1` help image size?

## Part B: SQLite → PostgreSQL migration
Each service now connects to PostgreSQL instead of SQLite. Update your `config.py`:

```python
# Before (Modules 2-7):
DATABASE_URL = "sqlite+aiosqlite:///./service.db"

# After (Module 8+):
DATABASE_URL = "postgresql+asyncpg://gamehub:gamehub_pass@postgres:5432/user_db"
```

Run Alembic migrations against the new PostgreSQL databases.

## Part C: Deploy to minikube

```bash
# Start minikube
minikube start --driver=docker --memory=4096

# Enable ingress addon (uses Traefik or nginx)
minikube addons enable ingress

# Point Docker CLI to minikube's Docker daemon
eval $(minikube docker-env)

# Build images inside minikube
docker build -t gamehub/user-service:latest ./services/user-service
docker build -t gamehub/game-service:latest ./services/game-service
docker build -t gamehub/activity-service:latest ./services/activity-service
docker build -t gamehub/logging-service:latest ./services/logging-service
```

## Part D: Install via Helm

```bash
# Install user-service
helm install user-service ./helm/user-service \
  --set image.tag=latest \
  --set database.url="postgresql+asyncpg://gamehub:gamehub_pass@postgres:5432/user_db"

# Check deployment
kubectl get pods
kubectl get svc
kubectl get ingress

# Port-forward to test locally
kubectl port-forward svc/user-service 8001:8001

# Check logs
kubectl logs -l app=user-service -f
```

## Part E: Scale and rolling update

```bash
# Scale to 3 replicas
kubectl scale deployment user-service --replicas=3

# Rolling update (change image tag, then apply)
helm upgrade user-service ./helm/user-service --set image.tag=v1.1.0

# Watch rollout
kubectl rollout status deployment/user-service
```

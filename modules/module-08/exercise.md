# Module 8 Exercise — Docker + Kubernetes

## Part A: Multi-stage Dockerfile review
Examine any service Dockerfile. Note the two stages:
1. **builder**: installs dependencies into `/install`
2. **runtime**: copies only installed packages + source code

Questions:
- Why does the runtime stage not run `pip install` directly?
- What is the benefit of `--prefix=/install`?
- How does `PYTHONDONTWRITEBYTECODE=1` help image size?

## Part B: Deploy to minikube

```bash
# Start minikube
minikube start --driver=docker --memory=4096

# Enable ingress addon (uses Traefik or nginx)
minikube addons enable ingress

# Point Docker CLI to minikube's Docker daemon
eval $(minikube docker-env)

# Build images inside minikube
docker build -t shopmicro/user-service:latest ./services/user-service
```

## Part C: Install via Helm

```bash
# Install user-service
helm install user-service ./helm/user-service \
  --set image.tag=latest \
  --set database.url="postgresql+asyncpg://shopmicro:pass@postgres:5432/user_db"

# Check deployment
kubectl get pods
kubectl get svc
kubectl get ingress

# Port-forward to test locally
kubectl port-forward svc/user-service 8001:8001

# Check logs
kubectl logs -l app=user-service -f
```

## Part D: Scale and rolling update

```bash
# Scale to 3 replicas
kubectl scale deployment user-service --replicas=3

# Rolling update (change image tag, then apply)
helm upgrade user-service ./helm/user-service --set image.tag=v1.1.0

# Watch rollout
kubectl rollout status deployment/user-service
```

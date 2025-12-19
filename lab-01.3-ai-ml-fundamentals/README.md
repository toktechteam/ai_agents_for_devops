# Chapter 1 Lab – AI/ML Fundamentals for DevOps Engineers

This lab is designed to help a **DevOps engineer** understand how **AI/ML workloads** differ from normal web apps — without needing any deep data science background.

You will:

- Run a **simple "fake ML model" API** using FastAPI
- Containerize it with Docker
- Deploy it to a **kind (Kubernetes-in-Docker)** cluster
- Compare **FREE vs PAID** versions:
  - FREE: Minimal, straightforward, enough for basic understanding
  - PAID: Production-leaning with config, resources, autoscaling, and CI

---

## Learning Outcomes

By the end of this lab, you'll be able to:

- Explain how **inference workloads** behave (CPU usage, latency, concurrency)
- Containerize a basic AI-like service
- Deploy to Kubernetes with proper **resources** and **health checks**
- Understand why AI workloads often need **tighter SLOs** and **autoscaling**

---

## Prerequisites

**Operating System:**
- Ubuntu 22.04 (or similar Linux / WSL2 / macOS)

**Required Software:**
- Docker 24+
- kind
- kubectl ≥ 1.29
- Python 3.11+
- Git

**Basic Familiarity With:**
- Docker build/run
- `kubectl apply`, `kubectl get pods`, etc.

---

## 1. Repository Structure

This chapter folder contains:

```
chapter-01-ai-ml-fundamentals/
├── free/                      # FREE version of the lab (simplified)
├── paid/                      # PAID version (more production-ready)
├── kind-mcp-cluster.yaml      # Kind cluster config used for lab
└── .github/
    └── workflows/
        └── ci.yml             # GitHub Actions CI pipeline
```

---

## 2. Setting Up kind Cluster

### 2.1 Create the Cluster

From inside `chapter-01-ai-ml-fundamentals/`:

```bash
kind create cluster --config kind-mcp-cluster.yaml
```

Verify:

```bash
kubectl get nodes
```

Expected output (example):

```
NAME                      STATUS   ROLES           AGE   VERSION
mcp-cluster-control-plane Ready    control-plane   30s   v1.30.0
```

---

## 3. FREE Version – Quick AI Inference API

### 3.1 Build Docker Image

From inside `chapter-01-ai-ml-fundamentals/free`:

```bash
docker build -t ai-lab-free:v1 .
```

### 3.2 Load Image into kind

```bash
kind load docker-image ai-lab-free:v1 --name mcp-cluster
```

### 3.3 Deploy to Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Check:

```bash
kubectl get pods
kubectl get svc ai-lab-free
```

Expected:
- Pod status: `Running`
- Service: `ClusterIP` with a stable internal IP

For local testing, use `kubectl port-forward`:

```bash
kubectl port-forward deploy/ai-lab-free 8000:8000
```

Now test the API:

```bash
curl -s http://localhost:8000/health
```

Expected JSON:

```json
{"status": "ok"}
```

Inference test:

```bash
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.5]}'
```

Expected sample output:

```json
{"prediction": 6.5, "model_latency_ms": 50}
```

*(Exact latency may differ; value is simulated.)*

### 3.4 Run Unit Tests (FREE)

From `chapter-01-ai-ml-fundamentals/free/app`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

Expected:

```
================== test session starts ==================
collected 2 items

tests/test_app.py ..                              [100%]

=================== 2 passed in X.XXs ===================
```

---

## 4. PAID Version – Closer to Production

The PAID version adds:

- Separate `model.py` and `config.py`
- `.env`-driven configuration
- Resource requests and limits
- Horizontal Pod Autoscaler (HPA)
- Namespace isolation
- CI pipeline in `.github/workflows/ci.yml`

### 4.1 Configure Environment

Copy the example env file:

```bash
cd chapter-01-ai-ml-fundamentals/paid
cp .env.example .env
```

You can tweak:
- `APP_ENV`
- `DEFAULT_LATENCY_MS`
- `MAX_BATCH_SIZE`

### 4.2 Build Docker Image

```bash
docker build -t ai-lab-paid:v1 .
```

### 4.3 Load Image into kind

```bash
kind load docker-image ai-lab-paid:v1 --name mcp-cluster
```

### 4.4 Deploy Namespace + App + HPA

From `chapter-01-ai-ml-fundamentals/paid`:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

Check:

```bash
kubectl get pods -n ai-ml-lab
kubectl get svc -n ai-ml-lab
kubectl get hpa -n ai-ml-lab
```

Port-forward:

```bash
kubectl port-forward -n ai-ml-lab deploy/ai-lab-paid 9000:9000
```

Health check:

```bash
curl -s http://localhost:9000/health
```

Expected:

```json
{"status": "ok", "env": "local"}
```

Prediction:

```bash
curl -s -X POST http://localhost:9000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.5, 1.5, 2]}'
```

Expected sample output:

```json
{
  "prediction": 4.0,
  "model_name": "simple-linear-demo",
  "latency_ms": 100
}
```

*(The exact values may differ slightly; the logic is deterministic for the given input.)*

### 4.5 Run Unit Tests (PAID)

From `chapter-01-ai-ml-fundamentals/paid/app`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

Expected:

```
================== test session starts ==================
collected 3 items

tests/test_app.py ...                            [100%]

=================== 3 passed in X.XXs ===================
```

---

## 5. CI Pipeline (GitHub Actions)

Once you push this chapter to GitHub, the workflow at:

```
.github/workflows/ci.yml
```

will:

1. Run tests for FREE and PAID apps
2. Build Docker images (without pushing to any registry)

You can trigger it automatically on push or manually via the GitHub UI.

---

## 6. Works on My Machine – Quick Rubric

From a fresh clone inside `chapter-01-ai-ml-fundamentals`:

**1. Create kind cluster**

```bash
kind create cluster --config kind-mcp-cluster.yaml
kubectl get nodes
```

**2. FREE app local test**

```bash
cd free/app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

In another terminal:

```bash
curl -s http://localhost:8000/health
```

**3. FREE app on Kubernetes**

```bash
cd ../..
docker build -t ai-lab-free:v1 .
kind load docker-image ai-lab-free:v1 --name mcp-cluster
kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml
kubectl port-forward deploy/ai-lab-free 8000:8000
curl -s http://localhost:8000/health
```

**4. PAID app on Kubernetes**

```bash
cd ../paid
cp .env.example .env
docker build -t ai-lab-paid:v1 .
kind load docker-image ai-lab-paid:v1 --name mcp-cluster
kubectl apply -f k8s/namespace.yaml -f k8s/deployment.yaml -f k8s/service.yaml -f k8s/hpa.yaml
kubectl port-forward -n ai-ml-lab deploy/ai-lab-paid 9000:9000
curl -s http://localhost:9000/health
```

If all of these work, the lab is ✅

---

## 7. Cleanup

To avoid leftover resources:

```bash
# Delete PAID resources
kubectl delete -f paid/k8s/hpa.yaml
kubectl delete -f paid/k8s/service.yaml
kubectl delete -f paid/k8s/deployment.yaml
kubectl delete -f paid/k8s/namespace.yaml

# Delete FREE resources
kubectl delete -f free/k8s/service.yaml
kubectl delete -f free/k8s/deployment.yaml

# Delete kind cluster
kind delete cluster --name mcp-cluster
```

---

## 8. Troubleshooting

### Pods not starting / ImagePullBackOff

Make sure you loaded the local image into kind:

```bash
kind load docker-image ai-lab-free:v1 --name mcp-cluster
kind load docker-image ai-lab-paid:v1 --name mcp-cluster
```

### Port-forward fails

Check pod status:

```bash
kubectl get pods
kubectl logs <pod-name>
```

### Tests failing

Ensure you're using the correct Python version and virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
```

Reinstall dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Questions or Issues?

Buy Ebook from here : https://theopskart.gumroad.com/l/AIAgentsforDevOps

If you encounter any problems with this lab, please check the troubleshooting section above or review the logs from your pods and containers.

Happy learning! 🚀
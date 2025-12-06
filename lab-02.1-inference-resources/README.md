# FREE Version – Quick AI Inference API Lab

This is the **FREE version** of the AI/ML Fundamentals lab for DevOps engineers. It provides a minimal, straightforward introduction to deploying AI-like services without needing deep data science knowledge.

## What You'll Learn

- How **inference workloads** behave (CPU usage, latency, concurrency)
- Containerizing a basic AI-like service with Docker
- Deploying to Kubernetes with health checks
- Testing AI service endpoints

---

## Prerequisites

**Operating System:**
- Ubuntu 22.04 (or similar Linux / WSL2 / macOS)

**Required Software:**
- Docker 24+
- kind (Kubernetes in Docker)
- kubectl ≥ 1.29
- Python 3.11+
- Git

**Basic Familiarity With:**
- Docker build/run commands
- `kubectl apply`, `kubectl get pods`, etc.

---

## Repository Structure

```
chapter-02.1-inference-resources/
├── app/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── tests/
│       └── test_app.py      # Unit tests
├── k8s/
│   ├── deployment.yaml      # Kubernetes deployment
│   └── service.yaml         # Kubernetes service
└── Dockerfile               # Container image definition
```

---

## Quick Start Guide

### Step 1: Create kind Cluster

From the parent directory:

```bash
kind create cluster --config kind-mcp-cluster.yaml
```

Verify the cluster is running:

```bash
kubectl get nodes
```

Expected output:

```
NAME                      STATUS   ROLES           AGE   VERSION
mcp-cluster-control-plane Ready    control-plane   30s   v1.30.0
```

### Step 2: Build Docker Image

From inside the `free/` directory:

```bash
docker build -t ai-lab-free:v1 .
```

### Step 3: Load Image into kind

```bash
kind load docker-image ai-lab-free:v1 --name mcp-cluster
```

### Step 4: Deploy to Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Check deployment status:

```bash
kubectl get pods
kubectl get svc ai-lab-free
```

Expected:
- Pod status: `Running`
- Service: `ClusterIP` with a stable internal IP

---

## Testing the API

### Local Port Forward

To access the service locally:

```bash
kubectl port-forward deploy/ai-lab-free 8000:8000
```

### Health Check

Test the health endpoint:

```bash
curl -s http://localhost:8000/health
```

Expected response:

```json
{"status": "ok"}
```

### Inference Test

Make a prediction request:

```bash
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.5]}'
```

Expected response:

```json
{"prediction": 6.5, "model_latency_ms": 50}
```

*Note: The exact latency may vary; the value is simulated.*

---

## Running Unit Tests

From the `free/app` directory:

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```

Expected output:

```
================== test session starts ==================
collected 2 items

tests/test_app.py ..                              [100%]

=================== 2 passed in X.XXs ===================
```

---

## Local Development

To run the FastAPI app locally (without Kubernetes):

```bash
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

In another terminal:

```bash
curl -s http://localhost:8000/health
```

---

## Cleanup

Remove all FREE lab resources:

```bash
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
```

Delete the kind cluster:

```bash
kind delete cluster --name mcp-cluster
```

---

## Troubleshooting

### Pods not starting / ImagePullBackOff

Ensure the image is loaded into kind:

```bash
kind load docker-image ai-lab-free:v1 --name mcp-cluster
```

Check pod status:

```bash
kubectl get pods
kubectl describe pod <pod-name>
```

### Port-forward fails

Verify the pod is running:

```bash
kubectl get pods
kubectl logs <pod-name>
```

### Tests failing

Ensure correct Python version and dependencies:

```bash
python --version  # Should be 3.11+
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pytest
```

### Connection refused on localhost:8000

Make sure port-forward is running:

```bash
kubectl port-forward deploy/ai-lab-free 8000:8000
```

---

## Next Steps

Once you're comfortable with the FREE version, explore the **PAID version** which includes:

- Production-ready configuration with environment variables
- Resource requests and limits
- Horizontal Pod Autoscaler (HPA)
- Namespace isolation
- CI/CD pipeline integration

---

## Questions or Issues?

Check the troubleshooting section above or review pod logs:

```bash
kubectl logs <pod-name>
```

Happy learning! 🚀
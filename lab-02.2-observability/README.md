# FREE Version – Observability for AI Inference Lab

This is the **FREE version** of Lab 2.2, teaching DevOps engineers how to add basic observability to AI inference services running in Kubernetes.

## What You'll Learn

- Why AI inference systems need deeper observability than normal CRUD apps
- How to emit basic logs using stdout
- How to create custom lightweight metrics endpoints
- How to build a simple Python load generator
- How DevOps teams debug latency issues in ML inference
- Fully offline observability (no external backend required)

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
- Kubernetes deployments and services
- Basic metrics concepts (counters, gauges)
- curl or similar HTTP clients

---

## Repository Structure

```
free/
├── app/
│   ├── main.py              # FastAPI app with metrics endpoint
│   ├── requirements.txt     # Python dependencies
│   └── tests/
│       └── test_app.py      # Unit tests
├── k8s/
│   ├── deployment.yaml      # Kubernetes deployment
│   └── service.yaml         # Kubernetes service
├── load-generator/
│   └── generate_load.py     # Simple load testing script
└── Dockerfile               # Container image definition
```

---

## Features

The FREE version includes:

✅ **Basic Stdout Logging** - Simple logging to container stdout  
✅ **Custom Metrics Endpoint** - Lightweight `/metrics-lite` endpoint  
✅ **Request Tracking** - Count total requests and track latency  
✅ **Simple Load Generator** - Python script to simulate traffic  
✅ **Offline Operation** - No external dependencies or backends  
✅ **Zero Cost** - Runs entirely in KIND cluster  

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

From the `free/` directory:

```bash
docker build -t ai-lab-2-2-free:v1 .
```

### Step 3: Load Image into kind

```bash
kind load docker-image ai-lab-2-2-free:v1 --name mcp-cluster
```

### Step 4: Deploy to Kubernetes

```bash
kubectl apply -f k8s/
```

Check deployment status:

```bash
kubectl get pods
kubectl get svc ai-lab-2-2-free
```

Expected:
- Pod status: `Running`
- Service: `ClusterIP` with a stable internal IP

---

## Testing Observability Features

### Access the Application

Port-forward the service to your local machine:

```bash
kubectl port-forward deploy/ai-lab-2-2-free 8002:8000
```

### Health Check

```bash
curl http://localhost:8002/health
```

Expected response:

```json
{"status": "ok"}
```

### View Metrics

Access the lightweight metrics endpoint:

```bash
curl http://localhost:8002/metrics-lite
```

Expected response:

```json
{
  "total_requests": 1,
  "total_predictions": 0,
  "avg_latency_ms": 0,
  "uptime_seconds": 123
}
```

### Make Prediction Requests

```bash
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.5]}'
```

Expected response:

```json
{
  "prediction": 6.5,
  "model_latency_ms": 50
}
```

### Check Updated Metrics

```bash
curl http://localhost:8002/metrics-lite
```

You should see updated counters:

```json
{
  "total_requests": 5,
  "total_predictions": 4,
  "avg_latency_ms": 52,
  "uptime_seconds": 245
}
```

---

## Viewing Logs

### Stream Application Logs

```bash
kubectl logs -f deploy/ai-lab-2-2-free
```

You'll see logs like:

```
INFO:     Started server process
INFO:     Application startup complete
INFO:     Prediction request received - latency: 48ms
INFO:     Prediction request received - latency: 51ms
```

### Filter Logs

Search for specific log entries:

```bash
kubectl logs deploy/ai-lab-2-2-free | grep "Prediction"
```

---

## Load Testing

### Using the Simple Load Generator

From the `free/load-generator/` directory:

```bash
# Install dependencies
pip install requests

# Run load generator
python generate_load.py --url http://localhost:8002 --requests 100
```

The load generator will:
- Send 100 prediction requests
- Print summary statistics
- Show average latency

Expected output:

```
Sending 100 requests to http://localhost:8002/predict...
Progress: [####################] 100/100
Complete!

Summary:
- Total requests: 100
- Successful: 100
- Failed: 0
- Average latency: 52ms
- Min latency: 45ms
- Max latency: 68ms
```

### Check Metrics After Load Test

```bash
curl http://localhost:8002/metrics-lite
```

You should see increased counters reflecting the load test.

---

## Understanding the Metrics

### Available Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `total_requests` | Counter | Total HTTP requests received |
| `total_predictions` | Counter | Total prediction requests processed |
| `avg_latency_ms` | Gauge | Average prediction latency in milliseconds |
| `uptime_seconds` | Gauge | Application uptime |

### Why These Metrics Matter

**For AI/ML Inference:**
- **Latency** - Critical for user experience and SLOs
- **Request Count** - Helps with capacity planning
- **Prediction Count** - Tracks actual model usage
- **Uptime** - Monitors service availability

Unlike typical CRUD apps, ML inference services often have:
- Higher latency variance
- CPU-intensive workloads
- Strict SLA requirements
- Need for detailed performance tracking

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
collected 3 items

tests/test_app.py ...                            [100%]

=================== 3 passed in X.XXs ===================
```

---

## Local Development

Run the FastAPI app locally (without Kubernetes):

```bash
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

In another terminal:

```bash
# Health check
curl http://localhost:8000/health

# Metrics
curl http://localhost:8000/metrics-lite

# Prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.5]}'
```

---

## Debugging Common Issues

### No Metrics Data

If metrics show all zeros:

1. Make sure you've sent some requests first
2. Check logs for errors
3. Verify the app is running

```bash
kubectl get pods
kubectl logs deploy/ai-lab-2-2-free
```

### High Latency

If latency is higher than expected:

1. Check pod resource usage
2. Look for CPU throttling
3. Review logs for errors

```bash
kubectl top pod
kubectl describe pod <pod-name>
```

### Load Generator Fails

If the load generator can't connect:

1. Verify port-forward is running
2. Check the URL is correct
3. Ensure the pod is healthy

```bash
kubectl get pods
kubectl port-forward deploy/ai-lab-2-2-free 8002:8000
```

---

## Cost Analysis

### FREE Version Cost: $0

This version runs entirely in KIND and has:
- No external dependencies
- No cloud services
- No data egress costs
- No storage costs

**Perfect for:**
- Learning and experimentation
- Local development
- CI/CD testing
- Proof of concepts

---

## Cleanup

Remove all FREE lab resources:

```bash
kubectl delete -f k8s/
```

Delete the kind cluster:

```bash
kind delete cluster --name mcp-cluster
```

---

## Troubleshooting

### Pod Not Starting

Check pod status and logs:

```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

Ensure image is loaded:

```bash
kind load docker-image ai-lab-2-2-free:v1 --name mcp-cluster
```

### Port-Forward Fails

Verify deployment is running:

```bash
kubectl get deployments
kubectl get pods
```

Try a different local port:

```bash
kubectl port-forward deploy/ai-lab-2-2-free 8003:8000
```

### Metrics Endpoint Not Responding

Check if the app started correctly:

```bash
kubectl logs deploy/ai-lab-2-2-free
```

Verify the endpoint path:

```bash
curl http://localhost:8002/metrics-lite  # Correct
curl http://localhost:8002/metrics       # Wrong
```

### Load Generator Errors

Ensure dependencies are installed:

```bash
pip install requests
```

Check that port-forward is active:

```bash
# Should show the port-forward process
ps aux | grep port-forward
```

---

## Next Steps

### Explore the PAID Version

The PAID version adds:

- **OpenTelemetry Integration** - Industry-standard tracing and metrics
- **OTLP Pipeline** - Send data to OpenTelemetry Collector
- **Rich Metrics** - Histogram buckets for latency distribution
- **Distributed Tracing** - Track requests across services
- **Production Features** - Namespaces, resource limits, proper observability

### Additional Learning

- Study OpenTelemetry concepts
- Learn about Prometheus metrics format
- Explore distributed tracing patterns
- Understand SLOs and SLIs for ML services

---

## Key Takeaways

✅ **Logs are essential** - Use stdout for easy Kubernetes collection  
✅ **Basic metrics help** - Even simple counters provide value  
✅ **Latency matters** - Track and optimize inference latency  
✅ **Start simple** - Build observability incrementally  
✅ **Test locally** - KIND provides a great development environment  

---

## Questions or Issues?

Check the troubleshooting section above or review pod logs:

```bash
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```

Happy learning about AI inference observability! 🚀📊
# Lab 2.2 FREE Version Setup Guide
## Observability for AI Inference Workloads - Basic Metrics & Logs

---

## 🎯 What You Will Achieve

By completing this lab, you will:

### Learning Objectives
1. **Understand AI/ML observability basics** - Learn why AI inference workloads need different monitoring than traditional CRUD applications
2. **Implement basic logging** - Set up stdout logging for Kubernetes-friendly log collection
3. **Create custom metrics** - Build a lightweight metrics endpoint without external dependencies
4. **Deploy to Kubernetes** - Practice deploying observable services to a local cluster
5. **Debug inference latency** - Learn to identify and troubleshoot performance issues

### Expected Outcomes
- ✅ A running AI inference service with built-in observability
- ✅ Ability to view real-time logs using kubectl
- ✅ Custom metrics endpoint showing request counts and latency
- ✅ Understanding of basic observability patterns for ML services
- ✅ Hands-on experience with load testing and metric validation

### Real-World Application
- **DevOps Engineers** can apply these patterns to monitor production ML services
- **SREs** can use these metrics to set up basic alerting and SLOs
- **Platform Teams** can standardize observability across AI workloads
- **Cost-conscious teams** can implement observability without external tools

---

## 📋 Prerequisites

### Required Software
- **Operating System:** Ubuntu 22.04 (or similar Linux / WSL2 / macOS)
- **Docker:** Version 24 or higher
- **kind:** Kubernetes in Docker
- **kubectl:** Version 1.29 or higher
- **Python:** Version 3.11 or higher
- **Git:** For cloning repositories

### Required Knowledge
- Basic Docker commands (`docker build`, `docker run`)
- Basic Kubernetes concepts (pods, deployments, services)
- Basic curl usage for HTTP requests
- Familiarity with command-line terminals

### Verification Commands

Check Docker:
```bash
docker --version
# Expected: Docker version 24.x.x or higher
```

Check kind:
```bash
kind --version
# Expected: kind v0.20.0 or higher
```

Check kubectl:
```bash
kubectl version --client
# Expected: v1.29.0 or higher
```

Check Python:
```bash
python3 --version
# Expected: Python 3.11.x or higher
```

---

## 🚀 Step-by-Step Setup

### Step 1: Create kind Cluster

Navigate to the lab directory:
```bash
cd lab-02.2-observability
```

Create the cluster:
```bash
kind create cluster --config kind-mcp-cluster.yaml
```

**Expected Output:**
```
Creating cluster "mcp-cluster" ...
 ✓ Ensuring node image (kindest/node:v1.30.0) 🖼
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-mcp-cluster"
You can now use your cluster with:

kubectl cluster-info --context kind-mcp-cluster
```

**Verify the cluster:**
```bash
kubectl get nodes
```

**Expected Output:**
```
NAME                      STATUS   ROLES           AGE   VERSION
mcp-cluster-control-plane Ready    control-plane   45s   v1.30.0
```

**Verify kubectl context:**
```bash
kubectl config current-context
```

**Expected Output:**
```
kind-mcp-cluster
```

---

### Step 2: Navigate to FREE Directory

```bash
cd free
```

Verify you're in the correct directory:
```bash
ls
```

**Expected Output:**
```
Dockerfile  app/  k8s/  load-generator/
```

---

### Step 3: Build Docker Image

Build the application image:
```bash
docker build -t ai-lab-2-2-free:v1 .
```

**Expected Output:**
```
[+] Building 45.2s (12/12) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 234B
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/python:3.11-slim
 => [1/6] FROM docker.io/library/python:3.11-slim
 => [2/6] WORKDIR /app
 => [3/6] COPY app/requirements.txt .
 => [4/6] RUN pip install --no-cache-dir -r requirements.txt
 => [5/6] COPY app/ .
 => [6/6] RUN useradd -m appuser && chown -R appuser:appuser /app
 => exporting to image
 => => exporting layers
 => => writing image sha256:abc123...
 => => naming to docker.io/library/ai-lab-2-2-free:v1
```

**Verify the image was built:**
```bash
docker images | grep ai-lab-2-2-free
```

**Expected Output:**
```
ai-lab-2-2-free   v1      abc123def456   1 minute ago   245MB
```

---

### Step 4: Load Image into kind

Load the Docker image into the kind cluster:
```bash
kind load docker-image ai-lab-2-2-free:v1 --name mcp-cluster
```

**Expected Output:**
```
Image: "ai-lab-2-2-free:v1" with ID "sha256:abc123..." not yet present on node "mcp-cluster-control-plane", loading...
```

**Verify image in kind:**
```bash
docker exec -it mcp-cluster-control-plane crictl images | grep ai-lab-2-2-free
```

**Expected Output:**
```
docker.io/library/ai-lab-2-2-free   v1      abc123def456   245MB
```

---

### Step 5: Deploy to Kubernetes

Deploy the application:
```bash
kubectl apply -f k8s/
```

**Expected Output:**
```
deployment.apps/ai-lab-2-2-free created
service/ai-lab-2-2-free created
```

**Wait for deployment to be ready:**
```bash
kubectl wait --for=condition=available --timeout=60s deployment/ai-lab-2-2-free
```

**Expected Output:**
```
deployment.apps/ai-lab-2-2-free condition met
```

---

### Step 6: Verify Deployment

Check pods:
```bash
kubectl get pods
```

**Expected Output:**
```
NAME                              READY   STATUS    RESTARTS   AGE
ai-lab-2-2-free-xxxxxxxxxx-xxxxx  1/1     Running   0          30s
```

**Note:** The pod name will have random characters after `ai-lab-2-2-free-`.

Check pod details:
```bash
kubectl get pods -l app=ai-lab-2-2-free -o wide
```

**Expected Output:**
```
NAME                              READY   STATUS    RESTARTS   AGE   IP           NODE
ai-lab-2-2-free-xxxxxxxxxx-xxxxx  1/1     Running   0          45s   10.244.0.5   mcp-cluster-control-plane
```

Check service:
```bash
kubectl get svc ai-lab-2-2-free
```

**Expected Output:**
```
NAME              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
ai-lab-2-2-free   ClusterIP   10.96.123.45    <none>        8000/TCP   1m
```

---

### Step 7: View Application Logs

View initial logs:
```bash
kubectl logs -l app=ai-lab-2-2-free
```

**Expected Output:**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

This confirms the FastAPI application has started successfully.

---

### Step 8: Set Up Port Forwarding

Forward the service port to your local machine:
```bash
kubectl port-forward deploy/ai-lab-2-2-free 8002:8000
```

**Expected Output:**
```
Forwarding from 127.0.0.1:8002 -> 8000
Forwarding from [::1]:8002 -> 8000
```

**Keep this terminal open!** Open a new terminal for testing.

---

## ✅ Testing and Validation

### Test 1: Health Check Endpoint

Test the health endpoint:
```bash
curl http://localhost:8002/health
```

**Expected Response:**
```json
{"status":"ok"}
```

**What this validates:**
- ✅ Application is running and responding
- ✅ FastAPI server is healthy
- ✅ Port forwarding is working correctly

---

### Test 2: Initial Metrics Check

View the metrics endpoint:
```bash
curl http://localhost:8002/metrics-lite
```

**Expected Response:**
```json
{
  "total_requests": 1,
  "total_predictions": 0,
  "avg_latency_ms": 0,
  "uptime_seconds": 15
}
```

**What this validates:**
- ✅ Custom metrics endpoint is functional
- ✅ Request counter is working (incremented by the health check)
- ✅ Uptime tracking is working

**Understanding the metrics:**
- `total_requests` - Total HTTP requests (includes health checks)
- `total_predictions` - Only counts `/predict` endpoint calls
- `avg_latency_ms` - Average prediction latency (0 until predictions are made)
- `uptime_seconds` - How long the application has been running

---

### Test 3: Make Prediction Requests

Make a single prediction:
```bash
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.5]}'
```

**Expected Response:**
```json
{
  "prediction": 6.5,
  "model_latency_ms": 50
}
```

**What this validates:**
- ✅ Prediction endpoint is working
- ✅ Model inference is functioning
- ✅ Latency is being tracked

Make multiple predictions with different inputs:
```bash
# Prediction 2
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [2.0, 3.0, 4.0]}'

# Prediction 3
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.5, 1.5, 2.5]}'
```

---

### Test 4: Verify Updated Metrics

Check metrics after predictions:
```bash
curl http://localhost:8002/metrics-lite
```

**Expected Response:**
```json
{
  "total_requests": 7,
  "total_predictions": 3,
  "avg_latency_ms": 51,
  "uptime_seconds": 120
}
```

**What this validates:**
- ✅ Request counter increased (health checks + metrics checks + predictions)
- ✅ Prediction counter shows 3 predictions made
- ✅ Average latency is calculated correctly (~50ms)
- ✅ Metrics are updating in real-time

---

### Test 5: Verify Logs Show Activity

View logs to see request activity:
```bash
kubectl logs -l app=ai-lab-2-2-free --tail=20
```

**Expected Output:**
```
INFO:     127.0.0.1:xxxxx - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "GET /metrics-lite HTTP/1.1" 200 OK
INFO:     Prediction request received - features: [1.0, 2.0, 3.5]
INFO:     Prediction completed - latency: 48ms, result: 6.5
INFO:     127.0.0.1:xxxxx - "POST /predict HTTP/1.1" 200 OK
INFO:     Prediction request received - features: [2.0, 3.0, 4.0]
INFO:     Prediction completed - latency: 52ms, result: 9.0
INFO:     127.0.0.1:xxxxx - "POST /predict HTTP/1.1" 200 OK
```

**What this validates:**
- ✅ Logging is working correctly
- ✅ Each prediction is logged with details
- ✅ Latency information is captured in logs
- ✅ HTTP response codes are logged

---

### Test 6: Stream Live Logs

Open a new terminal and stream logs in real-time:
```bash
kubectl logs -f -l app=ai-lab-2-2-free
```

In another terminal, make requests:
```bash
for i in {1..5}; do
  curl -X POST http://localhost:8002/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [1.0, 2.0, 3.5]}' -s > /dev/null
  sleep 1
done
```

**Expected Output in log stream:**
```
INFO:     Prediction request received - features: [1.0, 2.0, 3.5]
INFO:     Prediction completed - latency: 49ms, result: 6.5
INFO:     127.0.0.1:xxxxx - "POST /predict HTTP/1.1" 200 OK
INFO:     Prediction request received - features: [1.0, 2.0, 3.5]
INFO:     Prediction completed - latency: 51ms, result: 6.5
...
```

**What this validates:**
- ✅ Real-time log streaming works
- ✅ Logs appear immediately as requests are processed
- ✅ You can monitor the system in real-time

Press `Ctrl+C` to stop streaming logs.

---

### Test 7: Load Testing with Python Script

Navigate to the load generator directory:
```bash
cd load-generator
```

Install dependencies:
```bash
pip install requests
```

Run the load generator:
```bash
python generate_load.py --url http://localhost:8002 --requests 100
```

**Expected Output:**
```
Sending 100 requests to http://localhost:8002/predict...
Progress: [####################] 100/100
Complete!

Summary:
========================================
Total requests:     100
Successful:         100
Failed:             0
Duration:           5.2s
Requests/sec:       19.2

Latency Statistics:
  Minimum:          45ms
  Maximum:          68ms
  Average:          51ms
  Median:           50ms
```

**What this validates:**
- ✅ Application handles concurrent load
- ✅ Latency remains consistent under load
- ✅ No errors occur during sustained requests
- ✅ Performance metrics are realistic

---

### Test 8: Verify Metrics After Load Test

Check final metrics:
```bash
cd ..
curl http://localhost:8002/metrics-lite
```

**Expected Response:**
```json
{
  "total_requests": 110,
  "total_predictions": 103,
  "avg_latency_ms": 51,
  "uptime_seconds": 300
}
```

**What this validates:**
- ✅ Metrics accurately reflect all requests
- ✅ Counters are reliable under load
- ✅ Average latency calculation is correct
- ✅ System tracked 100+ predictions successfully

---

### Test 9: Error Handling

Test invalid input:
```bash
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'
```

**Expected Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "features"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**What this validates:**
- ✅ Application handles errors gracefully
- ✅ Validation is working correctly
- ✅ Error responses are properly formatted

Check logs for error handling:
```bash
kubectl logs -l app=ai-lab-2-2-free --tail=5
```

---

### Test 10: Pod Restart Recovery

Test that metrics reset after pod restart:
```bash
# Get current metrics
curl http://localhost:8002/metrics-lite

# Delete the pod (Kubernetes will automatically recreate it)
kubectl delete pod -l app=ai-lab-2-2-free

# Wait for new pod to be ready
kubectl wait --for=condition=ready pod -l app=ai-lab-2-2-free --timeout=60s

# Restart port-forward
kubectl port-forward deploy/ai-lab-2-2-free 8002:8000 &

# Wait a moment for port-forward to establish
sleep 3

# Check metrics (should be reset)
curl http://localhost:8002/metrics-lite
```

**Expected Response:**
```json
{
  "total_requests": 1,
  "total_predictions": 0,
  "avg_latency_ms": 0,
  "uptime_seconds": 5
}
```

**What this validates:**
- ✅ Kubernetes automatically restarts failed pods
- ✅ Application state resets on restart
- ✅ Metrics start fresh (in-memory storage)
- ✅ High availability mechanisms work

---

## 🎓 Understanding What You've Built

### Observability Components

**1. Logging:**
- Stdout logging captures all application events
- Kubernetes automatically collects stdout logs
- Logs include request details, latency, and errors
- Accessible via `kubectl logs` command

**2. Metrics:**
- Custom lightweight metrics endpoint
- No external dependencies (Prometheus, etc.)
- Real-time request counting and latency tracking
- In-memory storage (resets on pod restart)

**3. Why This Matters for AI/ML:**
- ML inference has variable latency
- Need to track prediction counts separately from health checks
- Latency directly impacts user experience
- Cost optimization requires understanding usage patterns

### Key Learning Points

**Difference from Traditional Apps:**
- Traditional CRUD: Predictable latency, standard HTTP patterns
- AI Inference: Variable latency, CPU-intensive, need detailed metrics

**DevOps Implications:**
- Need latency percentiles (p50, p95, p99) not just averages
- Request counting helps with capacity planning
- Logs help debug model performance issues
- Metrics guide resource allocation decisions

**Production Considerations:**
- This FREE version is great for learning and development
- Production systems need persistent metrics storage
- Consider the PAID version for OpenTelemetry integration
- Add alerting for SLO violations (latency > threshold)

---

## 📊 Success Criteria Checklist

Your lab is complete when you can confirm:

- [ ] kind cluster is running (`kubectl get nodes` shows Ready)
- [ ] Pod is in Running state (`kubectl get pods`)
- [ ] Health endpoint returns `{"status":"ok"}`
- [ ] Metrics endpoint returns valid JSON with counters
- [ ] Predictions return correct results
- [ ] Logs show all request activity
- [ ] Load test completes successfully with 0 failures
- [ ] Metrics accurately reflect all requests made
- [ ] Pod automatically recovers after deletion
- [ ] You understand why AI workloads need special observability

---

## 🧹 Cleanup

### Remove Application Resources

```bash
kubectl delete -f k8s/
```

**Expected Output:**
```
deployment.apps "ai-lab-2-2-free" deleted
service "ai-lab-2-2-free" deleted
```

Verify resources are deleted:
```bash
kubectl get pods
kubectl get svc
```

**Expected Output:**
```
No resources found in default namespace.
```

### Delete kind Cluster

```bash
kind delete cluster --name mcp-cluster
```

**Expected Output:**
```
Deleting cluster "mcp-cluster" ...
Deleted nodes: ["mcp-cluster-control-plane"]
```

Verify cluster is deleted:
```bash
kind get clusters
```

**Expected Output:**
```
No kind clusters found.
```

---

## 🔧 Troubleshooting

### Issue: Pod Not Starting

**Symptom:**
```bash
kubectl get pods
# Shows: ImagePullBackOff or CrashLoopBackOff
```

**Solution:**
```bash
# Check pod details
kubectl describe pod -l app=ai-lab-2-2-free

# Common fix: Reload image into kind
kind load docker-image ai-lab-2-2-free:v1 --name mcp-cluster

# Check pod logs
kubectl logs -l app=ai-lab-2-2-free
```

---

### Issue: Port Forward Fails

**Symptom:**
```
error: unable to forward port because pod is not running
```

**Solution:**
```bash
# Ensure pod is running
kubectl get pods

# If not running, wait for it
kubectl wait --for=condition=ready pod -l app=ai-lab-2-2-free

# Try port-forward again
kubectl port-forward deploy/ai-lab-2-2-free 8002:8000
```

---

### Issue: Connection Refused

**Symptom:**
```bash
curl http://localhost:8002/health
# curl: (7) Failed to connect to localhost port 8002: Connection refused
```

**Solution:**
```bash
# Check if port-forward is running
ps aux | grep port-forward

# If not, restart it
kubectl port-forward deploy/ai-lab-2-2-free 8002:8000

# Try a different port if 8002 is in use
kubectl port-forward deploy/ai-lab-2-2-free 8003:8000
curl http://localhost:8003/health
```

---

### Issue: Metrics Show Zeros

**Symptom:**
```json
{"total_requests": 0, "total_predictions": 0, ...}
```

**Solution:**
```bash
# Make some requests first
curl http://localhost:8002/health
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.5]}'

# Check metrics again
curl http://localhost:8002/metrics-lite
```

---

### Issue: Load Generator Fails

**Symptom:**
```
ModuleNotFoundError: No module named 'requests'
```

**Solution:**
```bash
# Install required Python package
pip install requests

# Or use pip3
pip3 install requests

# Run load generator again
python generate_load.py --url http://localhost:8002 --requests 100
```

---

## 📚 Next Steps

### Explore Further

1. **Modify the code** - Try adding new metrics or log fields
2. **Experiment with load** - Test with different request patterns
3. **Practice debugging** - Intentionally break things and fix them
4. **Review logs** - Study the log format and information captured

### Upgrade to PAID Version

The PAID version adds:
- OpenTelemetry tracing for distributed systems
- Metrics export to OpenTelemetry Collector
- Histogram-based latency tracking
- Production-ready resource management
- Namespace isolation

### Additional Resources

- FastAPI documentation: https://fastapi.tiangolo.com/
- Kubernetes logging: https://kubernetes.io/docs/concepts/cluster-administration/logging/
- Observability best practices for ML: Research OpenTelemetry for ML systems

---

## 🎉 Congratulations!

You've successfully completed the FREE version of Lab 2.2!

You now understand:
- ✅ How to add basic observability to AI inference services
- ✅ Why ML workloads need different monitoring than traditional apps
- ✅ How to use logs and metrics to debug latency issues
- ✅ How to deploy and test observable services in Kubernetes

**Keep this lab environment** for future experimentation, or **clean it up** using the cleanup steps above.

Happy learning! 🚀📊
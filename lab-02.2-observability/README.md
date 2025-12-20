# Lab 02.2 — Observability for AI Inference Services

[![Lab](https://img.shields.io/badge/Lab-02.2-blue.svg)](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-02.2-observability)
[![Chapter](https://img.shields.io/badge/Chapter-2-orange.svg)](https://theopskart.gumroad.com/l/AIAgentsforDevOps)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This lab is part of **Chapter 2** of the eBook **AI Agents for DevOps**.

---

## 🎯 Lab Objective

This lab focuses on introducing **observability** into an AI inference service running on Kubernetes.

You will deploy a simple inference API, expose logs and lightweight metrics, generate load, and observe runtime behavior from an infrastructure perspective.

> This lab builds directly on Chapter-2 concepts: **AI workloads behave differently than traditional applications and must be observed differently.**

---

## 📁 Repository Structure

```
lab-02.2-observability
├── Dockerfile
├── LICENSE
├── README.md
├── app
│   ├── load_generator.py
│   ├── main.py
│   ├── requirements.txt
│   └── tests
│       ├── test_app.py
│       └── test_load_generator.py
├── commands.md
├── k8s
│   ├── deployment.yaml
│   └── service.yaml
├── kind-mcp-cluster.yaml
└── setup.md
```

---

## 🧠 What You Will Learn

By completing this lab, you will understand:

1. **Why AI inference services need observability beyond basic uptime checks**
2. **How to expose logs and metrics directly from an inference service**
3. **How to observe inference behavior inside Kubernetes**
4. **How to generate controlled load against an inference endpoint**
5. **How DevOps engineers validate latency, stability, and behavior of AI workloads**
6. **Why observability should start inside the application, not with external tools**

---

## 📋 Prerequisites

### Operating System

- **Ubuntu 22.04** (EC2, local VM, WSL2, or similar)

### Required Tools

- **Docker**: 24+
- **kind**: Latest version
- **kubectl**: ≥ 1.29
- **Python**: 3.11+
- **Git**: Latest version

> For installation instructions, see [setup.md](setup.md)

---

## 🏗️ Application Overview

The FastAPI service exposes:

| Endpoint | Purpose |
|----------|---------|
| `/health` | Liveness and startup verification |
| `/predict` | Simulated inference endpoint |
| `/metrics-lite` | Lightweight observability metrics |

> The inference logic is intentionally simple to keep the focus on **observability and infrastructure behavior**, not ML complexity.

---

## 📁 Files You Should Care About

| File/Directory | Purpose |
|----------------|---------|
| `Dockerfile` | Container definition for inference service |
| `app/main.py` | FastAPI-based inference service with observability |
| `app/load_generator.py` | Load testing script for inference |
| `app/requirements.txt` | Python dependencies |
| `app/tests/` | Unit tests for the service |
| `k8s/deployment.yaml` | Kubernetes deployment configuration |
| `k8s/service.yaml` | Kubernetes service configuration |
| `kind-mcp-cluster.yaml` | Kind cluster configuration |
| `commands.md` | Common kubectl/docker commands reference |
| `README.md` | This file (single source of truth) |

---

## 🚀 Setup Instructions

### Step 1: Create Kubernetes Cluster

```bash
kind create cluster --config kind-mcp-cluster.yaml
kubectl get nodes
```

**Expected output:**
```
NAME                        STATUS   ROLES           AGE   VERSION
mcp-cluster-control-plane   Ready    control-plane   1m    v1.x.x
```

---

### Step 2: Build Docker Image

```bash
docker build -t ai-lab-2-2:v1 .
```

---

### Step 3: Load Image into kind

```bash
kind load docker-image ai-lab-2-2:v1 --name mcp-cluster
```

---

### Step 4: Deploy to Kubernetes

```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get svc ai-lab-2-2
```

**Ensure the pod is in `Running` state:**

```bash
kubectl wait --for=condition=ready pod -l app=ai-lab-2-2 --timeout=300s
```

---

## 🔍 Accessing the Service

### Port Forward

```bash
kubectl port-forward deploy/ai-lab-2-2 8002:8000
```

> Leave this running in a separate terminal.

---

## ✅ Testing the Service

### Health Check

```bash
curl http://localhost:8002/health
```

**Expected response:**
```json
{
  "status": "ok",
  "version": "v1"
}
```

---

### Metrics Endpoint

```bash
curl http://localhost:8002/metrics-lite
```

**Example output:**
```json
{
  "uptime_ms": 1766243858512,
  "cpu_simulated_ms": 25,
  "requests_total_estimate": 100
}
```

**What these metrics tell you:**
- **uptime_ms**: How long the service has been running
- **cpu_simulated_ms**: Simulated CPU cost per request
- **requests_total_estimate**: Approximate request count

---

### Inference Request

```bash
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[1.0,2.0,3.5]}'
```

**Response:**
```json
{
  "prediction": 6.5
}
```

---

## 📊 Viewing Logs

### Stream Logs in Real-Time

```bash
kubectl logs -f deploy/ai-lab-2-2
```

**Example log output:**
```
INFO:lab-2.2:Health check called
INFO:lab-2.2:Prediction requested with [1.0, 2.0, 3.5]
INFO:lab-2.2:Prediction completed: 6.5
```

---

### Filter Logs

```bash
# See only prediction logs
kubectl logs deploy/ai-lab-2-2 | grep "Prediction"

# See only errors
kubectl logs deploy/ai-lab-2-2 | grep "ERROR"

# Get last 50 lines
kubectl logs deploy/ai-lab-2-2 --tail=50
```

---

## 🔥 Load Testing with load_generator.py

The load generator simulates concurrent inference requests and helps you observe latency, logging behavior, and service stability.

### Run Load Generator Locally

**Ensure port-forward is running**, then:

```bash
python3 app/load_generator.py \
  --url http://localhost:8002/predict \
  --count 100
```

**What it does:**
- Sends repeated inference requests
- Measures request latency
- Helps validate service behavior under load

**While running, observe:**
```bash
# In another terminal - watch logs
kubectl logs -f deploy/ai-lab-2-2

# Watch metrics change
watch -n 1 curl -s http://localhost:8002/metrics-lite
```

---

## 🧪 Running Tests

### Application Tests

```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

**Expected output:**
```
====== test session starts ======
collected X items

tests/test_app.py ....
tests/test_load_generator.py ...

====== X passed in X.XXs ======
```

---

## 📈 Understanding the Observability Signals

### Logs
- **Show what happened**
- Useful for debugging inference flow
- Collected automatically by Kubernetes
- Critical for root cause analysis

### Metrics
- **Show how often and how long**
- Help detect performance degradation
- Represent the starting point before Prometheus or OpenTelemetry
- Enable trend analysis over time

---

## 🧹 Cleanup

```bash
kubectl delete -f k8s/
kind delete cluster --name mcp-cluster
docker system prune -f
```

---

## 💡 Why This Lab Exists in Chapter-2

This lab demonstrates the operational reality of AI inference services:

| Reality | Implication |
|---------|-------------|
| AI workloads are compute-heavy | Need CPU/memory metrics |
| Latency matters more than throughput alone | Need request-level timing |
| Logs and metrics must exist before scaling | Observability-first approach |
| Kubernetes is the control plane for AI operations | Standard tools apply |

---

## 🎯 Key Takeaways

1. **Observability must be built into the application**, not bolted on later
2. **Logs provide context**, metrics provide trends
3. **AI inference has predictable costs** that should be observable
4. **Load testing reveals behavior** that health checks miss
5. **Simple metrics are better than no metrics**

---

## ➡️ What This Lab Sets Up

This lab sets the foundation for:

- **Advanced observability** (Prometheus, Grafana)
- **Distributed tracing** (OpenTelemetry, Jaeger)
- **GPU-level monitoring** (nvidia-smi integration)
- **Production AI platforms**

---

## 🔧 Troubleshooting

### Port Forward Fails

```bash
# Check if service exists
kubectl get svc ai-lab-2-2

# Check if pod is running
kubectl get pods -l app=ai-lab-2-2

# Try different local port
kubectl port-forward deploy/ai-lab-2-2 8003:8000
```

### Load Generator Connection Refused

```bash
# Ensure port-forward is running
kubectl port-forward deploy/ai-lab-2-2 8002:8000

# Test endpoint manually first
curl http://localhost:8002/health
```

### No Logs Appearing

```bash
# Check pod status
kubectl get pods

# Describe pod for events
kubectl describe pod -l app=ai-lab-2-2

# Check if container is running
kubectl get pods -o wide
```

### Tests Failing

```bash
# Ensure correct Python version
python3 --version  # Should be 3.11+

# Install dependencies
pip install -r app/requirements.txt

# Run tests with verbose output
pytest -v
```

---

## ✅ Success Criteria

You have successfully completed this lab if:

- ✅ Pod is running and healthy
- ✅ All three endpoints (`/health`, `/predict`, `/metrics-lite`) work
- ✅ Logs show inference requests
- ✅ Load generator completes successfully
- ✅ You understand why observability matters for AI workloads

---

## 📦 Repository Location

This lab lives here:

👉 [github.com/toktechteam/ai_agents_for_devops/tree/main/lab-02.2-observability](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-02.2-observability)

---

## 📚 eBook Reference

This lab is explained in detail in **Chapter 2** of the eBook:

👉 **AI Agents for DevOps**  
[theopskart.gumroad.com/l/AIAgentsforDevOps](https://theopskart.gumroad.com/l/AIAgentsforDevOps)

---

## 📝 License

This repository uses a **dual license** structure:

- **📖 Educational Content** (documentation, tutorials, explanations):  
  Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)  
  Free for personal learning and non-commercial educational use.

- **💻 Code** (scripts, implementations, configurations):  
  Licensed under [MIT License](https://opensource.org/licenses/MIT)  
  Free to use in both personal and commercial projects.

**Attribution:**  
When sharing or adapting this content, please credit:
```
Original content from "AI Agents for DevOps" by TokTechTeam
https://theopskart.gumroad.com/l/AIAgentsforDevOps
```

For full license details and commercial use inquiries, see [LICENSE](../LICENSE).

---

## 🤝 Contributing

Contributions are welcome! However, please note:
- This content is tied to a commercial eBook
- Contributions should align with the educational goals
- All contributions will be licensed under the same terms

Before contributing:
1. Read the [LICENSE](../LICENSE) file
2. Open an issue to discuss your proposed changes
3. Submit a pull request

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/toktechteam/ai_agents_for_devops/issues)
- **eBook**: [AI Agents for DevOps](https://theopskart.gumroad.com/l/AIAgentsforDevOps)
- **Commercial Licensing**: toktechteam@gmail.com/theopskart@gmail.com

---

## ⭐ Acknowledgments

This lab is part of the comprehensive **AI Agents for DevOps** course, designed to teach practical AI implementation in production environments.

If you find this lab helpful, consider:
- ⭐ Starring this repository
- 📖 Getting the full eBook for deeper insights
- 🔄 Sharing with your team

---

Copyright © 2024 TokTechTeam. See [LICENSE](../LICENSE) for details.
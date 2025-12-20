# Lab 01.3 — AI/ML Fundamentals: Operating Reality on Kubernetes

[![Lab](https://img.shields.io/badge/Lab-01.3-blue.svg)](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-01.3-kubernetes-reality)
[![Chapter](https://img.shields.io/badge/Chapter-1-orange.svg)](https://theopskart.gumroad.com/l/AIAgentsforDevOps)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This lab is part of **Chapter 1** of the eBook **AI Agents for DevOps**.

---

## 🎯 Why This Lab Exists (Read This First)

In **Lab 1.1**, you learned that ML inference behaves differently from traditional APIs (startup time, memory, latency).

In **Lab 1.2**, you compared API-based models vs self-hosted models and understood cost, scaling, and latency trade-offs.

👉 **This lab (1.3)** answers a different question:

> **"What actually changes when I run an AI inference service on Kubernetes?"**

**Spoiler:**  
Almost nothing at first — and **that's the lesson**.

This lab intentionally looks boring so you can clearly see:

- What Kubernetes treats as normal
- What AI workloads don't change
- What problems will only appear later at scale

---

## 🎓 Lab Objective

Deploy a simple ML-style inference API on Kubernetes and observe:

- How Kubernetes sees an AI service
- How health checks behave
- How inference latency behaves
- Why AI infra problems are not obvious on Day-1

> This lab is about **operational reality**, not model complexity.

---

## 📚 What You Will Learn

By completing this lab, you will understand:

1. **AI inference pods are just pods to Kubernetes**
2. **Health checks don't reveal model complexity**
3. **Latency can look "fine" even when infra is wrong**
4. **Why many AI failures happen weeks later, not on day one**
5. **Why DevOps engineers must think beyond "it works"**

---

## 📋 Prerequisites

### Target Environment

- **Cloud VM**: EC2 / VM / Bare metal
- **OS**: Ubuntu 22.04 LTS
- **Instance Type**: t3.medium (minimum)
- **RAM**: 4 GB (this lab intentionally keeps it light)
- **Runtime**: Docker + Kind (local Kubernetes)

---

## 🛠️ Tool Installation (Mandatory)

### Step 1: System Updates and Basic Tools

```bash
sudo apt update && sudo apt upgrade -y

sudo apt install -y curl wget git build-essential software-properties-common \
    apt-transport-https ca-certificates gnupg lsb-release net-tools tmux \
    vim nano htop jq unzip
```

---

### Step 2: Install Docker (Latest)

```bash
# Remove old Docker packages
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
    sudo apt remove $pkg 2>/dev/null || true
done

# Install prerequisites
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
```

---

### Step 3: Install kubectl (Latest)

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify installation
kubectl version --client
```

---

### Step 4: Install Kind (Local Kubernetes)

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.30.0/kind-linux-amd64

chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Verify installation
kind version
```

---

## 🏗️ Lab Architecture (Conceptual)

```
Client
  |
  |  (HTTP)
  v
Kubernetes Service
  |
  v
AI Inference Pod (FastAPI)
  |
  v
Simple Model Logic (sum of numbers + latency)
```

**Key Points:**
- No GPUs
- No autoscaling
- No tricks

> **This is intentional.**

---

## 📁 Files You Should Care About

| File | Purpose |
|------|---------|
| `Dockerfile` | Container definition for AI service |
| `app.py` | FastAPI-based inference service |
| `requirements.txt` | Python dependencies |
| `k8s/deployment.yaml` | Kubernetes deployment configuration |
| `k8s/service.yaml` | Kubernetes service configuration |
| `README.md` | This file (single source of truth) |

---

## 🚀 How to Run the Lab

### 1. Create Kubernetes Cluster

```bash
kind create cluster --name ai-lab
kubectl get nodes
```

**Expected output:**
```
NAME                   STATUS   ROLES           AGE   VERSION
ai-lab-control-plane   Ready    control-plane   1m    v1.x.x
```

---

### 2. Build and Load Image into Kind

```bash
# Build the Docker image
docker build -t ai-lab:latest .

# Load image into Kind cluster
kind load docker-image ai-lab:latest --name ai-lab
```

---

### 3. Deploy to Kubernetes

```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get svc
```

**Wait for pod to be ready:**
```bash
kubectl wait --for=condition=ready pod -l app=ai-lab --timeout=300s
```

---

## ✅ Verification Steps (Very Important)

### 1. Pod Health

```bash
kubectl logs pod/<pod-name>
```

You should see:
```
Application startup complete
Uvicorn running on http://0.0.0.0:8000
GET /health 200 OK
```

This confirms:
- ✅ App started normally
- ✅ Kubernetes health probes work
- ✅ No AI-specific behavior yet

---

### 2. Port Forward

```bash
kubectl port-forward svc/ai-lab 8000:8000
```

Leave this running in a separate terminal.

---

### 3. Send Inference Request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[1,2,3,4,5]}'
```

**Expected output:**
```json
{
  "prediction": 15.0,
  "model_latency_ms": 50
}
```

---

## 💡 What This Lab Is Teaching You (The Real Lesson)

At this stage:

- ✅ Kubernetes is happy
- ✅ Health checks are green
- ✅ Latency looks fine
- ✅ Everything looks production-ready

👉 **This is the trap.**

---

## 🎯 Key Insight

**Kubernetes cannot tell the difference between:**

- A calculator
- An ML model
- A 40GB LLM (until it crashes)

**This is why:**

- AI systems pass CI/CD
- Pass readiness probes
- Pass load tests
- **And still fail in real production**

---

## 📊 Why This Lab Matters in Chapter 1

This lab completes Chapter 1's promise:

| Lab | What You Learned |
|-----|------------------|
| **1.1** | AI inference ≠ normal API |
| **1.2** | API vs self-hosted trade-offs |
| **1.3** | Kubernetes does not save you |

You now understand why AI workloads break infra assumptions **later**, not immediately.

---

## ✅ Success Criteria

You have completed this lab successfully if:

- ✅ Pod is running
- ✅ `/health` returns 200
- ✅ `/predict` works
- ✅ **You feel "this looks too normal"**

> That feeling is **exactly correct**.

---

## 🧹 Cleanup

```bash
# Delete the Kind cluster
kind delete cluster --name ai-lab

# Clean up Docker resources
docker system prune -f
```

---

## ➡️ What Comes Next

You've now completed all Chapter 1 labs and understand:

- **Lab 1.1**: Why ML services behave differently
- **Lab 1.2**: API vs self-hosted operational trade-offs
- **Lab 1.3**: Why Kubernetes doesn't reveal AI problems early

**Next:** Move to **Chapter 2** to explore advanced orchestration patterns and real-world scaling challenges.

---

## 🔧 Troubleshooting

### Kind Cluster Won't Start

```bash
# Check Docker is running
docker ps

# Delete and recreate cluster
kind delete cluster --name ai-lab
kind create cluster --name ai-lab
```

### Image Not Found in Kind

```bash
# Verify image exists
docker images | grep ai-lab

# Reload image into Kind
kind load docker-image ai-lab:latest --name ai-lab
```

### Pod Stuck in Pending State

```bash
# Check pod events
kubectl describe pod <pod-name>

# Check node resources
kubectl top nodes
```

### Port Forward Not Working

```bash
# Ensure service exists
kubectl get svc

# Check pod is running
kubectl get pods

# Try different local port
kubectl port-forward svc/ai-lab 8080:8000
```

---

## 📦 Repository Location

This lab lives here:

👉 [github.com/toktechteam/ai_agents_for_devops/tree/main/lab-01.3-kubernetes-reality](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-01.3-ai-ml-fundamentals)

---

## 📚 eBook Reference

This lab is explained in detail in **Chapter 1** of the eBook:

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
- **Commercial Licensing**: theopskart@gmail.com/toktechteam@gmail.com

---

## ⭐ Acknowledgments

This lab is part of the comprehensive **AI Agents for DevOps** course, designed to teach practical AI implementation in production environments.

If you find this lab helpful, consider:
- ⭐ Starring this repository
- 📖 Getting the full eBook for deeper insights
- 🔄 Sharing with your team

---

Copyright © 2024 TokTechTeam. See [LICENSE](../LICENSE) for details.
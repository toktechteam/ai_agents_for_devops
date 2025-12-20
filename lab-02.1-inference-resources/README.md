# Lab 02.1 — Inference Resource Reality

[![Lab](https://img.shields.io/badge/Lab-02.1-blue.svg)](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-02.1-inference-resource-reality)
[![Chapter](https://img.shields.io/badge/Chapter-2-orange.svg)](https://theopskart.gumroad.com/l/AIAgentsforDevOps)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Chapter 2 – Understanding the AI Stack from an Infrastructure Perspective**

This lab is part of **Chapter 2** of the eBook **AI Agents for DevOps**.

---

## 🎯 Lab Objective

This lab demonstrates a critical but non-obvious reality of AI inference workloads:

> **AI inference cost is driven by fixed resources (CPU / memory), not request volume.**

You will deploy a simple inference API and observe how:

- CPU is consumed per request
- Memory stays fixed
- Kubernetes treats AI inference pods as stateful, resource-heavy services
- Scaling assumptions from traditional microservices start to break

This lab is intentionally simple at the model level so that **infrastructure behavior is impossible to ignore**.

---

## ❗ What This Lab Is NOT

- ❌ Not about ML accuracy
- ❌ Not about training models
- ❌ Not about advanced algorithms
- ❌ Not about Python tricks

> The "model" is intentionally trivial.  
> The learning is in the **infrastructure behavior**, not the math.

---

## 🧠 What You Will Learn

By the end of this lab, you will clearly understand:

1. **Why AI inference has fixed per-pod resource cost**
2. **Why CPU usage grows linearly with requests**
3. **Why memory does not scale with traffic**
4. **Why AI inference pods behave more like pets than cattle**
5. **Why naive horizontal auto-scaling fails for AI workloads**

---

## 📋 Prerequisites

### Target Environment

- **OS**: Ubuntu 22.04 LTS
- **Instance type**: t3.medium (minimum)
- **RAM**: 4 GB minimum
- **Internet access**: Required
- **Tools**: Docker, kubectl, kind

---

## 🛠️ Step-by-Step Setup

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
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
```

---

### Step 3: Install kubectl

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s \
https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify installation
kubectl version --client
```

---

### Step 4: Install kind (Kubernetes in Docker)

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.30.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Verify installation
kind version
```

---

### Step 5: Create Kubernetes Cluster

```bash
kind create cluster --name ai-lab-cluster
kubectl get nodes
```

**Expected output:**
```
NAME                           STATUS   ROLES           AGE   VERSION
ai-lab-cluster-control-plane   Ready    control-plane   1m    v1.x.x
```

---

## 📁 Files You Should Care About

| File | Purpose |
|------|---------|
| `Dockerfile` | Container definition for inference service |
| `app/main.py` | FastAPI-based inference service |
| `app/load_generator.py` | Load testing script |
| `requirements.txt` | Python dependencies |
| `k8s/deployment.yaml` | Kubernetes deployment configuration |
| `k8s/service.yaml` | Kubernetes service configuration |
| `README.md` | This file (single source of truth) |

---

## 🚀 Deployment Steps

### Step 6: Build and Deploy the Inference Service

```bash
# Build Docker image
docker build -t ai-lab-2-1:latest .

# Load image into Kind cluster
kind load docker-image ai-lab-2-1:latest --name ai-lab-cluster

# Deploy to Kubernetes
kubectl apply -f k8s/
```

**Verify deployment:**

```bash
kubectl get pods
kubectl get svc
```

Wait for the pod to be ready:

```bash
kubectl wait --for=condition=ready pod -l app=ai-lab-2-1 --timeout=300s
```

---

### Step 7: Access the Service

```bash
kubectl port-forward svc/ai-lab-2-1 8000:8000
```

> Leave this running in a separate terminal.

---

## ✅ Testing the Service

### Step 8: Verify Health

```bash
curl http://localhost:8000/health
```

**Expected output:**

```json
{
  "status": "ok",
  "mode": "standard",
  "cpu_burn_ms": 30
}
```

---

### Step 9: Run Inference Requests

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[1.0,2.0,3.5]}'
```

**Expected output:**

```json
{
  "prediction": 6.5,
  "cpu_burn_ms": 30
}
```

---

### Step 10: Generate Load

Run from the EC2 host (not inside the container):

```bash
python3 app/load_generator.py \
  --url http://localhost:8000/predict \
  --requests 200
```

This simulates sustained inference traffic hitting the service.

**While load is running, monitor resources:**

```bash
# In another terminal
kubectl top pods
watch kubectl top pods
```

---

## 📊 What You Should Observe

| Metric | Behavior | Why This Matters |
|--------|----------|------------------|
| **CPU usage** | Increases with requests | Each inference has compute cost |
| **Memory usage** | Remains constant | Model loaded once, stays in memory |
| **Pod scaling** | Does not auto-scale | No HPA configured (intentional) |
| **Request cost** | Fixed per request | Predictable but unavoidable |
| **Pod restart** | Resets all state | Expensive in real AI systems |

> This mirrors real AI inference services, **not traditional APIs**.

---

## 🧠 Key Takeaways

1. **AI inference cost is resource-bound, not traffic-bound**
2. **Memory is allocated upfront** (model loading)
3. **CPU burn is predictable and unavoidable**
4. **Killing pods is expensive in real AI systems**
5. **Auto-scaling needs prediction and pre-warming**

---

## 💡 The Critical Insight

**Traditional microservices:**
- Stateless
- CPU scales with traffic, memory stays low
- Auto-scaling works out of the box
- Cheap to restart

**AI inference services:**
- Stateful (model in memory)
- CPU scales with traffic, memory stays high and fixed
- Auto-scaling requires warm-up time
- Expensive to restart (model reload)

---

## ✅ Success Criteria

You have successfully completed this lab if:

- ✅ Service starts and passes health checks
- ✅ Predictions work correctly
- ✅ Load generation increases CPU usage
- ✅ You understand **why AI inference breaks microservice assumptions**

---

## 🧹 Cleanup

```bash
# Delete the Kind cluster
kind delete cluster --name ai-lab-cluster

# Clean up Docker resources
docker system prune -f
```

---

## 🔧 Troubleshooting

### Pod Not Starting

```bash
# Check pod logs
kubectl logs -l app=ai-lab-2-1

# Check pod events
kubectl describe pod -l app=ai-lab-2-1
```

### Load Generator Fails

```bash
# Ensure port-forward is running
kubectl port-forward svc/ai-lab-2-1 8000:8000

# Test health endpoint first
curl http://localhost:8000/health

# Install Python dependencies if needed
pip3 install requests
```

### Can't See Resource Usage

```bash
# Install metrics-server for Kind
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Patch for Kind compatibility
kubectl patch deployment metrics-server -n kube-system --type='json' \
  -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'

# Wait for metrics to be available (takes ~1 minute)
kubectl top nodes
```

### Image Not Loading into Kind

```bash
# Verify image exists
docker images | grep ai-lab-2-1

# Reload image
kind load docker-image ai-lab-2-1:latest --name ai-lab-cluster

# Restart the deployment
kubectl rollout restart deployment ai-lab-2-1
```

---

## ➡️ What Comes Next

After completing this lab, you understand the **resource reality** of AI inference.

**Next steps:**
- **Lab 2.2**: Advanced resource management and optimization
- **Lab 2.3**: Autoscaling strategies for AI workloads

These build on the foundation you just established.

---

## 📦 Repository Location

This lab lives here:

👉 [github.com/toktechteam/ai_agents_for_devops/tree/main/lab-02.1-inference-resource](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-02.1-inference-resource)

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
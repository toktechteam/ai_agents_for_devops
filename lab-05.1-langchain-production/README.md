# Lab 05.1 — Deploying LangChain in Production (Agent Perspective)

[![Lab](https://img.shields.io/badge/Lab-05.1-blue.svg)](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-05.1-langchain-production)
[![Chapter](https://img.shields.io/badge/Chapter-5-orange.svg)](https://theopskart.gumroad.com/l/AIAgentsforDevOps)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This lab is part of **Chapter 5** of the eBook **AI Agents for DevOps**.

---

## 🎯 Purpose of This Lab

This lab is **not about running Python files or learning LangChain syntax**.

This lab teaches **how a production AI agent behaves**, how it:

- Plans actions
- Uses tools safely
- Maintains memory
- Tracks cost
- Exposes observability

> If you finish this lab correctly, you will **think differently about automation**.

---

## 🧠 What You Are Building

A **LangChain-based Incident Responder Agent** that:

- Accepts alerts via API
- Creates an investigation plan
- Executes safe tools (not raw kubectl)
- Maintains memory between requests
- Tracks token cost
- Exposes Prometheus metrics

**This is how real AI agents run in production.**

---

## ❗ Important Rule (Read This First)

- ❌ You do NOT run Python files directly
- ❌ You do NOT run unit tests manually
- ✅ You test the agent **only via API**

> This is a **service-based lab**, not a script-based lab.

---

## 🏗️ Architecture Overview

### How This Lab Runs

```
Client (curl)
   ↓
LangChain API Service
   ↓
Agent Reasoning Engine
   ↓
Safe Tool Layer
   ↓
Memory + Cost Tracking
   ↓
Metrics (Prometheus)
```

### Component Layers

```
┌─────────────────────────────────────────────────────┐
│              FastAPI REST Endpoint                  │
│              POST /investigate                      │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│           LangChain Agent Core                      │
│  - Receives alert                                   │
│  - Generates investigation plan                     │
│  - Decides tool sequence dynamically                │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│              Safe Tool Layer                        │
│  - check_pods (simulated)                          │
│  - fetch_metrics (simulated)                       │
│  - check_logs (simulated)                          │
│  - NO direct kubectl access                        │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│         Memory + Cost Tracking                      │
│  - In-memory state (Redis-like)                    │
│  - Token counting                                   │
│  - USD cost calculation                             │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│        Prometheus Metrics Endpoint                  │
│        GET /metrics                                 │
│  - agent_requests_total                             │
│  - agent_tokens_total                               │
│  - agent_average_cost                               │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
lab-05.1-langchain-production/
├── README.md                   ← This file
├── setup.md                    ← Detailed setup guide
├── kind-cluster.yaml           ← Kind cluster configuration
├── Dockerfile                  ← Container image definition
├── app/
│   ├── main.py                 ← FastAPI service
│   ├── agent.py                ← LangChain agent logic
│   ├── tools.py                ← Safe tool implementations
│   ├── memory.py               ← Memory management
│   ├── cost.py                 ← Token and cost tracking
│   ├── metrics.py              ← Prometheus metrics
│   └── requirements.txt        ← Python dependencies
└── k8s/
    ├── namespace.yaml          ← Namespace: langchain
    ├── deployment.yaml         ← Agent deployment
    └── service.yaml            ← ClusterIP service
```

---

## 🚀 Quick Start Guide

### Step 1: Build and Deploy

**Build the Docker image:**
```bash
docker build -t langchain-agent:v1 .
```

**Create Kind cluster:**
```bash
kind create cluster --config kind-cluster.yaml
```

**Load image into Kind:**
```bash
kind load docker-image langchain-agent:v1 --name kind
```

**Deploy to Kubernetes:**
```bash
kubectl apply -f k8s/
```

**Verify deployment:**
```bash
kubectl get pods -n langchain
kubectl get svc -n langchain
```

---

### Step 2: Expose the Service

```bash
kubectl -n langchain port-forward svc/langchain 8000:8000
```

**Expected output:**
```
Forwarding from 127.0.0.1:8000 -> 8000
```

> Leave this running in a separate terminal.

---

## 🧪 Testing the Agent

### Test #1: Agent Reasoning & Planning

**Send a High CPU Alert:**
```bash
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"alert_type":"high_cpu","service":"payment-api"}'
```

**Actual Output:**
```json
{
  "alert": {
    "alert_type": "high_cpu",
    "service": "payment-api"
  },
  "plan": [
    "check_pods",
    "fetch_metrics"
  ],
  "steps": [
    {
      "step": "check_pods",
      "result": "[FAKE] pods for payment-api: payment-api-123 payment-api-456"
    },
    {
      "step": "fetch_metrics",
      "result": "[FAKE] metrics: latency_p95=430ms cpu=87%"
    }
  ],
  "cost": {
    "tokens": 101,
    "usd": 0.000202
  },
  "memory": {
    "last_service": "payment-api"
  }
}
```

**✅ What You Learned:**

- The agent created a **plan** (`check_pods` → `fetch_metrics`)
- This is **not if/else logic**
- The agent **decides steps dynamically**
- This is the core difference between **scripts and agents**

---

### Test #2: Tool Execution (Safety Model)

Look at this section from the previous output:

```json
"steps": [
  {
    "step": "check_pods",
    "result": "[FAKE] pods..."
  },
  {
    "step": "fetch_metrics",
    "result": "[FAKE] metrics..."
  }
]
```

**✅ What You Learned:**

- Tools are **abstracted**
- The agent does **not run real kubectl**
- This prevents:
  - Accidental deletions
  - Security risks
  - Unsafe automation
- **This is mandatory in production agent systems**

---

### Test #3: Memory Persistence

**Send another alert for the same service:**
```bash
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"alert_type":"high_latency","service":"payment-api"}'
```

**Actual Output:**
```json
{
  "alert": {
    "alert_type": "high_latency",
    "service": "payment-api"
  },
  "plan": [
    "fetch_metrics",
    "check_logs"
  ],
  "steps": [
    {
      "step": "fetch_metrics",
      "result": "[FAKE] metrics: latency_p95=430ms cpu=87%"
    },
    {
      "step": "check_logs",
      "result": "[FAKE] logs for payment-api: INFO stable system"
    }
  ],
  "cost": {
    "tokens": 88,
    "usd": 0.000176
  },
  "memory": {
    "last_service": "payment-api"
  }
}
```

**✅ What You Learned:**

- The plan **changed based on alert type**
- The agent **remembered the service**
- This is **stateful behavior**
- **This is why agents need Redis/Postgres in real systems**

---

### Test #4: Cost Awareness (Critical)

Look at the cost section from both outputs:

**First request:**
```json
"cost": {
  "tokens": 101,
  "usd": 0.000202
}
```

**Second request:**
```json
"cost": {
  "tokens": 88,
  "usd": 0.000176
}
```

**✅ What You Learned:**

- Every decision **costs money**
- **Tokens = cloud bill**
- Agents must be **cost-observable**
- **This is why FinOps matters for AI**

---

### Test #5: Observability (Production Requirement)

**Fetch Prometheus metrics:**
```bash
curl http://localhost:8000/metrics
```

**Look for these metrics:**
```
# HELP agent_requests_total Total number of investigation requests
# TYPE agent_requests_total counter
agent_requests_total 2.0

# HELP agent_tokens_total Total tokens consumed
# TYPE agent_tokens_total counter
agent_tokens_total 189.0

# HELP agent_average_cost Average cost per request in USD
# TYPE agent_average_cost gauge
agent_average_cost 0.000189
```

**✅ What You Learned:**

- Agents expose **infra-grade metrics**
- **Tokens are first-class metrics**
- Cost can be **alerted and budgeted**
- **AI systems must be monitored like Kubernetes**

---

## 🚫 What You Should NOT Do (Common Mistakes)

| Action | Why It's Wrong |
|--------|----------------|
| `python chain.py` | This is not a script |
| Running tests manually | Not the learning goal |
| Direct kubectl calls | Breaks safety model |
| Editing agent logic | Covered in later labs |
| Running without API | Misses production patterns |

---

## 🎓 Key Learning Outcomes

After this lab, you understand:

| Concept | Traditional Approach | Agent Approach |
|---------|---------------------|----------------|
| **Execution** | Script (if/else) | Planning (reasoning) |
| **Tools** | Direct commands | Abstracted & safe |
| **State** | Stateless | Stateful (memory) |
| **Cost** | Not tracked | Token-level tracking |
| **Observability** | Logs only | Metrics + logs |
| **Testing** | Unit tests | API integration |

### Core Principles Learned

✅ **Agent ≠ script**  
✅ **Planning ≠ hardcoding**  
✅ **Tools must be sandboxed**  
✅ **Memory creates state**  
✅ **Tokens create cost**  
✅ **Observability is mandatory**  
✅ **APIs are the testing surface**

> **This is production-grade agent thinking.**

---

## 💰 Cost Analysis

### Token Economics

**Per investigation:**
- Average: 90-100 tokens
- Cost: ~$0.0002 USD (GPT-3.5 equivalent pricing)

**Monthly cost (1000 alerts):**
```
1000 requests × 100 tokens = 100,000 tokens
100,000 tokens × $0.000002/token = $0.20

Infrastructure (1 pod): ~$5/month
Total: ~$5.20/month
```

**Cost optimization strategies:**
- Cache tool results (reduce tokens by 30-50%)
- Use smaller models for simple decisions
- Implement request batching
- Set token limits per investigation

---

## 🔧 Troubleshooting

### Issue: Agent Not Responding

**Check pod status:**
```bash
kubectl get pods -n langchain
kubectl logs -n langchain -l app=langchain
```

**Common causes:**
- Port-forward not running
- Image not loaded into Kind
- Service not exposed

**Solution:**
```bash
# Reload image
kind load docker-image langchain-agent:v1 --name <cluster-name>

# Restart port-forward
kubectl -n langchain port-forward svc/langchain 8000:8000
```

---

### Issue: Metrics Not Available

**Check metrics endpoint:**
```bash
curl http://localhost:8000/health
```

**If health works but metrics don't:**
```bash
# Check if Prometheus client is installed
kubectl exec -n langchain -it <pod-name> -- pip list | grep prometheus
```

---

### Issue: Memory Not Persisting

**Expected behavior:**
- Memory is **in-process** in this lab
- Restarting the pod **clears memory**
- This is intentional for learning

**For production:**
- Use Redis for distributed memory
- Use PostgreSQL for persistent memory
- Implement memory snapshots

---

## 🧹 Cleanup

### Remove Kubernetes Resources

```bash
kubectl delete namespace langchain
```

### Delete Kind Cluster

```bash
kind delete cluster --name kind
```

### Clean Docker Images

```bash
docker rmi langchain-agent:v1
docker system prune -f
```

---

## 📚 Next Steps

### Extend This Lab

**1. Add Real Tools:**
```python
# Replace fake tools with actual implementations
def check_pods(service):
    # Actually call Kubernetes API
    pods = kubernetes_client.list_pods(label=f"app={service}")
    return [pod.name for pod in pods]
```

**2. Implement Persistent Memory:**
```python
# Use Redis for distributed memory
from redis import Redis

class PersistentMemory:
    def __init__(self):
        self.redis = Redis(host='redis', port=6379)
```

**3. Add Authentication:**
```python
# Protect the API endpoint
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/investigate")
async def investigate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Validate token
    ...
```

**4. Implement Cost Limits:**
```python
# Prevent runaway costs
MAX_TOKENS_PER_REQUEST = 500
MAX_USD_PER_DAY = 10.0

if request_tokens > MAX_TOKENS_PER_REQUEST:
    raise HTTPException(status_code=429, detail="Token limit exceeded")
```

---

## ✅ Lab Status

After completing this lab:

- ✔ Lab 5.1 completed
- ✔ Agent behavior validated
- ✔ Cost tracked
- ✔ Memory verified
- ✔ Metrics exposed

**You are now ready for multi-agent systems and workflows.**

---

## 📦 Repository Location

This lab lives here:

👉 [github.com/toktechteam/ai_agents_for_devops/tree/main/lab-05.1-langchain-production](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-05.1-langchain-production)

---

## 📚 eBook Reference

This lab is explained in detail in **Chapter 5** of the eBook:

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
- **Email**: toktechteam@gmail.com / theopskart@gmail.com
- **Commercial Licensing**: Contact us via email

---

## ⭐ Acknowledgments

This lab is part of the comprehensive **AI Agents for DevOps** course, designed to teach practical AI implementation in production environments.

If you find this lab helpful, consider:
- ⭐ Starring this repository
- 📖 Getting the full eBook for deeper insights
- 🔄 Sharing with your team

---

## 📖 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangChain Agents Guide](https://python.langchain.com/docs/modules/agents/)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangSmith for Agent Observability](https://docs.smith.langchain.com/)

---

Copyright © 2025 TokTechTeam. See [LICENSE](../LICENSE) for details.
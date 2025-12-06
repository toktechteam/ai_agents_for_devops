# Lab 5.1 FREE Version – Production-Style LangChain Agent Patterns
## Learning LangChain Operational Patterns Without the Complexity

---

## 🎯 What You Will Learn

### Core Concepts

By completing this lab, you will master:

1. **LangChain Production Patterns** - Without needing LangChain installed:
   - **Chain-style execution**: Multi-step agent workflows
   - **Tool orchestration**: Sequential and parallel execution
   - **State management**: Conversation and decision history
   - **Cost tracking**: Token usage and financial monitoring
   - **Metrics exposure**: Prometheus-ready observability

2. **Production Agent Deployment** - Real-world operational patterns:
   - **Horizontal scaling**: Multi-replica deployments
   - **Health monitoring**: Readiness and liveness probes
   - **Resource management**: CPU/memory limits for agents
   - **Autoscaling**: HPA based on load
   - **Zero-downtime**: Rolling updates

3. **Infrastructure Economics** - Cost-aware ML systems:
   - **Token tracking**: Per-request token consumption
   - **Cost calculation**: Real-time cost per investigation
   - **Budget management**: Cost limits and alerting
   - **Optimization strategies**: Reducing operational costs

4. **Agent Chain Architecture** - Multi-step reasoning:
   - **Planner**: Analyzes problem and creates plan
   - **Executor**: Runs tools in sequence
   - **Reasoner**: Synthesizes results
   - **Memory**: Maintains context across calls

### Practical Skills

You will be able to:

- ✅ Implement chain-style agent execution flows
- ✅ Track token usage and costs in real-time
- ✅ Build Prometheus metrics for ML systems
- ✅ Deploy horizontally scalable agents
- ✅ Implement decision logging for auditing
- ✅ Design tool execution pipelines
- ✅ Manage agent state in memory
- ✅ Configure autoscaling for agent workloads

### Real-World Applications

**ML Platform Engineers** will learn:
- Production deployment patterns for LangChain agents
- Cost tracking and optimization strategies
- Horizontal scaling for agent workloads
- Observability for AI systems

**SREs** will learn:
- Running AI agents in production
- Monitoring token usage and costs
- Autoscaling agent deployments
- Reliability patterns for ML services

**FinOps Teams** will learn:
- Tracking ML inference costs
- Token-level cost attribution
- Budget management for AI services
- Cost optimization opportunities

---

## 📋 Prerequisites

### Required Software
- **Operating System:** Ubuntu 22.04 (or similar Linux / WSL2 / macOS)
- **Docker:** Version 24 or higher
- **kind:** Kubernetes in Docker
- **kubectl:** Version 1.29 or higher
- **Python:** Version 3.11 or higher
- **curl:** For API testing

### Required Knowledge
- Basic understanding of LangChain concepts (chains, tools, agents)
- Kubernetes fundamentals (deployments, services, HPA)
- Prometheus metrics basics
- Cost management principles

### Important Note

**This lab does NOT require:**
- ❌ LangChain installation
- ❌ OpenAI API key
- ❌ GPU resources
- ❌ Redis or Postgres
- ❌ Vector databases

**Why?** This free version focuses on **operational patterns** you need to run LangChain agents in production, not the LangChain library itself. You'll learn the infrastructure side.

---

## 🏗️ Architecture Overview

### What You're Building

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         Namespace: langchain-free                     │  │
│  │                                                        │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │  Deployment: langchain-free (3 replicas)     │    │  │
│  │  │                                              │    │  │
│  │  │  ┌────────────────────────────────────────┐ │    │  │
│  │  │  │  Pod 1: Chain Agent                    │ │    │  │
│  │  │  │  ┌──────────────────────────────────┐  │ │    │  │
│  │  │  │  │  FastAPI (Port 8000)             │  │ │    │  │
│  │  │  │  │  ├─ /investigate                 │  │ │    │  │
│  │  │  │  │  ├─ /metrics (Prometheus)        │  │ │    │  │
│  │  │  │  │  └─ /health                      │  │ │    │  │
│  │  │  │  └──────────────┬───────────────────┘  │ │    │  │
│  │  │  │                 │                       │ │    │  │
│  │  │  │                 ▼                       │ │    │  │
│  │  │  │  ┌──────────────────────────────────┐  │ │    │  │
│  │  │  │  │  Chain Engine                    │  │ │    │  │
│  │  │  │  │                                  │  │ │    │  │
│  │  │  │  │  Step 1: Planner                 │  │ │    │  │
│  │  │  │  │  ├─ Analyze alert                │  │ │    │  │
│  │  │  │  │  ├─ Generate plan                │  │ │    │  │
│  │  │  │  │  └─ Track tokens used            │  │ │    │  │
│  │  │  │  │                                  │  │ │    │  │
│  │  │  │  │  Step 2: Executor                │  │ │    │  │
│  │  │  │  │  ├─ Run tools in sequence        │  │ │    │  │
│  │  │  │  │  ├─ Collect results              │  │ │    │  │
│  │  │  │  │  └─ Track tokens used            │  │ │    │  │
│  │  │  │  │                                  │  │ │    │  │
│  │  │  │  │  Step 3: Reasoner                │  │ │    │  │
│  │  │  │  │  ├─ Synthesize findings          │  │ │    │  │
│  │  │  │  │  ├─ Generate summary             │  │ │    │  │
│  │  │  │  │  └─ Track tokens used            │  │ │    │  │
│  │  │  │  └──────────────┬───────────────────┘  │ │    │  │
│  │  │  │                 │                       │ │    │  │
│  │  │  │      ┌──────────┴─────────┐            │ │    │  │
│  │  │  │      │                    │            │ │    │  │
│  │  │  │      ▼                    ▼            │ │    │  │
│  │  │  │  ┌─────────┐      ┌──────────────┐    │ │    │  │
│  │  │  │  │ Tools   │      │ Cost Tracker │    │ │    │  │
│  │  │  │  │         │      │              │    │ │    │  │
│  │  │  │  │ - check │      │ - Tokens used│    │ │    │  │
│  │  │  │  │   _pods │      │ - Cost (USD) │    │ │    │  │
│  │  │  │  │ - get   │      │ - Per chain  │    │ │    │  │
│  │  │  │  │   _logs │      │ - Cumulative │    │ │    │  │
│  │  │  │  │ - get   │      └──────────────┘    │ │    │  │
│  │  │  │  │   _metric                           │ │    │  │
│  │  │  │  └─────────┘                           │ │    │  │
│  │  │  │                                        │ │    │  │
│  │  │  │  ┌──────────────────────────────────┐ │ │    │  │
│  │  │  │  │  Memory Store (In-process)       │ │ │    │  │
│  │  │  │  │  - Last alert                    │ │ │    │  │
│  │  │  │  │  - Investigation history         │ │ │    │  │
│  │  │  │  │  - Service patterns              │ │ │    │  │
│  │  │  │  └──────────────────────────────────┘ │ │    │  │
│  │  │  │                                        │ │    │  │
│  │  │  │  ┌──────────────────────────────────┐ │ │    │  │
│  │  │  │  │  Metrics Exporter                │ │ │    │  │
│  │  │  │  │  - agent_requests_total          │ │ │    │  │
│  │  │  │  │  - agent_tokens_total            │ │ │    │  │
│  │  │  │  │  - agent_cost_total              │ │ │    │  │
│  │  │  │  │  - agent_latency_seconds         │ │ │    │  │
│  │  │  │  └──────────────────────────────────┘ │ │    │  │
│  │  │  └────────────────────────────────────────┘ │    │  │
│  │  │                                              │    │  │
│  │  │  Pod 2 and Pod 3: Same structure            │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  │                                                        │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │  Service: langchain-free (LoadBalancer)      │    │  │
│  │  │  Distributes traffic across 3 pods           │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  │                                                        │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │  HPA: Horizontal Pod Autoscaler              │    │  │
│  │  │  Min: 1, Max: 5, Target CPU: 70%             │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Chain Execution Flow

```
Investigation Request
    ↓
┌─────────────────────────────────────────┐
│  STEP 1: PLANNER                        │
│  ┌───────────────────────────────────┐  │
│  │ Input: Alert                      │  │
│  │ {                                 │  │
│  │   "alert_type": "high_latency",   │  │
│  │   "service": "checkout-api"       │  │
│  │ }                                 │  │
│  │                                   │  │
│  │ Process:                          │  │
│  │ - Analyze alert type              │  │
│  │ - Determine required tools        │  │
│  │ - Generate plan                   │  │
│  │ - Simulate LLM token usage        │  │
│  │                                   │  │
│  │ Output:                           │  │
│  │ {                                 │  │
│  │   "plan": [                       │  │
│  │     "check_pods",                 │  │
│  │     "get_metrics",                │  │
│  │     "get_logs"                    │  │
│  │   ],                              │  │
│  │   "tokens_used": 45               │  │
│  │ }                                 │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  STEP 2: EXECUTOR                       │
│  ┌───────────────────────────────────┐  │
│  │ For each tool in plan:            │  │
│  │                                   │  │
│  │ Tool 1: check_pods                │  │
│  │ Result: "3 pods running,          │  │
│  │          1 high latency"          │  │
│  │ Tokens: 12                        │  │
│  │                                   │  │
│  │ Tool 2: get_metrics               │  │
│  │ Result: "p95: 480ms (target:      │  │
│  │          200ms)"                  │  │
│  │ Tokens: 15                        │  │
│  │                                   │  │
│  │ Tool 3: get_logs                  │  │
│  │ Result: "ERROR: Database timeout" │  │
│  │ Tokens: 18                        │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  STEP 3: REASONER                       │
│  ┌───────────────────────────────────┐  │
│  │ Input: All tool results           │  │
│  │                                   │  │
│  │ Process:                          │  │
│  │ - Analyze findings                │  │
│  │ - Identify root cause             │  │
│  │ - Generate recommendations        │  │
│  │ - Simulate LLM token usage        │  │
│  │                                   │  │
│  │ Output:                           │  │
│  │ {                                 │  │
│  │   "summary": "Database timeout    │  │
│  │    causing high latency",         │  │
│  │   "root_cause": "Connection pool  │  │
│  │    exhaustion",                   │  │
│  │   "recommendations": [            │  │
│  │     "Increase connection pool",   │  │
│  │     "Add timeout monitoring"      │  │
│  │   ],                              │  │
│  │   "tokens_used": 67               │  │
│  │ }                                 │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
    ↓
Final Report + Cost Tracking
{
  "total_tokens": 157,
  "cost_usd": 0.000314,
  "execution_time_ms": 234
}
```

---

## 📁 Repository Structure

```
lab-05.1-langchain-production-free/
├── README.md                   ← This file
├── setup.md                    ← Detailed setup guide
├── kind-cluster.yaml           ← Cluster configuration
├── Dockerfile                  ← Container image definition
├── app/
│   ├── main.py                 ← FastAPI application
│   ├── chain_engine.py         ← Chain execution (Planner→Executor→Reasoner)
│   ├── tools.py                ← Simulated infrastructure tools
│   ├── cost_tracker.py         ← Token usage and cost calculation
│   ├── memory.py               ← In-process state management
│   ├── metrics.py              ← Prometheus metrics exporter
│   ├── config.py               ← Configuration management
│   ├── requirements.txt        ← Python dependencies
│   └── tests/
│       ├── test_main.py        ← API tests
│       ├── test_chain.py       ← Chain execution tests
│       ├── test_tools.py       ← Tool tests
│       ├── test_cost.py        ← Cost tracking tests
│       └── test_metrics.py     ← Metrics tests
└── k8s/
    ├── namespace.yaml          ← Namespace isolation
    ├── deployment.yaml         ← 3-replica deployment
    ├── service.yaml            ← Load balancer service
    └── hpa.yaml                ← Horizontal Pod Autoscaler
```

---

## 🚀 Quick Start Guide

### Option 1: Run Locally

**Step 1: Navigate to app directory**
```bash
cd lab-05.1-langchain-production-free/app
```

**Step 2: Install dependencies**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Step 3: Start the agent**
```bash
uvicorn main:app --reload
```

**Step 4: Test investigation**

```bash
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "alert_type": "high_latency",
    "service": "checkout-api"
  }'
```

**Expected Response:**
```json
{
  "investigation_id": "inv_abc123",
  "alert": {
    "alert_type": "high_latency",
    "service": "checkout-api",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "chain_execution": {
    "planner": {
      "plan": ["check_pods", "get_metrics", "get_logs"],
      "reasoning": "High latency requires checking pod health, metrics, and logs",
      "tokens_used": 45
    },
    "executor": {
      "steps": [
        {
          "step": 1,
          "tool": "check_pods",
          "result": "[SIMULATED] 3 pods running: checkout-api-1, checkout-api-2, checkout-api-3. Pod checkout-api-2 showing high response time.",
          "tokens_used": 12,
          "duration_ms": 45
        },
        {
          "step": 2,
          "tool": "get_metrics",
          "result": "[SIMULATED] Metrics for checkout-api: p50=120ms, p95=480ms, p99=890ms. Target: p95 < 200ms.",
          "tokens_used": 15,
          "duration_ms": 32
        },
        {
          "step": 3,
          "tool": "get_logs",
          "result": "[SIMULATED] Recent errors: ERROR: Database connection timeout after 5000ms. Connection pool: 45/50 in use.",
          "tokens_used": 18,
          "duration_ms": 38
        }
      ],
      "total_tokens": 45
    },
    "reasoner": {
      "summary": "The checkout-api service is experiencing high latency (p95: 480ms vs target 200ms) due to database connection timeouts. Connection pool is near exhaustion (45/50 connections in use).",
      "root_cause": "Database connection pool exhaustion leading to timeout errors",
      "recommendations": [
        "Increase database connection pool size from 50 to 100",
        "Add connection timeout monitoring and alerts",
        "Review slow queries causing long-held connections",
        "Consider adding connection pooling at application layer"
      ],
      "confidence": 0.85,
      "tokens_used": 67
    }
  },
  "cost_tracking": {
    "total_tokens": 157,
    "breakdown": {
      "planner": 45,
      "executor": 45,
      "reasoner": 67
    },
    "cost_usd": 0.000314,
    "model": "simulated-gpt-4"
  },
  "execution_time_ms": 234,
  "memory_updated": true
}
```

**Step 5: View metrics**
```bash
curl http://localhost:8000/metrics
```

**Expected Output:**
```
# HELP agent_requests_total Total investigation requests
# TYPE agent_requests_total counter
agent_requests_total 1

# HELP agent_tokens_total Total tokens consumed
# TYPE agent_tokens_total counter
agent_tokens_total 157

# HELP agent_cost_total Total cost in USD
# TYPE agent_cost_total counter
agent_cost_total 0.000314

# HELP agent_latency_seconds Investigation latency
# TYPE agent_latency_seconds histogram
agent_latency_seconds_bucket{le="0.1"} 0
agent_latency_seconds_bucket{le="0.5"} 1
agent_latency_seconds_bucket{le="1.0"} 1
agent_latency_seconds_sum 0.234
agent_latency_seconds_count 1
```

---

### Option 2: Run on Kubernetes

**Step 1: Create kind cluster**
```bash
cd lab-05.1-langchain-production-free
kind create cluster --config kind-cluster.yaml
```

**Step 2: Build and load image**
```bash
docker build -t langchain-free:v1 .
kind load docker-image langchain-free:v1 --name langchain-free
```

**Step 3: Deploy**
```bash
kubectl apply -f k8s/
```

**Step 4: Wait for pods**
```bash
kubectl wait --for=condition=available --timeout=60s deployment/langchain-free -n langchain-free
```

**Step 5: Port-forward and test**
```bash
kubectl -n langchain-free port-forward svc/langchain-free 8000:8000

# In another terminal
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"alert_type":"high_cpu","service":"payment-api"}'
```

---

## 📊 Understanding Production Patterns

### 1. Chain-Style Execution

**Why chains matter:**
- **Structured reasoning**: Breaking complex tasks into steps
- **Observability**: Each step is trackable
- **Error handling**: Failures are isolated
- **Optimization**: Steps can be cached or parallelized

**Chain pattern:**
```python
class ChainEngine:
    def execute(self, alert):
        # Step 1: Planning
        plan = self.planner.generate_plan(alert)
        
        # Step 2: Execution
        results = self.executor.run_tools(plan)
        
        # Step 3: Reasoning
        summary = self.reasoner.synthesize(results)
        
        return {
            "plan": plan,
            "results": results,
            "summary": summary
        }
```

### 2. Token Tracking and Cost Management

**Token simulation:**
```python
class CostTracker:
    def __init__(self):
        self.cost_per_1k_tokens = 0.002  # $0.002 per 1K tokens (GPT-4 pricing)
    
    def track_step(self, step_name, input_text, output_text):
        # Simulate token counting
        tokens = len(input_text.split()) + len(output_text.split())
        cost = (tokens / 1000) * self.cost_per_1k_tokens
        
        return {
            "step": step_name,
            "tokens": tokens,
            "cost_usd": cost
        }
```

**Why this matters in production:**
- LLM costs can be 70-90% of operational expenses
- Token tracking enables cost attribution
- Budget alerts prevent runaway costs
- Optimization opportunities become visible

### 3. Prometheus Metrics

**Exposed metrics:**
```
agent_requests_total          - Total investigations
agent_tokens_total            - Total tokens consumed
agent_cost_total             - Total cost (USD)
agent_latency_seconds        - Request latency histogram
agent_errors_total           - Error count
agent_tools_executed_total   - Tool execution count
```

**Production monitoring:**
```yaml
# Prometheus scrape config
scrape_configs:
  - job_name: 'langchain-agent'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: ['langchain-free']
    metrics_path: '/metrics'
```

### 4. Horizontal Scaling

**Why 3 replicas?**
- **High availability**: No single point of failure
- **Load distribution**: Traffic spread across pods
- **Rolling updates**: Zero downtime deployments
- **Resource efficiency**: Better resource utilization

**HPA configuration:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: langchain-free
spec:
  minReplicas: 1
  maxReplicas: 5
  targetCPUUtilizationPercentage: 70
```

---

## 🧪 Running Tests

```bash
cd lab-05.1-langchain-production-free/app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

**Expected Output:**
```
================== test session starts ==================
collected 12 items

tests/test_main.py::test_health_endpoint PASSED        [8%]
tests/test_main.py::test_investigate_endpoint PASSED   [16%]
tests/test_chain.py::test_planner PASSED               [25%]
tests/test_chain.py::test_executor PASSED              [33%]
tests/test_chain.py::test_reasoner PASSED              [41%]
tests/test_tools.py::test_check_pods PASSED            [50%]
tests/test_tools.py::test_get_metrics PASSED           [58%]
tests/test_cost.py::test_token_tracking PASSED         [66%]
tests/test_cost.py::test_cost_calculation PASSED       [75%]
tests/test_metrics.py::test_metrics_export PASSED      [83%]
tests/test_metrics.py::test_prometheus_format PASSED   [91%]
tests/test_metrics.py::test_metric_values PASSED       [100%]

=================== 12 passed in 1.85s ===================
```

---

## 💰 Cost Analysis

### Running in KIND: $0/month

Completely free for learning and development.

### Production Deployment: $20-30/month

**Scenario:** Real LangChain with GPT-4

**Infrastructure:**
```
3 agent pods: 0.5 CPU × 3 × 730 hrs × $0.04/hr = $43.80
With spot instances (70% off): $13.14
```

**LLM Costs:**
```
Assumptions:
- 1000 investigations/month
- 150 tokens average per investigation
- GPT-4: $0.002 per 1K tokens

Monthly LLM cost: 1000 × 150 / 1000 × $0.002 = $0.30
```

**Total: ~$13-15/month** with spot instances

### Cost Optimization Strategies

**1. Caching:**
```python
# Cache common investigation patterns
if alert_type in cache:
    return cached_result  # Save LLM call
```

**2. Model selection:**
```
GPT-4: $0.002/1K tokens - Use for complex investigations
GPT-3.5: $0.0002/1K tokens - Use for simple alerts (90% savings!)
```

**3. Prompt optimization:**
```
Verbose prompt: 500 tokens
Optimized prompt: 100 tokens
Savings: 80%
```

---

## 🎓 Key Learning Outcomes

### Conceptual Understanding

After completing this lab, you understand:

✅ **LangChain Production Patterns:**
- Chain-style execution (Planner→Executor→Reasoner)
- Tool orchestration in production
- State management across requests
- Cost tracking and optimization

✅ **Operational Patterns:**
- Horizontal scaling for ML agents
- Metrics exposure for observability
- Resource management
- Health monitoring

✅ **Cost Management:**
- Token-level tracking
- Real-time cost calculation
- Budget management
- Optimization strategies

✅ **Infrastructure Design:**
- Multi-replica deployments
- Autoscaling based on load
- Zero-downtime updates
- Prometheus integration

### Technical Skills

You can now:

✅ **Deploy LangChain-style agents** in production
✅ **Implement chain execution** patterns
✅ **Track and optimize costs** at token level
✅ **Expose Prometheus metrics** for ML systems
✅ **Configure horizontal scaling** for agents
✅ **Manage agent state** in memory
✅ **Debug chain execution** flows

### Real-World Patterns

You've learned:

✅ **Chain orchestration** - Multi-step agent workflows
✅ **Cost-aware AI** - Financial intelligence in agents
✅ **Production scaling** - High-availability patterns
✅ **Observability** - Metrics for AI systems

---

## 🔧 Troubleshooting

### Issue: Metrics Not Showing

**Check metrics endpoint:**
```bash
curl http://localhost:8000/metrics
```

**Verify Prometheus format:**
```bash
curl http://localhost:8000/metrics | grep "# HELP"
```

### Issue: High Memory Usage

**Check pod memory:**
```bash
kubectl top pod -n langchain-free
```

**Adjust limits:**
```yaml
resources:
  limits:
    memory: "512Mi"  # Increase if needed
```

---

## 🧹 Cleanup

```bash
kubectl delete namespace langchain-free
kind delete cluster --name langchain-free
```

---

## 📚 Next Steps

### Explore PAID Version

The PAID version adds:
- **Real LangChain** integration
- **Redis** conversation memory
- **Postgres** decision logs
- **Vector DB** semantic memory
- **OpenTelemetry** tracing
- **Grafana** dashboards

---

## 🎉 Congratulations!

You've mastered LangChain production patterns!

### What You've Learned:

✅ **Chain Execution** - Multi-step agent workflows  
✅ **Cost Tracking** - Token-level financial intelligence  
✅ **Production Scaling** - Horizontal pod autoscaling  
✅ **Observability** - Prometheus metrics for AI  

You now understand how to run LangChain agents in production!

Happy learning! 🚀🔗🤖💰
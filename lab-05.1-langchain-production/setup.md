# Lab 5.1 FREE Setup Guide – Production-Style LangChain Agent Patterns
## Learning LangChain Operations Without the Complexity

---

## 🎯 What You Will Achieve

By completing this setup, you will:

### Learning Objectives

1. **Implement Chain-Style Execution** - Multi-step agent workflows
2. **Track Token Usage and Costs** - Real-time financial monitoring
3. **Deploy Horizontally Scaled Agents** - 3-replica production pattern
4. **Expose Prometheus Metrics** - Observability for ML systems
5. **Configure Autoscaling** - HPA for agent workloads
6. **Understand LangChain Patterns** - Without installing LangChain

### Expected Outcomes

- ✅ Working chain execution engine (Planner→Executor→Reasoner)
- ✅ Token tracking and cost calculation system
- ✅ Prometheus metrics exposure
- ✅ 3-replica deployment in Kubernetes
- ✅ Horizontal Pod Autoscaler configured
- ✅ In-process memory for state management
- ✅ Comprehensive test coverage
- ✅ Understanding of production LangChain patterns

### Real-World Skills

**ML Engineers** will learn:
- Deploying chain-based agents
- Cost tracking for LLM systems
- Production scaling patterns

**SREs** will learn:
- Running AI agents reliably
- Monitoring ML workloads
- Autoscaling agent deployments

**FinOps Teams** will learn:
- Tracking LLM costs
- Token-level attribution
- Budget management

---

## 📋 Prerequisites

### Required Software

**1. Docker (24+)**
```bash
docker --version
```

**2. kind**
```bash
kind version
```

**3. kubectl (1.29+)**
```bash
kubectl version --client
```

**4. Python (3.11+)**
```bash
python3 --version
```

### Required Knowledge

- Basic understanding of LangChain concepts
- Kubernetes fundamentals
- Prometheus metrics basics

### Important Note

**This lab does NOT require:**
- ❌ LangChain library
- ❌ OpenAI API key
- ❌ External databases
- ❌ GPU resources

---

## 🏗️ Understanding Chain Architecture

### Chain Execution Pattern

```
Investigation Request
    ↓
┌────────────────────────────────┐
│  PLANNER                        │
│  Input: Alert                   │
│  Output: Plan + Token Count     │
│  Time: ~50ms                    │
└────────────────┬───────────────┘
                 │
                 ▼
┌────────────────────────────────┐
│  EXECUTOR                       │
│  Input: Plan                    │
│  For each tool:                 │
│    - Execute                    │
│    - Track tokens               │
│    - Collect result             │
│  Output: Results + Token Count  │
│  Time: ~100ms                   │
└────────────────┬───────────────┘
                 │
                 ▼
┌────────────────────────────────┐
│  REASONER                       │
│  Input: All results             │
│  Output: Summary + Token Count  │
│  Time: ~80ms                    │
└────────────────┬───────────────┘
                 │
                 ▼
Final Report + Total Cost
```

### Cost Tracking Flow

```
Each step tracks tokens:
  Planner: 45 tokens
  Tool 1: 12 tokens
  Tool 2: 15 tokens
  Tool 3: 18 tokens
  Reasoner: 67 tokens
  ────────────────────
  Total: 157 tokens

Cost calculation:
  157 tokens × ($0.002 / 1000 tokens) = $0.000314
```

---

## 🚀 Step-by-Step Setup

### Step 1: Navigate to Lab Directory

```bash
cd lab-05.1-langchain-production-free
```

Verify you're in the correct location:
```bash
ls
```

**Expected Output:**
```
Dockerfile  README.md  app/  k8s/  kind-cluster.yaml  setup.md
```

---

### Step 2: Examine Chain Engine Code

Before running, understand the chain pattern.

**View chain engine:**
```bash
cat app/chain_engine.py | head -100
```

**Key components:**

**1. Planner:**
```python
class Planner:
    def generate_plan(self, alert):
        """Generate investigation plan based on alert"""
        # Simulate LLM reasoning
        plan = self._determine_tools(alert)
        tokens = self._simulate_tokens(alert, plan)
        
        return {
            "plan": plan,
            "reasoning": self._explain_plan(alert),
            "tokens_used": tokens
        }
```

**2. Executor:**
```python
class Executor:
    def run_tools(self, plan):
        """Execute tools in sequence"""
        results = []
        for tool_name in plan:
            result = self.tools.execute(tool_name)
            tokens = self._simulate_tool_tokens(result)
            results.append({
                "tool": tool_name,
                "result": result,
                "tokens": tokens
            })
        return results
```

**3. Reasoner:**
```python
class Reasoner:
    def synthesize(self, results):
        """Analyze results and generate summary"""
        summary = self._analyze_findings(results)
        recommendations = self._generate_recommendations(results)
        tokens = self._simulate_reasoning_tokens(summary)
        
        return {
            "summary": summary,
            "recommendations": recommendations,
            "tokens_used": tokens
        }
```

---

### Step 3: Run Locally First

**Navigate to app directory:**
```bash
cd app
```

**Create virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Collecting fastapi==0.104.1
Collecting uvicorn[standard]==0.24.0
Collecting prometheus-client==0.19.0
...
Successfully installed fastapi uvicorn prometheus-client ...
```

**Start the agent:**
```bash
uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started server process [12345]
INFO:     ChainEngine initialized
INFO:     Planner ready
INFO:     Executor loaded 3 tools
INFO:     Reasoner initialized
INFO:     CostTracker configured (model: simulated-gpt-4)
INFO:     Metrics exporter ready
INFO:     Application startup complete
```

---

### Step 4: Test Chain Execution

Open a new terminal (keep agent running).

**Test high latency investigation:**
```bash
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "alert_type": "high_latency",
    "service": "checkout-api"
  }'
```

**Expected Response (formatted):**
```json
{
  "investigation_id": "inv_abc123xyz",
  "timestamp": "2024-01-15T10:30:00Z",
  "alert": {
    "alert_type": "high_latency",
    "service": "checkout-api"
  },
  "chain_execution": {
    "planner": {
      "plan": ["check_pods", "get_metrics", "get_logs"],
      "reasoning": "High latency requires checking pod health, current metrics, and recent logs to identify the root cause",
      "tokens_used": 45,
      "duration_ms": 52
    },
    "executor": {
      "steps": [
        {
          "step": 1,
          "tool": "check_pods",
          "result": "[SIMULATED] Found 3 pods for checkout-api: checkout-api-1 (healthy), checkout-api-2 (high latency), checkout-api-3 (healthy)",
          "tokens_used": 12,
          "duration_ms": 45
        },
        {
          "step": 2,
          "tool": "get_metrics",
          "result": "[SIMULATED] Metrics for checkout-api: p50=120ms, p95=480ms, p99=890ms. Target: p95 < 200ms. Current: EXCEEDING TARGET",
          "tokens_used": 15,
          "duration_ms": 32
        },
        {
          "step": 3,
          "tool": "get_logs",
          "result": "[SIMULATED] Recent errors from checkout-api-2: ERROR: Database connection timeout after 5000ms. Connection pool: 45/50 connections in use",
          "tokens_used": 18,
          "duration_ms": 38
        }
      ],
      "total_tokens": 45,
      "total_duration_ms": 115
    },
    "reasoner": {
      "summary": "The checkout-api service is experiencing high latency (p95: 480ms vs target 200ms) due to database connection timeouts. Analysis shows connection pool near exhaustion (45/50 connections).",
      "root_cause": "Database connection pool exhaustion leading to timeout errors",
      "recommendations": [
        "Increase database connection pool size from 50 to 100",
        "Add connection timeout monitoring and alerts",
        "Review slow queries causing long-held connections",
        "Consider implementing connection pooling at application layer",
        "Add circuit breaker for database failures"
      ],
      "confidence": 0.85,
      "tokens_used": 67,
      "duration_ms": 78
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
    "cost_per_1k_tokens": 0.002,
    "model": "simulated-gpt-4"
  },
  "execution_time_ms": 245,
  "memory_updated": true
}
```

**What this validates:**
- ✅ Chain executed all three steps
- ✅ Each step tracked tokens
- ✅ Cost calculated correctly
- ✅ Results aggregated properly
- ✅ Recommendations generated

---

### Step 5: Test Different Alert Types

**High CPU alert:**
```bash
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "alert_type": "high_cpu",
    "service": "payment-api"
  }'
```

**Expected:** Different plan (check_pods, get_metrics, check_events)

**Pod crash alert:**
```bash
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "alert_type": "pod_crash",
    "service": "auth-service"
  }'
```

**Expected:** Different plan (check_pods, get_logs, check_events)

**What this validates:**
- ✅ Planner adapts to different alert types
- ✅ Different tools selected based on context
- ✅ Token counts vary by plan complexity

---

### Step 6: Verify Cost Tracking

**Send multiple investigations:**
```bash
for i in {1..5}; do
  curl -s -X POST http://localhost:8000/investigate \
    -H "Content-Type: application/json" \
    -d "{\"alert_type\":\"high_cpu\",\"service\":\"svc$i\"}" > /dev/null
  echo "Investigation $i sent"
done
```

**Check cumulative costs:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "uptime_seconds": 234,
  "investigations_total": 6,
  "cumulative_stats": {
    "total_tokens": 942,
    "total_cost_usd": 0.001884,
    "average_tokens_per_investigation": 157,
    "average_cost_per_investigation": 0.000314
  }
}
```

**What this validates:**
- ✅ Costs accumulate across investigations
- ✅ Averages calculated correctly
- ✅ Health endpoint shows stats

---

### Step 7: View Prometheus Metrics

**Get metrics:**
```bash
curl http://localhost:8000/metrics
```

**Expected Output:**
```
# HELP agent_requests_total Total investigation requests
# TYPE agent_requests_total counter
agent_requests_total 6

# HELP agent_tokens_total Total tokens consumed
# TYPE agent_tokens_total counter
agent_tokens_total 942

# HELP agent_cost_total Total cost in USD
# TYPE agent_cost_total counter
agent_cost_total 0.001884

# HELP agent_latency_seconds Investigation latency in seconds
# TYPE agent_latency_seconds histogram
agent_latency_seconds_bucket{le="0.1"} 0
agent_latency_seconds_bucket{le="0.25"} 6
agent_latency_seconds_bucket{le="0.5"} 6
agent_latency_seconds_bucket{le="1.0"} 6
agent_latency_seconds_bucket{le="+Inf"} 6
agent_latency_seconds_sum 1.470
agent_latency_seconds_count 6

# HELP agent_tools_executed_total Total tool executions
# TYPE agent_tools_executed_total counter
agent_tools_executed_total{tool="check_pods"} 6
agent_tools_executed_total{tool="get_metrics"} 6
agent_tools_executed_total{tool="get_logs"} 3
agent_tools_executed_total{tool="check_events"} 3

# HELP agent_planner_tokens_total Tokens used by planner
# TYPE agent_planner_tokens_total counter
agent_planner_tokens_total 270

# HELP agent_executor_tokens_total Tokens used by executor
# TYPE agent_executor_tokens_total counter
agent_executor_tokens_total 270

# HELP agent_reasoner_tokens_total Tokens used by reasoner
# TYPE agent_reasoner_tokens_total counter
agent_reasoner_tokens_total 402
```

**What this validates:**
- ✅ All metrics exposed in Prometheus format
- ✅ Counters incrementing correctly
- ✅ Histograms showing latency distribution
- ✅ Per-tool metrics tracked

---

### Step 8: Run Unit Tests

**Ensure in app directory:**
```bash
cd lab-05.1-langchain-production-free/app
source .venv/bin/activate
```

**Run all tests:**
```bash
pytest -v
```

**Expected Output:**
```
================== test session starts ==================
platform linux -- Python 3.11.x, pytest-7.4.x
collected 12 items

tests/test_main.py::test_health_endpoint PASSED        [8%]
tests/test_main.py::test_investigate_endpoint PASSED   [16%]
tests/test_chain.py::test_planner_generation PASSED    [25%]
tests/test_chain.py::test_executor_tools PASSED        [33%]
tests/test_chain.py::test_reasoner_synthesis PASSED    [41%]
tests/test_tools.py::test_check_pods_tool PASSED       [50%]
tests/test_tools.py::test_get_metrics_tool PASSED      [58%]
tests/test_cost.py::test_token_counting PASSED         [66%]
tests/test_cost.py::test_cost_calculation PASSED       [75%]
tests/test_metrics.py::test_metrics_export PASSED      [83%]
tests/test_metrics.py::test_prometheus_format PASSED   [91%]
tests/test_metrics.py::test_counter_increment PASSED   [100%]

=================== 12 passed in 1.85s ===================
```

**Test individual components:**

**Test chain execution:**
```bash
pytest tests/test_chain.py -v
```

**Test cost tracking:**
```bash
pytest tests/test_cost.py -v
```

**Expected details:**
```
tests/test_cost.py::test_token_counting PASSED

Test validated:
  ✓ Token counting simulation accurate
  ✓ Different steps have different token counts
  ✓ Total tokens sum correctly

tests/test_cost.py::test_cost_calculation PASSED

Test validated:
  ✓ Cost calculation formula correct
  ✓ 157 tokens × ($0.002 / 1000) = $0.000314
  ✓ Breakdown by chain step accurate
```

---

### Step 9: Deploy to Kubernetes

**Navigate to lab root:**
```bash
cd .. # Back to lab-05.1-langchain-production-free/
```

**Create kind cluster:**
```bash
kind create cluster --config kind-cluster.yaml
```

**Expected Output:**
```
Creating cluster "langchain-free" ...
 ✓ Ensuring node image (kindest/node:v1.30.0) 🖼
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-langchain-free"
```

**Verify cluster:**
```bash
kubectl get nodes
```

---

### Step 10: Build and Load Docker Image

**Build the image:**
```bash
docker build -t langchain-free:v1 .
```

**Expected Output:**
```
[+] Building 38.2s (13/13) FINISHED
 => [1/7] FROM docker.io/library/python:3.11-slim
 => [2/7] WORKDIR /app
 => [3/7] COPY app/requirements.txt .
 => [4/7] RUN pip install --no-cache-dir -r requirements.txt
 => [5/7] COPY app/ .
 => exporting to image
 => => naming to docker.io/library/langchain-free:v1
```

**Load into kind:**
```bash
kind load docker-image langchain-free:v1 --name langchain-free
```

**Verify:**
```bash
docker exec -it langchain-free-control-plane crictl images | grep langchain-free
```

---

### Step 11: Deploy All Kubernetes Resources

**Create namespace:**
```bash
kubectl apply -f k8s/namespace.yaml
```

**Deploy agent:**
```bash
kubectl apply -f k8s/deployment.yaml
```

**Create service:**
```bash
kubectl apply -f k8s/service.yaml
```

**Create HPA:**
```bash
kubectl apply -f k8s/hpa.yaml
```

**Wait for deployment:**
```bash
kubectl wait --for=condition=available --timeout=120s deployment/langchain-free -n langchain-free
```

---

### Step 12: Verify 3-Replica Deployment

**Check pods:**
```bash
kubectl get pods -n langchain-free
```

**Expected Output:**
```
NAME                              READY   STATUS    RESTARTS   AGE
langchain-free-xxxxxxxxxx-aaaaa   1/1     Running   0          45s
langchain-free-xxxxxxxxxx-bbbbb   1/1     Running   0          45s
langchain-free-xxxxxxxxxx-ccccc   1/1     Running   0          45s
```

**Verify all 3 pods are running:**
```bash
kubectl get pods -n langchain-free | grep -c "1/1.*Running"
```

**Expected:** `3`

**Check HPA:**
```bash
kubectl get hpa -n langchain-free
```

**Expected Output:**
```
NAME             REFERENCE                   TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
langchain-free   Deployment/langchain-free   0%/70%    1         5         3          50s
```

**What this validates:**
- ✅ 3 replicas running (high availability)
- ✅ HPA configured (autoscaling ready)
- ✅ Min 1, Max 5 pods (cost-efficient)

---

### Step 13: Test Load Distribution

**Port-forward to service:**
```bash
kubectl -n langchain-free port-forward svc/langchain-free 8000:8000
```

**Send requests and check which pod handles them:**
```bash
for i in {1..10}; do
  curl -s -X POST http://localhost:8000/investigate \
    -H "Content-Type: application/json" \
    -d "{\"alert_type\":\"high_cpu\",\"service\":\"svc$i\"}" > /dev/null
  echo "Request $i sent"
done
```

**Check logs from all pods:**
```bash
kubectl logs -n langchain-free -l app=langchain-free --tail=5
```

**Expected:** Logs from multiple pods (load distributed)

**Check individual pod logs:**
```bash
POD1=$(kubectl get pods -n langchain-free -o jsonpath='{.items[0].metadata.name}')
kubectl logs -n langchain-free $POD1 --tail=10
```

---

### Step 14: Test Agent in Kubernetes

**Send investigation:**
```bash
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "alert_type": "high_memory",
    "service": "web-app"
  }'
```

**Check metrics from service:**
```bash
curl http://localhost:8000/metrics | grep agent_requests_total
```

**Expected:** Counter incremented

**Test health endpoint:**
```bash
curl http://localhost:8000/health
```

**Expected:** Healthy status with statistics

---

### Step 15: Simulate Load for Autoscaling

**Generate load (requires hey or similar tool):**
```bash
# Install hey if needed
go install github.com/rakyll/hey@latest

# Generate load
hey -z 60s -c 10 -m POST \
  -H "Content-Type: application/json" \
  -d '{"alert_type":"high_cpu","service":"test"}' \
  http://localhost:8000/investigate
```

**Watch HPA scale:**
```bash
kubectl get hpa -n langchain-free --watch
```

**Expected:** Replicas increase if CPU > 70%

**Watch pods scale:**
```bash
kubectl get pods -n langchain-free --watch
```

---

## ✅ Testing and Validation

### Test 1: Chain Execution Completeness

**Verify all chain steps execute:**
```bash
curl -s -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"alert_type":"high_latency","service":"test"}' | \
  jq '.chain_execution | keys'
```

**Expected Output:**
```json
[
  "planner",
  "executor",
  "reasoner"
]
```

### Test 2: Token Tracking Accuracy

**Verify token counts sum correctly:**
```bash
curl -s -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"alert_type":"high_cpu","service":"test"}' | \
  jq '{
    planner: .cost_tracking.breakdown.planner,
    executor: .cost_tracking.breakdown.executor,
    reasoner: .cost_tracking.breakdown.reasoner,
    total: .cost_tracking.total_tokens,
    sum: (.cost_tracking.breakdown.planner + .cost_tracking.breakdown.executor + .cost_tracking.breakdown.reasoner)
  }'
```

**Expected:** `total == sum`

### Test 3: Cost Calculation Formula

**Manual verification:**
```
Token count: 157
Rate: $0.002 per 1K tokens
Expected cost: 157 / 1000 × $0.002 = $0.000314
```

**Verify:**
```bash
curl -s -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"alert_type":"high_cpu","service":"test"}' | \
  jq '.cost_tracking.cost_usd'
```

**Expected:** `0.000314`

### Test 4: Metrics Persistence

**Send investigation:**
```bash
curl -s -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"alert_type":"test","service":"test"}' > /dev/null
```

**Check metric before:**
```bash
BEFORE=$(curl -s http://localhost:8000/metrics | grep "^agent_requests_total" | awk '{print $2}')
```

**Send another:**
```bash
curl -s -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"alert_type":"test","service":"test"}' > /dev/null
```

**Check metric after:**
```bash
AFTER=$(curl -s http://localhost:8000/metrics | grep "^agent_requests_total" | awk '{print $2}')
echo "Before: $BEFORE, After: $AFTER"
```

**Expected:** `AFTER = BEFORE + 1`

### Test 5: Multi-Pod Load Distribution

**Disable one pod:**
```bash
kubectl scale deployment langchain-free -n langchain-free --replicas=2
```

**Send requests:**
```bash
for i in {1..5}; do
  curl -s -X POST http://localhost:8000/investigate \
    -H "Content-Type: application/json" \
    -d '{"alert_type":"test","service":"test"}' > /dev/null
done
```

**Check both pods handled requests:**
```bash
kubectl logs -n langchain-free -l app=langchain-free --tail=20 | grep "Investigation"
```

**Scale back up:**
```bash
kubectl scale deployment langchain-free -n langchain-free --replicas=3
```

---

## 🎓 Understanding What You've Built

### Chain Pattern vs Direct Execution

**Traditional approach:**
```python
# Single monolithic function
def investigate(alert):
    pods = check_pods()
    logs = get_logs()
    metrics = get_metrics()
    return analyze(pods, logs, metrics)
```

**Chain pattern:**
```python
# Structured, observable, optimizable
def investigate(alert):
    # Step 1: Planning
    plan = planner.generate(alert)  # Trackable
    
    # Step 2: Execution
    results = executor.run(plan)    # Parallelizable
    
    # Step 3: Reasoning
    summary = reasoner.synthesize(results)  # Cacheable
    
    return {plan, results, summary}
```

### Cost Tracking Importance

**Real-world LLM costs:**
```
Scenario: 10,000 investigations/month

Without tracking:
  Unknown cost
  No optimization opportunities
  Budget overruns

With tracking:
  10,000 × 157 tokens = 1,570,000 tokens
  1,570 K tokens × $0.002 = $3.14/month
  
  Optimization opportunities:
  - Cache common patterns (30% savings)
  - Use cheaper models (90% savings on simple cases)
  - Reduce verbose prompts (20% savings)
  
  Optimized: ~$1.50/month (52% savings)
```

---

## 💰 Cost Analysis

### Running in KIND: $0/month

Free for learning and development.

### Production Deployment

**Infrastructure (3 replicas):**
```
Compute: 1.5 CPU × 730 hrs × $0.04/hr = $43.80
With spot instances (70% off): $13.14
```

**LLM Costs (if using real LangChain):**
```
10,000 investigations × 150 tokens = 1.5M tokens
GPT-4: 1.5M / 1000 × $0.002 = $3.00
GPT-3.5: 1.5M / 1000 × $0.0002 = $0.30 (90% cheaper!)
```

**Total: $13-16/month** with spot instances and GPT-3.5

---

## 🔧 Troubleshooting

### Issue: HPA Not Scaling

**Check metrics server:**
```bash
kubectl top nodes
kubectl top pods -n langchain-free
```

**If metrics unavailable, install metrics-server:**
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### Issue: Metrics Not Updating

**Check metrics endpoint:**
```bash
kubectl exec -n langchain-free -l app=langchain-free -- curl localhost:8000/metrics
```

**Verify counter increments:**
```bash
# Before
kubectl exec -n langchain-free -l app=langchain-free -- curl -s localhost:8000/metrics | grep agent_requests_total

# Send request
curl -X POST http://localhost:8000/investigate ...

# After
kubectl exec -n langchain-free -l app=langchain-free -- curl -s localhost:8000/metrics | grep agent_requests_total
```

---

## 🧹 Cleanup

### Remove Kubernetes Resources

```bash
kubectl delete namespace langchain-free
```

### Delete kind Cluster

```bash
kind delete cluster --name langchain-free
```

### Clean Local Files

```bash
cd lab-05.1-langchain-production-free/app
rm -rf .venv
rm -rf __pycache__
```

---

## 📊 Success Criteria Checklist

Your lab is complete when:

- [ ] Local agent runs successfully
- [ ] Chain executes all three steps
- [ ] Token tracking accurate
- [ ] Cost calculation correct
- [ ] Metrics exposed in Prometheus format
- [ ] All unit tests pass (12/12)
- [ ] Kind cluster created
- [ ] 3 replicas deployed
- [ ] HPA configured
- [ ] Load distributes across pods
- [ ] Autoscaling works (optional)
- [ ] You understand chain pattern
- [ ] You understand cost tracking importance
- [ ] You understand horizontal scaling

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

✅ **Chain Execution** - Multi-step reasoning workflows  
✅ **Cost Tracking** - Token-level financial monitoring  
✅ **Horizontal Scaling** - Production-ready deployment  
✅ **Prometheus Metrics** - Observability for AI systems  

You now understand how to run LangChain agents in production!

Happy learning! 🚀🔗💰📊
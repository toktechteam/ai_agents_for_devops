# Lab 4.1 Setup Guide – Your First Infrastructure AI Agent
## Building an Autonomous Investigation Agent from Scratch

---

## 🎯 What You Will Achieve

By completing this setup, you will:

### Learning Objectives

1. **Understand AI Agent Architecture** - Learn the core components that make a system "agentic"
2. **Build Planning and Reasoning** - Implement decision-making logic for infrastructure tasks
3. **Create Tool Orchestration** - Enable agents to use multiple tools systematically
4. **Implement Agent Memory** - Store context for better decision-making
5. **Deploy Agents as Services** - Run agents in production-like environments
6. **Test Agent Behavior** - Validate autonomous system behavior

### Expected Outcomes

- ✅ A working infrastructure investigation agent
- ✅ FastAPI service exposing agent capabilities
- ✅ Tool registry with simulated infrastructure operations
- ✅ In-process memory system for context retention
- ✅ Safe executor with error handling
- ✅ Comprehensive test suite validating agent behavior
- ✅ Understanding of agent vs traditional automation
- ✅ Foundation for building production AI agents

### Real-World Skills

**SREs** will learn:
- Automating incident investigation
- Building intelligent alert responders
- Creating self-service diagnostic tools

**Platform Engineers** will learn:
- Agent-based infrastructure automation
- Tool orchestration patterns
- Extending Kubernetes capabilities

**DevOps Engineers** will learn:
- Autonomous system design
- Runbook automation
- Intelligent workflow orchestration

---

## 📋 Prerequisites

### Required Software

**1. Docker (24+)**
```bash
docker --version
```
Expected: `Docker version 24.x.x or higher`

**2. kind**
```bash
kind version
```
Expected: `kind v0.20.0 or higher`

**3. kubectl (1.29+)**
```bash
kubectl version --client
```
Expected: `v1.29.0 or higher`

**4. Python (3.11+)**
```bash
python3 --version
```
Expected: `Python 3.11.x or higher`

**5. curl**
```bash
curl --version
```

### Required Knowledge

- Basic Python programming
- Understanding of REST APIs
- Basic Kubernetes concepts (pods, services, deployments)
- Familiarity with DevOps practices (alerts, logs, metrics)

---

## 🏗️ Understanding Agent Architecture

### What Makes This an "Agent"?

Traditional automation:
```python
# Fixed script - no reasoning
if cpu > 90:
    check_logs()
    restart_pod()
```

AI Agent:
```python
# Dynamic reasoning
alert = receive_alert()
plan = agent.analyze_and_plan(alert)  # Decides what to do
results = agent.execute(plan)         # Orchestrates tools
agent.learn_from(results)             # Improves over time
```

### Agent Components

```
┌─────────────────────────────────────────────┐
│              SimpleAgent                     │
│  ┌────────────────────────────────────────┐ │
│  │  Planning Engine                       │ │
│  │  - Analyzes alerts                     │ │
│  │  - Generates investigation plans       │ │
│  │  - Adapts based on context            │ │
│  └────────────────┬───────────────────────┘ │
│                   │                          │
│      ┌────────────┴────────────┐            │
│      │                         │            │
│      ▼                         ▼            │
│  ┌─────────────┐         ┌──────────────┐  │
│  │ Tool        │         │   Memory     │  │
│  │ Registry    │         │   Store      │  │
│  │             │         │              │  │
│  │ - check_pods│         │ - Last alert │  │
│  │ - get_logs  │         │ - Findings   │  │
│  │ - get_metric│         │ - Patterns   │  │
│  └──────┬──────┘         └──────┬───────┘  │
│         │                       │          │
│         └───────┬───────────────┘          │
│                 ▼                          │
│         ┌───────────────┐                 │
│         │ SafeExecutor  │                 │
│         │ - Error handle│                 │
│         │ - Timeouts    │                 │
│         └───────────────┘                 │
└─────────────────────────────────────────────┘
```

### Investigation Workflow

```
Alert: "high_cpu on payment-api"
    ↓
Agent Reasoning:
  "This is a CPU issue. I should:
   1. Check pod status (are pods healthy?)
   2. Get recent logs (what errors occurred?)
   3. Check metrics (how bad is it?)"
    ↓
Plan Generated:
  ["check_pods", "get_logs", "get_metrics"]
    ↓
Execute Tools:
  check_pods → "3 pods: 2 healthy, 1 degraded"
  get_logs → "ERROR: Connection pool exhausted"
  get_metrics → "CPU: 95%, Memory: 60%"
    ↓
Store in Memory:
  {
    "findings": ["High CPU on pod-789", "Connection issue"],
    "patterns": ["payment-api has connection issues"]
  }
    ↓
Return Report with actionable insights
```

---

## 🚀 Step-by-Step Setup

### Step 1: Navigate to Lab Directory

```bash
cd lab-04.1-first-ai-agent-free
```

Verify you're in the correct location:
```bash
ls
```

**Expected Output:**
```
Dockerfile  README.md  app/  k8s/  kind-mcp-cluster.yaml  setup.md
```

---

### Step 2: Examine the Agent Code (Understanding First)

Before running, let's understand what we're building.

**View the agent core:**
```bash
cat app/agent.py | head -50
```

**Key agent methods:**

**1. generate_plan()** - Reasoning:
```python
def generate_plan(self, alert):
    """Generate investigation plan based on alert type"""
    alert_type = alert.get("type")
    
    if alert_type == "high_cpu":
        return ["check_pods", "get_logs", "get_metrics"]
    elif alert_type == "high_memory":
        return ["check_pods", "get_metrics", "check_events"]
    # ... more alert types
```

**2. investigate()** - Orchestration:
```python
def investigate(self, alert):
    """Run full investigation"""
    # 1. Generate plan
    plan = self.generate_plan(alert)
    
    # 2. Execute each tool
    results = []
    for tool_name in plan:
        tool = self.tools.get(tool_name)
        result = self.executor.execute(tool, alert["service"])
        results.append({"tool": tool_name, "result": result})
    
    # 3. Store in memory
    self.memory.store(alert, results)
    
    # 4. Return report
    return {
        "alert": alert,
        "plan": plan,
        "investigation": results,
        "memory_snapshot": self.memory.snapshot()
    }
```

**View tools:**
```bash
cat app/tools.py | grep "def "
```

**Understanding tools:**
- `check_pods` - Simulates checking pod status
- `get_logs` - Simulates retrieving recent logs
- `get_metrics` - Simulates fetching current metrics
- `check_events` - Simulates checking Kubernetes events

---

### Step 3: Run Locally (Recommended First)

**Navigate to app directory:**
```bash
cd app
```

**Create virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Expected Output:**
```
(.venv) user@machine:~/lab-04.1-first-ai-agent-free/app$
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Collecting fastapi==0.104.1
Collecting uvicorn[standard]==0.24.0
Collecting pytest==7.4.3
...
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 pytest-7.4.3 ...
```

**Start the agent service:**
```bash
uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['/path/to/app']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**What this validates:**
- ✅ Python environment is correct
- ✅ Dependencies installed successfully
- ✅ FastAPI application starts
- ✅ Agent initialized without errors

---

### Step 4: Test the Agent with Different Alerts

Open a new terminal (keep the agent running).

**Test 1: High CPU Alert**

```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type": "high_cpu", "service": "payment-api"}'
```

**Expected Response:**
```json
{
  "alert": {
    "type": "high_cpu",
    "service": "payment-api"
  },
  "plan": [
    "check_pods",
    "get_logs",
    "get_metrics"
  ],
  "investigation": [
    {
      "tool": "check_pods",
      "result": "Found 3 pods for payment-api: 2 healthy, 1 high CPU (pod-789)"
    },
    {
      "tool": "get_logs",
      "result": "Last 10 lines from pod-789: ERROR: Connection pool exhausted at line 234"
    },
    {
      "tool": "get_metrics",
      "result": "payment-api metrics - CPU: 95%, Memory: 60%, Requests: 450/s"
    }
  ],
  "memory_snapshot": {
    "last_alert": {
      "type": "high_cpu",
      "service": "payment-api"
    },
    "findings": [
      "High CPU detected on pod-789",
      "Connection pool exhaustion found in logs"
    ],
    "total_investigations": 1
  }
}
```

**What this validates:**
- ✅ Agent received alert correctly
- ✅ Generated appropriate plan for CPU issue
- ✅ Executed all three tools in order
- ✅ Each tool returned simulated but realistic data
- ✅ Results stored in memory
- ✅ Memory snapshot includes findings

---

**Test 2: High Memory Alert**

```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type": "high_memory", "service": "web-app"}'
```

**Expected Response:**
```json
{
  "alert": {
    "type": "high_memory",
    "service": "web-app"
  },
  "plan": [
    "check_pods",
    "get_metrics",
    "check_events"
  ],
  "investigation": [
    {
      "tool": "check_pods",
      "result": "Found 5 pods for web-app: 4 healthy, 1 high memory (pod-456)"
    },
    {
      "tool": "get_metrics",
      "result": "web-app metrics - CPU: 45%, Memory: 92%, Requests: 200/s"
    },
    {
      "tool": "check_events",
      "result": "Recent events: Warning: OOMKilled pod-456 5 minutes ago"
    }
  ],
  "memory_snapshot": {
    "last_alert": {
      "type": "high_memory",
      "service": "web-app"
    },
    "findings": [
      "High CPU detected on pod-789",
      "Connection pool exhaustion found in logs",
      "High memory on pod-456",
      "OOMKilled event detected"
    ],
    "total_investigations": 2
  }
}
```

**What this validates:**
- ✅ Agent adapts plan based on alert type
- ✅ Different tools for memory vs CPU issues
- ✅ Memory accumulates findings across investigations
- ✅ Investigation count increments

---

**Test 3: Pod Crash Alert**

```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type": "pod_crash", "service": "auth-service"}'
```

**Expected Response:**
```json
{
  "alert": {
    "type": "pod_crash",
    "service": "auth-service"
  },
  "plan": [
    "check_pods",
    "get_logs",
    "check_events"
  ],
  "investigation": [
    {
      "tool": "check_pods",
      "result": "Found 2 pods for auth-service: 1 running, 1 CrashLoopBackOff"
    },
    {
      "tool": "get_logs",
      "result": "Last 10 lines from crashed pod: FATAL: Database connection failed"
    },
    {
      "tool": "check_events",
      "result": "Recent events: Error: BackOff restarting failed container"
    }
  ],
  "memory_snapshot": {
    "last_alert": {
      "type": "pod_crash",
      "service": "auth-service"
    },
    "findings": [
      "Connection pool exhaustion found in logs",
      "High memory on pod-456",
      "OOMKilled event detected",
      "CrashLoopBackOff detected",
      "Database connection failure"
    ],
    "total_investigations": 3
  }
}
```

**What this validates:**
- ✅ Agent handles different alert types
- ✅ Each alert type triggers appropriate tools
- ✅ Memory persists across multiple investigations
- ✅ Findings accumulate and provide historical context

---

### Step 5: Test Health Endpoint

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "agent": "SimpleAgent",
  "tools_available": 4,
  "memory_size": 3
}
```

**What this validates:**
- ✅ Health check endpoint works
- ✅ Agent is initialized
- ✅ Tools are registered
- ✅ Memory is tracking investigations

---

### Step 6: View Agent Logs

Check the terminal where uvicorn is running. You should see:

```
INFO:     127.0.0.1:xxxxx - "POST /alerts HTTP/1.1" 200 OK
INFO:     Agent received alert: high_cpu for payment-api
INFO:     Generated plan: ['check_pods', 'get_logs', 'get_metrics']
INFO:     Executing tool: check_pods
INFO:     Executing tool: get_logs
INFO:     Executing tool: get_metrics
INFO:     Investigation complete, stored in memory
```

---

### Step 7: Run Unit Tests

In a new terminal (or stop uvicorn with Ctrl+C):

```bash
cd lab-04.1-first-ai-agent-free/app
source .venv/bin/activate
pytest -v
```

**Expected Output:**
```
================== test session starts ==================
platform linux -- Python 3.11.x, pytest-7.4.x
collected 8 items

tests/test_main.py::test_health_endpoint PASSED        [12%]
tests/test_main.py::test_alerts_endpoint PASSED        [25%]
tests/test_agent.py::test_agent_planning PASSED        [37%]
tests/test_agent.py::test_agent_execution PASSED       [50%]
tests/test_tools.py::test_check_pods_tool PASSED       [62%]
tests/test_tools.py::test_get_logs_tool PASSED         [75%]
tests/test_memory.py::test_memory_storage PASSED       [87%]
tests/test_memory.py::test_memory_retrieval PASSED     [100%]

=================== 8 passed in 0.45s ===================
```

**Run specific test suites:**

**Test agent behavior:**
```bash
pytest tests/test_agent.py -v
```

**Expected Output:**
```
tests/test_agent.py::test_agent_planning PASSED
tests/test_agent.py::test_agent_execution PASSED

Test details:
  test_agent_planning:
    - Validates plan generation for different alert types
    - Ensures correct tools are selected
    ✓ PASSED

  test_agent_execution:
    - Validates full investigation workflow
    - Ensures all tools execute correctly
    - Verifies memory storage
    ✓ PASSED
```

**Test tools:**
```bash
pytest tests/test_tools.py -v
```

**Expected Output:**
```
tests/test_tools.py::test_check_pods_tool PASSED
tests/test_tools.py::test_get_logs_tool PASSED

Test details:
  test_check_pods_tool:
    - Validates pod checking returns expected format
    - Tests with different service names
    ✓ PASSED

  test_get_logs_tool:
    - Validates log retrieval simulation
    - Tests error scenarios in logs
    ✓ PASSED
```

**Test memory:**
```bash
pytest tests/test_memory.py -v
```

**Expected Output:**
```
tests/test_memory.py::test_memory_storage PASSED
tests/test_memory.py::test_memory_retrieval PASSED

Test details:
  test_memory_storage:
    - Validates storing alerts and findings
    - Tests memory persistence across calls
    ✓ PASSED

  test_memory_retrieval:
    - Validates snapshot generation
    - Tests finding retrieval
    ✓ PASSED
```

---

### Step 8: Deploy to Kubernetes

Now that local testing works, deploy to Kubernetes.

**Navigate to lab root:**
```bash
cd .. # Back to lab-04.1-first-ai-agent-free/
```

**Create kind cluster:**
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
```

**Verify cluster:**
```bash
kubectl get nodes
```

**Expected Output:**
```
NAME                      STATUS   ROLES           AGE   VERSION
mcp-cluster-control-plane Ready    control-plane   45s   v1.30.0
```

---

### Step 9: Build and Load Docker Image

**Build the image:**
```bash
docker build -t free-agent-lab-4-1:v1 .
```

**Expected Output:**
```
[+] Building 28.5s (13/13) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 345B
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/python:3.11-slim
 => [1/7] FROM docker.io/library/python:3.11-slim
 => [2/7] WORKDIR /app
 => [3/7] COPY app/requirements.txt .
 => [4/7] RUN pip install --no-cache-dir -r requirements.txt
 => [5/7] COPY app/ .
 => [6/7] RUN useradd -m agentuser && chown -R agentuser:agentuser /app
 => [7/7] USER agentuser
 => exporting to image
 => => exporting layers
 => => writing image sha256:abc123...
 => => naming to docker.io/library/free-agent-lab-4-1:v1
```

**Verify image:**
```bash
docker images | grep free-agent-lab-4-1
```

**Expected Output:**
```
free-agent-lab-4-1   v1      abc123def456   2 minutes ago   245MB
```

**Load into kind:**
```bash
kind load docker-image free-agent-lab-4-1:v1 --name mcp-cluster
```

**Expected Output:**
```
Image: "free-agent-lab-4-1:v1" with ID "sha256:abc123..." not yet present on node "mcp-cluster-control-plane", loading...
```

**Verify in kind:**
```bash
docker exec -it mcp-cluster-control-plane crictl images | grep free-agent
```

---

### Step 10: Deploy to Kubernetes

**Create namespace:**
```bash
kubectl apply -f k8s/namespace.yaml
```

**Expected Output:**
```
namespace/ai-ml-lab-4-1 created
```

**Deploy agent:**
```bash
kubectl apply -f k8s/deployment.yaml
```

**Expected Output:**
```
deployment.apps/free-agent-lab-4-1 created
```

**Create service:**
```bash
kubectl apply -f k8s/service.yaml
```

**Expected Output:**
```
service/free-agent-lab-4-1 created
```

**Wait for pod to be ready:**
```bash
kubectl wait --for=condition=available --timeout=60s deployment/free-agent-lab-4-1 -n ai-ml-lab-4-1
```

**Expected Output:**
```
deployment.apps/free-agent-lab-4-1 condition met
```

---

### Step 11: Verify Kubernetes Deployment

**Check pods:**
```bash
kubectl get pods -n ai-ml-lab-4-1
```

**Expected Output:**
```
NAME                                 READY   STATUS    RESTARTS   AGE
free-agent-lab-4-1-xxxxxxxxxx-xxxxx  1/1     Running   0          45s
```

**Check service:**
```bash
kubectl get svc -n ai-ml-lab-4-1
```

**Expected Output:**
```
NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
free-agent-lab-4-1   ClusterIP   10.96.123.45    <none>        8000/TCP   50s
```

**Check logs:**
```bash
kubectl logs -n ai-ml-lab-4-1 -l app=free-agent --tail=20
```

**Expected Output:**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     SimpleAgent initialized with 4 tools
INFO:     Memory store created
INFO:     SafeExecutor initialized
```

---

### Step 12: Test Agent in Kubernetes

**Port-forward to access:**
```bash
kubectl port-forward -n ai-ml-lab-4-1 svc/free-agent-lab-4-1 8000:8000
```

**Expected Output:**
```
Forwarding from 127.0.0.1:8000 -> 8000
Forwarding from [::1]:8000 -> 8000
```

**In another terminal, test health:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "agent": "SimpleAgent",
  "tools_available": 4,
  "memory_size": 0
}
```

**Send test alert:**
```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"high_memory","service":"web-app"}'
```

**Expected:** Same structured response as local testing

**Check agent logs:**
```bash
kubectl logs -n ai-ml-lab-4-1 -l app=free-agent --tail=10
```

**Expected Output:**
```
INFO:     127.0.0.1:xxxxx - "GET /health HTTP/1.1" 200 OK
INFO:     Agent received alert: high_memory for web-app
INFO:     Generated plan: ['check_pods', 'get_metrics', 'check_events']
INFO:     Investigation complete
INFO:     127.0.0.1:xxxxx - "POST /alerts HTTP/1.1" 200 OK
```

---

## ✅ Testing and Validation

### Test 1: Agent Planning Logic

**Test different alert types generate different plans:**

```bash
# CPU alert
curl -s -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"high_cpu","service":"test"}' | jq '.plan'

# Memory alert
curl -s -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"high_memory","service":"test"}' | jq '.plan'

# Crash alert
curl -s -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"pod_crash","service":"test"}' | jq '.plan'
```

**Expected:** Each returns different tool combinations

### Test 2: Memory Accumulation

**Send multiple alerts and verify memory grows:**

```bash
# Alert 1
curl -s -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"high_cpu","service":"svc1"}' | jq '.memory_snapshot.total_investigations'

# Alert 2
curl -s -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"high_memory","service":"svc2"}' | jq '.memory_snapshot.total_investigations'
```

**Expected Output:**
```
1
2
```

### Test 3: Tool Execution

**Verify all tools return valid results:**

```bash
curl -s -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"high_cpu","service":"test"}' | jq '.investigation[].tool'
```

**Expected Output:**
```
"check_pods"
"get_logs"
"get_metrics"
```

### Test 4: Error Handling

**Test with invalid alert type:**

```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"invalid_type","service":"test"}'
```

**Expected:** Agent handles gracefully with fallback plan

### Test 5: Concurrent Requests

**Send multiple alerts simultaneously:**

```bash
for i in {1..5}; do
  curl -s -X POST http://localhost:8000/alerts \
    -H "Content-Type: application/json" \
    -d "{\"type\":\"high_cpu\",\"service\":\"svc$i\"}" &
done
wait
```

**Expected:** All requests complete successfully

---

## 🎓 Understanding What You've Built

### Agent Decision Flow

**Input:** Alert
```json
{"type": "high_cpu", "service": "payment-api"}
```

**Step 1: Analysis**
```
Agent thinks: "CPU alert detected. Need to:
1. Check if pods are healthy
2. Look for errors in logs
3. Verify current resource usage"
```

**Step 2: Planning**
```python
plan = ["check_pods", "get_logs", "get_metrics"]
```

**Step 3: Execution**
```
For each tool in plan:
  - Get tool from registry
  - Execute with safe executor
  - Collect result
  - Handle any errors
```

**Step 4: Memory Storage**
```python
memory.store({
  "alert": {...},
  "findings": ["High CPU on pod-789", "Connection issue"]
})
```

**Step 5: Report Generation**
```json
{
  "alert": {...},
  "plan": [...],
  "investigation": [...],
  "memory_snapshot": {...}
}
```

### Why This is an "Agent"

**Autonomy:**
- Decides which tools to use
- Adapts plan based on alert type
- Operates without human intervention

**Reasoning:**
- Analyzes alert characteristics
- Generates appropriate response
- Learns from past investigations

**Tool Use:**
- Orchestrates multiple tools
- Handles tool failures gracefully
- Aggregates tool results

**Memory:**
- Stores investigation history
- Detects patterns over time
- Provides context for decisions

---

## 💰 Cost Analysis

### Running in KIND: $0/month

Completely free for development and learning.

### Cloud Deployment: $3-5/month

**Scenario:** Single agent pod, low traffic

**Specifications:**
- 0.25 CPU, 256Mi RAM
- 1 pod running 24/7
- Minimal request volume

**Monthly Cost:**
```
Compute: 0.25 CPU × 730 hrs × $0.04/hr = $7.30
With discounts/spot: ~$3-5/month
```

### Scaling Cost

**10 alerts/day:**
- Cost: $3-5/month
- Response time: < 1s

**1000 alerts/day:**
- May need 2-3 pods
- Cost: $10-15/month
- Horizontal scaling handles load

---

## 🔧 Troubleshooting

### Issue: Pod Not Starting

**Check pod status:**
```bash
kubectl describe pod -n ai-ml-lab-4-1 -l app=free-agent
```

**Common causes:**
- Image not loaded: `kind load docker-image free-agent-lab-4-1:v1 --name mcp-cluster`
- Resource constraints: Check node resources
- Configuration errors: Review deployment.yaml

### Issue: Agent Not Responding

**Check logs:**
```bash
kubectl logs -n ai-ml-lab-4-1 -l app=free-agent --tail=50
```

**Test connectivity:**
```bash
kubectl exec -n ai-ml-lab-4-1 -l app=free-agent -- curl localhost:8000/health
```

### Issue: Tests Failing

**Ensure correct directory:**
```bash
cd lab-04.1-first-ai-agent-free/app
pytest
```

**Reinstall dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
pytest
```

---

## 🧹 Cleanup

### Stop Local Agent

```bash
# If running uvicorn locally
# Press Ctrl+C in the terminal
```

### Remove Kubernetes Resources

```bash
kubectl delete namespace ai-ml-lab-4-1
```

### Delete kind Cluster

```bash
kind delete cluster --name mcp-cluster
```

### Clean Virtual Environment

```bash
cd lab-04.1-first-ai-agent-free/app
deactivate
rm -rf .venv
```

---

## 📊 Success Criteria Checklist

Your lab is complete when:

- [ ] Local agent runs successfully
- [ ] Can send alerts and receive reports
- [ ] Different alert types generate different plans
- [ ] Memory accumulates across investigations
- [ ] All unit tests pass
- [ ] Agent deploys to Kubernetes
- [ ] Pod is running and healthy
- [ ] Can access agent via port-forward
- [ ] Agent responds to alerts in K8s
- [ ] Logs show agent activity
- [ ] You understand agent vs traditional automation
- [ ] You can explain each component's role
- [ ] You understand the investigation workflow

---

## 📚 Next Steps

### Extend This Agent

**1. Add Real Kubernetes Integration:**
```python
from kubernetes import client, config

def check_pods_real(self, service):
    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces(
        label_selector=f"app={service}"
    )
    return [pod.metadata.name for pod in pods.items]
```

**2. Add Remediation Actions:**
```python
def restart_pod(self, pod_name):
    # Restart unhealthy pod
    pass

def scale_deployment(self, service, replicas):
    # Scale up/down
    pass
```

**3. Implement Pattern Detection:**
```python
def detect_patterns(self):
    # Analyze memory for recurring issues
    # Example: "payment-api has CPU issues every evening"
    pass
```

**4. Add Alerting:**
```python
def send_alert(self, severity, message):
    # Send to Slack, PagerDuty, etc.
    pass
```

---

## 🎉 Congratulations!

You've successfully built your first AI agent!

### What You've Mastered:

✅ **AI Agent Architecture** - Understanding autonomous systems  
✅ **Planning and Reasoning** - Dynamic decision-making  
✅ **Tool Orchestration** - Multi-step workflows  
✅ **Memory Systems** - Context retention  
✅ **Safe Execution** - Error handling and timeouts  
✅ **Kubernetes Deployment** - Agents as microservices  

You now have the foundation to build production AI agents!

Happy learning! 🚀🤖🔧
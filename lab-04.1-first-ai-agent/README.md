# Lab 4.1 FREE Version – Your First Infrastructure AI Agent
## Building an Autonomous Investigation Agent (Simple but Real)

---

## 🎯 What You Will Learn

### Core Concepts

By completing this lab, you will understand:

1. **What AI Agents Are** - Moving beyond chatbots to autonomous systems:
   - **Reasoning**: Ability to analyze problems and make decisions
   - **Planning**: Breaking complex tasks into steps
   - **Tool Use**: Interacting with external systems
   - **Memory**: Maintaining context across interactions
   - **Autonomy**: Acting without constant human guidance

2. **Infrastructure Investigation Patterns** - Real-world DevOps automation:
   - Automated alert response
   - Multi-step diagnostic workflows
   - Tool orchestration for infrastructure
   - Investigation result aggregation

3. **Agent Architecture Components** - The building blocks:
   - **Controller**: API layer receiving requests
   - **Agent Core**: Decision-making and planning logic
   - **Tool Registry**: Available capabilities
   - **Memory System**: Context retention
   - **Safe Executor**: Error-handling and sandboxing

4. **Difference from Traditional Automation**:
   - Traditional: Fixed if-then scripts
   - Agent: Dynamic reasoning and adaptation
   - Traditional: Single-step actions
   - Agent: Multi-step plans with feedback

### Practical Skills

You will be able to:

- ✅ Build a simple but functional AI agent
- ✅ Implement agent planning and reasoning patterns
- ✅ Create a tool registry for infrastructure operations
- ✅ Design safe tool execution with error handling
- ✅ Implement in-memory context storage
- ✅ Deploy agents as Kubernetes services
- ✅ Test agent behavior and tool interactions
- ✅ Debug agent decision-making flows

### Real-World Applications

**SREs and DevOps Engineers** will learn:
- How to automate incident investigation
- Building intelligent runbook automation
- Creating self-service diagnostic tools
- Reducing time to detection and resolution

**Platform Engineers** will learn:
- Agent-based infrastructure management
- Tool orchestration patterns
- Building operator-like behavior
- Extending Kubernetes capabilities

**ML Engineers** will learn:
- Practical AI agent implementation
- Integration of ML with operations
- Production agent deployment
- Agent observability patterns

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
- Basic understanding of Kubernetes (pods, deployments, services)
- Python programming fundamentals
- REST API concepts
- Basic DevOps practices (alerts, monitoring, logs)

### Verification Commands

```bash
# Check Docker
docker version

# Check kind
kind version

# Check kubectl
kubectl version --client

# Check Python
python3 --version

# Check curl
curl --version
```

---

## 🏗️ Architecture Overview

### What You're Building

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         Namespace: ai-ml-lab-4-1                      │  │
│  │                                                        │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │  Pod: free-agent-*                           │    │  │
│  │  │  ┌────────────────────────────────────────┐  │    │  │
│  │  │  │  FastAPI Controller (Port 8000)        │  │    │  │
│  │  │  │  ┌──────────────────────────────────┐  │  │    │  │
│  │  │  │  │  POST /alerts                    │  │  │    │  │
│  │  │  │  │  - Receives infrastructure alert │  │  │    │  │
│  │  │  │  │  - Validates payload             │  │  │    │  │
│  │  │  │  │  - Routes to agent               │  │  │    │  │
│  │  │  │  └──────────────┬───────────────────┘  │  │    │  │
│  │  │  │                 │                       │  │    │  │
│  │  │  │                 ▼                       │  │    │  │
│  │  │  │  ┌──────────────────────────────────┐  │  │    │  │
│  │  │  │  │  SimpleAgent (Core Logic)        │  │  │    │  │
│  │  │  │  │                                  │  │  │    │  │
│  │  │  │  │  1. Analyze alert                │  │  │    │  │
│  │  │  │  │  2. Generate plan                │  │  │    │  │
│  │  │  │  │  3. Execute investigation        │  │  │    │  │
│  │  │  │  │  4. Store in memory              │  │  │    │  │
│  │  │  │  │  5. Return report                │  │  │    │  │
│  │  │  │  │                                  │  │  │    │  │
│  │  │  │  │  Components:                     │  │  │    │  │
│  │  │  │  │  ├─ Planning Engine              │  │  │    │  │
│  │  │  │  │  ├─ Tool Orchestrator            │  │  │    │  │
│  │  │  │  │  ├─ Memory Manager               │  │  │    │  │
│  │  │  │  │  └─ Result Aggregator            │  │  │    │  │
│  │  │  │  └──────────────┬───────────────────┘  │  │    │  │
│  │  │  │                 │                       │  │    │  │
│  │  │  │      ┌──────────┴──────────┐           │  │    │  │
│  │  │  │      ▼                     ▼           │  │    │  │
│  │  │  │  ┌─────────────┐   ┌──────────────┐   │  │    │  │
│  │  │  │  │ Tool        │   │   Memory     │   │  │    │  │
│  │  │  │  │ Registry    │   │   Store      │   │  │    │  │
│  │  │  │  │             │   │              │   │  │    │  │
│  │  │  │  │ Available:  │   │ In-process:  │   │  │    │  │
│  │  │  │  │ - check_pods│   │ - Last alert │   │  │    │  │
│  │  │  │  │ - get_logs  │   │ - Findings   │   │  │    │  │
│  │  │  │  │ - get_metric│   │ - Patterns   │   │  │    │  │
│  │  │  │  └──────┬──────┘   └──────────────┘   │  │    │  │
│  │  │  │         │                              │  │    │  │
│  │  │  │         ▼                              │  │    │  │
│  │  │  │  ┌──────────────────────────────────┐  │  │    │  │
│  │  │  │  │  SafeExecutor                    │  │  │    │  │
│  │  │  │  │  - Error handling                │  │  │    │  │
│  │  │  │  │  - Timeout protection            │  │  │    │  │
│  │  │  │  │  - Result validation             │  │  │    │  │
│  │  │  │  └──────────────────────────────────┘  │  │    │  │
│  │  │  └────────────────────────────────────────┘  │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Agent Workflow

```
1. Alert Received
   ↓
2. Agent Analyzes Alert Type
   ↓
3. Generate Investigation Plan
   [
     "check_pods",
     "get_logs", 
     "get_metrics"
   ]
   ↓
4. Execute Each Tool
   ├─ check_pods → "3 pods running, 1 high CPU"
   ├─ get_logs → "ERROR: Connection timeout..."
   └─ get_metrics → "CPU: 95%, Memory: 60%"
   ↓
5. Store in Memory
   {
     "last_alert": {...},
     "findings": [...],
     "patterns": [...]
   }
   ↓
6. Return Investigation Report
   {
     "alert": {...},
     "plan": [...],
     "investigation": [...],
     "memory_snapshot": {...}
   }
```

---

## 📁 Repository Structure

```
lab-04.1-first-ai-agent-free/
├── README.md                   ← This file
├── setup.md                    ← Detailed setup guide
├── kind-mcp-cluster.yaml       ← Cluster configuration
├── Dockerfile                  ← Container image definition
├── app/
│   ├── main.py                 ← FastAPI application (API layer)
│   ├── agent.py                ← SimpleAgent class (core logic)
│   ├── tools.py                ← Tool registry + fake infra tools
│   ├── memory.py               ← In-process memory store
│   ├── executor.py             ← Safe tool executor
│   ├── alerts.py               ← Sample alert payloads
│   ├── requirements.txt        ← Python dependencies
│   └── tests/
│       ├── test_main.py        ← API endpoint tests
│       ├── test_agent.py       ← Agent behavior tests
│       ├── test_tools.py       ← Tool execution tests
│       └── test_memory.py      ← Memory system tests
└── k8s/
    ├── namespace.yaml          ← Namespace: ai-ml-lab-4-1
    ├── deployment.yaml         ← Agent deployment
    └── service.yaml            ← ClusterIP service
```

---

## 🚀 Quick Start Guide

### Option 1: Run Locally (Recommended First)

**Step 1: Navigate to app directory**
```bash
cd lab-04.1-first-ai-agent-free/app
```

**Step 2: Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Run the agent**
```bash
uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

**Step 5: Test with an alert**

In another terminal:
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
    "service": "payment-api",
    "timestamp": "2024-01-15T10:30:00Z"
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
      "result": "Last 10 lines from pod-789: ERROR: Connection pool exhausted..."
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
      "High CPU on pod-789",
      "Connection pool issue detected"
    ],
    "total_investigations": 1
  }
}
```

**What this validates:**
- ✅ Agent received and parsed alert
- ✅ Generated investigation plan
- ✅ Executed tools in sequence
- ✅ Stored findings in memory
- ✅ Returned structured report

---

### Option 2: Run on Kubernetes

**Step 1: Create kind cluster**
```bash
cd lab-04.1-first-ai-agent-free
kind create cluster --config kind-mcp-cluster.yaml
kubectl get nodes
```

**Step 2: Build Docker image**
```bash
docker build -t free-agent-lab-4-1:v1 .
```

**Step 3: Load image into kind**
```bash
kind load docker-image free-agent-lab-4-1:v1 --name mcp-cluster
```

**Step 4: Deploy to Kubernetes**
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

**Step 5: Verify deployment**
```bash
kubectl get pods -n ai-ml-lab-4-1
kubectl get svc -n ai-ml-lab-4-1
```

**Step 6: Port-forward to access**
```bash
kubectl port-forward -n ai-ml-lab-4-1 svc/free-agent-lab-4-1 8000:8000
```

**Step 7: Send alert**
```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"high_memory","service":"web-app"}'
```

---

## 🧪 Running Tests

### Local Testing

From the `app/` directory:

```bash
cd lab-04.1-first-ai-agent-free/app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

**Expected Output:**
```
================== test session starts ==================
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

### Test Individual Components

**Test agent only:**
```bash
pytest tests/test_agent.py -v
```

**Test tools only:**
```bash
pytest tests/test_tools.py -v
```

**Test memory only:**
```bash
pytest tests/test_memory.py -v
```

---

## 📊 Understanding Agent Components

### 1. SimpleAgent (agent.py)

The core agent logic:

```python
class SimpleAgent:
    def __init__(self):
        self.tools = ToolRegistry()
        self.memory = MemoryStore()
        self.executor = SafeExecutor()
    
    def investigate(self, alert):
        # 1. Generate plan based on alert type
        plan = self.generate_plan(alert)
        
        # 2. Execute each step
        results = []
        for tool_name in plan:
            result = self.executor.execute(
                self.tools.get(tool_name),
                alert
            )
            results.append(result)
        
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

**Key responsibilities:**
- Alert analysis
- Plan generation
- Tool orchestration
- Memory management
- Report generation

### 2. Tool Registry (tools.py)

Available infrastructure tools:

```python
class ToolRegistry:
    def __init__(self):
        self.tools = {
            "check_pods": self.check_pods,
            "get_logs": self.get_logs,
            "get_metrics": self.get_metrics,
            "check_events": self.check_events
        }
    
    def check_pods(self, service):
        # Simulated: Check pod status
        return f"Found 3 pods for {service}: 2 healthy, 1 degraded"
    
    def get_logs(self, service):
        # Simulated: Retrieve recent logs
        return f"Recent logs for {service}: ERROR: Connection timeout..."
    
    def get_metrics(self, service):
        # Simulated: Get current metrics
        return f"{service} metrics - CPU: 85%, Memory: 70%"
```

**Why simulated?**
- Focus on agent patterns, not integration complexity
- No need for actual Kubernetes API access
- Safe to experiment with
- Easy to understand and modify

### 3. Memory Store (memory.py)

Simple in-process memory:

```python
class MemoryStore:
    def __init__(self):
        self.data = {
            "last_alert": None,
            "findings": [],
            "patterns": []
        }
    
    def store(self, alert, findings):
        self.data["last_alert"] = alert
        self.data["findings"].extend(findings)
        self._detect_patterns()
    
    def snapshot(self):
        return {
            "last_alert": self.data["last_alert"],
            "findings": self.data["findings"][-5:],  # Last 5
            "total_investigations": len(self.data["findings"])
        }
```

**Memory capabilities:**
- Store recent alerts
- Track investigation findings
- Detect recurring patterns
- Provide context for decisions

### 4. Safe Executor (executor.py)

Error handling and safety:

```python
class SafeExecutor:
    def execute(self, tool_func, *args, **kwargs):
        try:
            # Execute with timeout
            result = self._run_with_timeout(
                tool_func, 
                *args, 
                timeout=30,
                **kwargs
            )
            return {
                "success": True,
                "result": result
            }
        except TimeoutError:
            return {
                "success": False,
                "error": "Tool execution timeout"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
```

**Safety features:**
- Timeout protection
- Exception catching
- Result validation
- Error reporting

---

## 🎓 Key Learning Outcomes

### Conceptual Understanding

After completing this lab, you understand:

✅ **Agent vs Traditional Automation:**
- **Traditional**: Fixed scripts, predetermined steps
- **Agent**: Dynamic planning, adaptive execution

✅ **Agent Architecture Patterns:**
- Controller layer (API)
- Agent core (reasoning)
- Tool layer (capabilities)
- Memory layer (context)
- Executor layer (safety)

✅ **Investigation Workflows:**
- Alert reception
- Plan generation
- Tool orchestration
- Result aggregation
- Memory storage

✅ **Tool Design Principles:**
- Single responsibility
- Predictable outputs
- Error handling
- Idempotency

### Technical Skills

You can now:

✅ **Build AI agents** from scratch
✅ **Implement planning logic** for multi-step tasks
✅ **Create tool registries** for extensibility
✅ **Design memory systems** for context
✅ **Deploy agents** as Kubernetes services
✅ **Test agent behavior** systematically
✅ **Debug agent execution** flows

### Real-World Patterns

You've learned:

✅ **Incident automation** - Automated alert investigation
✅ **Runbook execution** - Tool orchestration patterns
✅ **Context retention** - Memory for better decisions
✅ **Safe execution** - Error handling and timeouts
✅ **Service deployment** - Agent as a microservice

---

## 💰 Cost Analysis

### Running in KIND: $0/month

This lab runs entirely locally with no cloud costs.

### If Deployed to Cloud: <$5/month

**Scenario:** Single agent pod, minimal traffic

**Specifications:**
- 1 pod with 0.25 CPU, 256Mi RAM
- Low request volume (< 100/day)
- No external dependencies

**Monthly Cost:**
```
Compute: 0.25 CPU × 730 hrs × $0.04/hr = $7.30
But with idle time discounts: ~$3-5/month

Storage (logs): $0.50
Total: $3.50-5.50/month
```

**Cost Optimization:**
- Use spot instances (save 60-80%)
- Set resource limits appropriately
- Implement request caching
- Use horizontal pod autoscaling

---

## 🔧 Troubleshooting

### Issue: Pod in ImagePullBackOff

**Cause:** Image not loaded into kind cluster

**Solution:**
```bash
kind load docker-image free-agent-lab-4-1:v1 --name mcp-cluster
kubectl delete pod -n ai-ml-lab-4-1 -l app=free-agent
```

### Issue: API Not Reachable

**Check service:**
```bash
kubectl get svc -n ai-ml-lab-4-1
kubectl describe svc free-agent-lab-4-1 -n ai-ml-lab-4-1
```

**Check port-forward:**
```bash
# Kill existing port-forward
pkill -f "port-forward"

# Restart
kubectl port-forward -n ai-ml-lab-4-1 svc/free-agent-lab-4-1 8000:8000
```

### Issue: Tests Failing

**Check working directory:**
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

### Issue: Agent Returns Errors

**Check logs:**
```bash
kubectl logs -n ai-ml-lab-4-1 -l app=free-agent --tail=50
```

**Test locally:**
```bash
cd app
python3 -m main
# In another terminal, send test alert
```

---

## 🧹 Cleanup

### Remove Kubernetes Resources

```bash
kubectl delete namespace ai-ml-lab-4-1
```

### Delete kind Cluster

```bash
kind delete cluster --name mcp-cluster
```

### Clean Local Environment

```bash
cd lab-04.1-first-ai-agent-free/app
deactivate  # Exit virtualenv
rm -rf .venv
```

---

## 📚 Next Steps

### Extend This Agent

**1. Add More Tools:**
```python
def restart_pod(self, service):
    # Restart unhealthy pods
    return f"Restarted pod for {service}"

def scale_deployment(self, service, replicas):
    # Scale up/down
    return f"Scaled {service} to {replicas} replicas"
```

**2. Improve Planning:**
```python
def generate_advanced_plan(self, alert):
    # More sophisticated planning based on alert type
    if alert["type"] == "high_cpu":
        return ["check_pods", "get_metrics", "get_logs", "check_events"]
    elif alert["type"] == "high_memory":
        return ["check_pods", "get_metrics", "check_memory_leaks"]
```

**3. Add Persistent Memory:**
```python
# Replace in-memory store with file or database
self.memory = PersistentMemoryStore(file_path="/data/memory.json")
```

**4. Implement Learning:**
```python
def detect_patterns(self):
    # Analyze past investigations
    # Identify common issues
    # Suggest preventive actions
```

### Explore PAID Version

The PAID version adds:
- **LLM-based planning** (GPT-4, Claude)
- **Real memory layers** (working, episodic, semantic)
- **Database integration** (Redis, Postgres, Vector DB)
- **Tool sandboxing** (isolated execution)
- **OpenTelemetry** (full observability)
- **Production features** (auth, rate limiting, monitoring)

---

## 🎉 Congratulations!

You've successfully built your first AI agent!

### What You've Mastered:

✅ **AI Agent Fundamentals** - Understanding autonomous systems  
✅ **Agent Architecture** - Controller, core, tools, memory, executor  
✅ **Tool Orchestration** - Multi-step investigation workflows  
✅ **Memory Systems** - Context retention and pattern detection  
✅ **Safe Execution** - Error handling and timeouts  
✅ **Kubernetes Deployment** - Agents as microservices  

### Real-World Impact:

These patterns power:
- **Automated incident response** at tech companies
- **Self-healing infrastructure** systems
- **Intelligent runbook automation**
- **DevOps copilots** and assistants

You now have the foundation to build production AI agents!

Happy learning! 🚀🤖🔧
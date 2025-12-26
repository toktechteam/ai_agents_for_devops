# Lab 05.2 — AutoGen Multi-Agent Incident Workflow (Kubernetes)

[![Lab](https://img.shields.io/badge/Lab-05.2-blue.svg)](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-05.2-autogen-workflow)
[![Chapter](https://img.shields.io/badge/Chapter-5-orange.svg)](https://theopskart.gumroad.com/l/AIAgentsforDevOps)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Chapter 5: Agent Frameworks and Platforms**

This lab is part of **Chapter 5** of the eBook **AI Agents for DevOps**.

---

## 🎯 What This Lab Teaches

This lab demonstrates **AutoGen-style multi-agent execution** from an operations and infrastructure perspective, not from a UI or API perspective.

> **If Lab 5.1 showed agents as services,**  
> **👉 Lab 5.2 shows agents as workers.**

This lab intentionally behaves differently from traditional microservices.

---

## 📚 Core Concepts (Directly Mapped to Chapter 5)

### 1️⃣ AutoGen-Style Agents Are Task-Oriented, Not Servers

From Chapter 5:

> "Autonomous frameworks behave more like research jobs than web services."

**This lab proves that statement in practice.**

Each agent pod:
- Executes a mission (incident investigation)
- Produces a result
- Terminates cleanly

**There is:**
- ❌ No API server
- ❌ No long-running process
- ❌ No request loop

**This execution model is commonly used for:**
- Incident responders
- Root-cause analysis agents
- Code-review agents
- One-shot remediation agents

> ✔ This is expected behavior  
> ✔ This is production-accurate behavior

---

### 2️⃣ Scaling Means Parallel Executions — Not Load Balancing

When you scale this deployment:

```bash
kubectl scale deployment autogen-agent --replicas=2
```

**You do NOT get:**
- ❌ Traffic splitting
- ❌ Request routing
- ❌ Shared sessions

**Instead, you get:**
```
Pod A → runs workflow → completes
Pod B → runs workflow → completes
```

**That means:**
- **Horizontal scaling = parallel agent runs**
- **NOT load-balanced services**

> This is a core AutoGen pattern and exactly what Chapter 5 describes for multi-agent systems.

---

### 3️⃣ Logs Prove Real Multi-Agent Collaboration

Each execution shows multiple agents collaborating:

- **Commander Agent** → planning & delegation
- **Investigator Agent** → analysis & recommendation

From Chapter 5:

> "AutoGen orchestrates multiple specialized agents collaborating toward a goal."

✔ Proven by real execution  
✔ No mocks  
✔ No fake diagrams

---

## 🏗️ Architecture Overview

```
Kubernetes Pod
┌──────────────────────────────┐
│  Commander Agent              │
│  - Reads alert                │
│  - Creates investigation plan │
│  - Delegates task             │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  Investigator Agent           │
│  - Analyzes symptoms          │
│  - Determines root cause      │
│  - Suggests remediation       │
└──────────────┬───────────────┘
               │
               ▼
     Workflow Result (Logs)
```

**The workflow runs once per pod, then exits.**

---

## 📁 Repository Structure

```
lab-05.2-autogen-workflow/
├── README.md                   ← This file
├── setup.md                    ← Detailed setup guide
├── Dockerfile                  ← Container image definition
├── app/
│   ├── workflow.py             ← AutoGen multi-agent workflow
│   ├── agents.py               ← Commander and Investigator agents
│   ├── alert.py                ← Alert data structure
│   └── requirements.txt        ← Python dependencies
└── k8s/
    ├── namespace.yaml          ← Namespace: autogen
    └── deployment.yaml         ← Agent deployment (job-style)
```

---

## 🚀 How to Run the Lab

### Step 1: Deploy the Agent

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
```

**Verify pod creation:**
```bash
kubectl get pods -n autogen
```

**Expected output:**
```
NAME                              READY   STATUS      RESTARTS   AGE
autogen-agent-xxxxx              0/1     Completed   0          30s
```

> Note: `STATUS: Completed` is **expected and correct** (see explanation below)

---

### Step 2: View Execution Output

```bash
kubectl logs -n autogen -l app=autogen-agent
```

**✅ Expected Output (Real Output):**
```
=== INCIDENT WORKFLOW RESULT ===
Alert: High CPU alert on payment-service
Commander: Investigation plan created. Delegating root cause analysis to SRE Investigator.
Investigator: Analysis complete. High CPU observed due to traffic spike. Recommend scaling replicas and enabling HPA.
```

**What this confirms:**
- ✔ Multi-agent workflow executed successfully
- ✔ Agents collaborated
- ✔ Workflow completed cleanly

---

## 🧪 How to Properly Test This Lab

This lab is tested by **observing execution**, not by calling endpoints.

### ✅ Test 1 — Single Execution

```bash
kubectl apply -f k8s/deployment.yaml
kubectl logs -n autogen -l app=autogen-agent
```

**What this proves:**
- Workflow runs end-to-end
- Agents collaborate correctly
- Execution completes successfully

---

### ✅ Test 2 — Parallel Execution (Horizontal Scaling)

```bash
kubectl scale deployment autogen-agent -n autogen --replicas=2
kubectl get pods -n autogen
kubectl logs -n autogen -l app=autogen-agent
```

**Expected behavior:**
Same workflow output printed twice, one execution per pod.

**Example output:**
```
=== INCIDENT WORKFLOW RESULT ===
Alert: High CPU alert on payment-service
...
=== INCIDENT WORKFLOW RESULT ===
Alert: High CPU alert on payment-service
...
```

**What this proves:**
- Scaling creates **parallel agent runs**
- AutoGen does **not load-balance requests**
- Each agent execution is **independent**

---

### ✅ Test 3 — Restart Behavior (Stateless Agents)

```bash
kubectl delete pod -n autogen -l app=autogen-agent
kubectl get pods -n autogen
kubectl logs -n autogen -l app=autogen-agent
```

**Expected behavior:**
- Workflow runs again
- Fresh execution from scratch

**What this proves:**
- Agents are **stateless**
- Executions are **reproducible**
- No hidden state or session coupling

---

## ⚠️ Why Pods Show "Completed" (This Is Correct)

After execution, pods show:
```
STATUS: Completed
```

**This is intentional.**

**Reason:**
1. The agent finishes its task
2. The process exits
3. Kubernetes marks the pod as completed

> This is **job-style execution**, not a service.

---

## 🚫 What This Lab Is NOT (Read Carefully)

This lab is NOT:

- ❌ A REST API
- ❌ A FastAPI service
- ❌ A long-running controller
- ❌ A load-balanced microservice

**Those patterns come later.**

**This lab focuses on:**
> Agent execution models, not request handling.

---

## 📊 Lab Comparison

| Lab | Focus | Pattern |
|-----|-------|---------|
| **Lab 5.1** | LangChain | Single agent, service-style |
| **Lab 5.2** | AutoGen | Multi-agent, workflow-style |

> **This lab is the pivot point of Chapter 5.**

---

## 🎓 Key Learning Outcomes

After completing this lab, you should clearly understand:

| Concept | Understanding |
|---------|---------------|
| **Execution Model** | AutoGen agents run like batch jobs |
| **Scaling Model** | Horizontal scaling = parallel executions |
| **Multi-Agent** | Agents collaborate within single workflow |
| **State Model** | Stateless, reproducible executions |
| **Completion** | Pods complete and exit (not crash) |
| **Production Use** | Ideal for incident response workflows |

---

## 💰 Cost Analysis

### Running in Kubernetes

**Single execution:**
- Pod runs for ~5-10 seconds
- CPU: 0.1 cores
- Memory: 128Mi
- Cost: ~$0.0001 per run

**1000 executions/month:**
```
1000 runs × 10 seconds = ~2.8 hours of compute
0.1 CPU × 2.8 hours × $0.04/hour = $0.011
Total: ~$0.01/month
```

**Cost optimization:**
- Use spot instances for 60-80% savings
- Batch multiple incidents into single runs
- Implement workflow caching for repeated patterns

---

## 🔧 Troubleshooting

### Issue: Pod Shows CrashLoopBackOff

**This means the workflow failed, not that the pattern is wrong.**

**Check logs:**
```bash
kubectl logs -n autogen -l app=autogen-agent
```

**Common causes:**
- Missing dependencies
- Syntax errors in workflow
- Configuration issues

**Solution:**
```bash
# Rebuild image with fixes
docker build -t autogen-agent:v2 .
kind load docker-image autogen-agent:v2

# Redeploy
kubectl delete deployment autogen-agent -n autogen
kubectl apply -f k8s/deployment.yaml
```

---

### Issue: No Logs Appearing

**Check pod status:**
```bash
kubectl get pods -n autogen
kubectl describe pod -n autogen -l app=autogen-agent
```

**Verify pod completed:**
```bash
kubectl logs -n autogen -l app=autogen-agent --tail=100
```

**If logs are empty:**
- Pod may still be initializing
- Check for ImagePullBackOff
- Verify image exists in cluster

---

### Issue: Scaling Doesn't Create Multiple Outputs

**Check replica count:**
```bash
kubectl get deployment autogen-agent -n autogen
```

**Verify multiple pods exist:**
```bash
kubectl get pods -n autogen
```

**Check all pod logs:**
```bash
kubectl logs -n autogen -l app=autogen-agent --all-containers=true
```

---

## 🧹 Cleanup

### Remove Lab Resources

```bash
kubectl delete namespace autogen
```

### Verify Cleanup

```bash
kubectl get namespaces | grep autogen
kubectl get pods --all-namespaces | grep autogen
```

---

## 📚 Next Steps

### Extend This Lab

**1. Add More Agents:**
```python
# Add a Remediator Agent
class RemediatorAgent:
    def execute_remediation(self, recommendation):
        # Implement auto-remediation
        return "Scaled deployment to 5 replicas"
```

**2. Make It Persistent:**
```python
# Store workflow results in database
import psycopg2

def store_result(workflow_result):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO workflows VALUES (%s)", [workflow_result])
```

**3. Add Real Kubernetes Integration:**
```python
# Use kubernetes client
from kubernetes import client, config

def get_pod_status(service_name):
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace="default", label_selector=f"app={service_name}")
    return [pod.metadata.name for pod in pods.items]
```

**4. Implement Workflow Orchestration:**
```python
# Use Argo Workflows for complex orchestration
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: autogen-incident-response
spec:
  entrypoint: investigate
  templates:
  - name: investigate
    steps:
    - - name: commander
        template: commander-step
    - - name: investigator
        template: investigator-step
```

---

## 🎉 Congratulations!

You've successfully understood AutoGen-style multi-agent workflows!

### What You've Mastered:

✅ **Task-oriented agents** - Workers, not servers  
✅ **Job-style execution** - Run to completion pattern  
✅ **Multi-agent collaboration** - Commander + Investigator pattern  
✅ **Parallel execution** - Scaling = more workers  
✅ **Stateless workflows** - Reproducible executions  
✅ **Production patterns** - Real incident response automation

### Real-World Impact:

These patterns power:
- **Automated incident response** workflows
- **Root cause analysis** systems
- **Code review** automation
- **Security investigation** agents
- **Infrastructure remediation** workflows

---

## 🧠 Final Takeaway

> **AutoGen agents are workers, not servers.**  
> **Kubernetes runs them exactly how it runs batch jobs — and that's the point.**

**This lab doesn't just "run" —  
it teaches how agent platforms really behave in production.**

---

## 📦 Repository Location

This lab lives here:

👉 [github.com/toktechteam/ai_agents_for_devops/tree/main/lab-05.2-autogen-workflow](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-05.2-autogen-workflow)

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

- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [AutoGen Multi-Agent Patterns](https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat)
- [Kubernetes Jobs Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [Argo Workflows](https://argoproj.github.io/argo-workflows/)

---

## ✅ Success Checklist

You are done when:

- ✅ Workflow logs appear
- ✅ Multiple agents are visible in logs
- ✅ Pods complete successfully
- ✅ Scaling creates parallel executions
- ✅ You understand why this is not a service

---

Copyright © 2024 TokTechTeam. See [LICENSE](../LICENSE) for details.
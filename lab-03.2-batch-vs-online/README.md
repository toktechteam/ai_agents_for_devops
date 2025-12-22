# Lab 03.2 — Batch vs Online AI Workloads: Batch Inference with Kubernetes Jobs

[![Lab](https://img.shields.io/badge/Lab-03.2-blue.svg)](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-03.2-batch-vs-online)
[![Chapter](https://img.shields.io/badge/Chapter-3-orange.svg)](https://theopskart.gumroad.com/l/AIAgentsforDevOps)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This lab is part of **Chapter 3** of the eBook **AI Agents for DevOps**.

---

## 🎯 What You Will Learn

### Core Concepts

By completing this lab, you will understand:

1. **Batch vs Online Inference** - The fundamental difference between two AI deployment patterns:
   - **Online inference**: Always-on API serving real-time predictions (Labs 1 & 2)
   - **Batch inference**: One-shot or scheduled jobs processing datasets and exiting

2. **When to Use Batch Inference**:
   - Processing large datasets overnight
   - Generating daily/weekly reports
   - Scoring customer data in bulk
   - Training data preprocessing
   - Model evaluation and testing

3. **Kubernetes Jobs** - How to run one-time tasks in Kubernetes:
   - Different from Deployments (which run continuously)
   - Job completion and success criteria
   - Resource management for batch workloads

4. **Kubernetes CronJobs** - How to schedule recurring batch tasks:
   - Cron syntax for scheduling
   - Managing scheduled job history
   - Monitoring scheduled executions

---

### Practical Skills

You will be able to:

- ✅ Design batch inference workflows for ML systems
- ✅ Deploy one-time batch jobs using Kubernetes Jobs
- ✅ Schedule recurring batch processing using CronJobs
- ✅ Monitor and debug batch job executions
- ✅ Retrieve and analyze batch job outputs from logs
- ✅ Understand cost implications of batch vs online inference

---

### Real-World Applications

**DevOps Engineers** will learn:
- How to deploy batch ML workloads in production
- When to choose batch over real-time inference
- How to schedule nightly model scoring jobs

**Data Engineers** will learn:
- How to productionize batch prediction pipelines
- Integration patterns for ML in data workflows
- Job monitoring and troubleshooting techniques

**ML Engineers** will learn:
- Deployment patterns for batch inference
- How to package batch prediction code for Kubernetes
- Cost-effective ML inference strategies

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
- Basic Kubernetes concepts (pods, jobs)
- Understanding of `kubectl apply`, `kubectl logs`, `kubectl get pods`
- Basic Python familiarity (helpful but not required)

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
```

---

## 🏗️ Architecture Overview

### What You're Building

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         Namespace: ai-ml-lab-3-1                      │  │
│  │                                                        │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │  Kubernetes Job (One-Time)                   │    │  │
│  │  │  ┌──────────────────────────────────────┐   │    │  │
│  │  │  │  Pod: batch-inference-once-xxxxx     │   │    │  │
│  │  │  │                                       │   │    │  │
│  │  │  │  1. Read input.jsonl                 │   │    │  │
│  │  │  │  2. Process each record              │   │    │  │
│  │  │  │  3. Compute predictions              │   │    │  │
│  │  │  │  4. Write to stdout                  │   │    │  │
│  │  │  │  5. Exit (Status: Completed)         │   │    │  │
│  │  │  └──────────────────────────────────────┘   │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  │                                                        │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │  Kubernetes CronJob (Scheduled)              │    │  │
│  │  │  Schedule: "*/2 * * * *" (every 2 minutes)  │    │  │
│  │  │  ┌──────────────────────────────────────┐   │    │  │
│  │  │  │  Job 1: batch-inference-xxxxx-1      │   │    │  │
│  │  │  │    → Pod (Completed)                  │   │    │  │
│  │  │  ├──────────────────────────────────────┤   │    │  │
│  │  │  │  Job 2: batch-inference-xxxxx-2      │   │    │  │
│  │  │  │    → Pod (Completed)                  │   │    │  │
│  │  │  ├──────────────────────────────────────┤   │    │  │
│  │  │  │  Job 3: batch-inference-xxxxx-3      │   │    │  │
│  │  │  │    → Pod (Running)                    │   │    │  │
│  │  │  └──────────────────────────────────────┘   │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Components

**1. Input Data (`input.jsonl`):**
```json
{"id": 1, "features": [1.0, 2.0, 3.0]}
{"id": 2, "features": [4.0, 5.0, 6.0]}
```

**2. Batch Job (`batch_job.py`):**
- Reads JSONL file
- Computes `prediction = sum(features)` for each record
- Outputs predictions as JSONL to stdout
- Exits with status 0 on success

**3. Kubernetes Job:**
- Runs the container **once**
- Pod completes and remains for log inspection
- Success criteria: Exit code 0

**4. Kubernetes CronJob:**
- Runs the same container on a schedule
- Creates new Jobs at specified intervals
- Maintains job history for auditing

---

## 📁 Repository Structure

```
lab-03.1-batch-vs-online/
├── README.md                  ← This file
├── setup.md                   ← Detailed setup guide
├── kind-mcp-cluster.yaml      ← Cluster configuration
├── Dockerfile                 ← Container image definition
├── app/
│   ├── batch_job.py           ← Batch inference logic
│   ├── requirements.txt       ← Python dependencies
│   ├── data/
│   │   └── input.jsonl        ← Sample dataset (2 records)
│   └── tests/
│       └── test_batch_job.py  ← Unit tests
└── k8s/
    ├── namespace.yaml         ← Namespace for isolation
    ├── job-batch-once.yaml    ← One-time batch job
    └── cronjob-batch.yaml     ← Scheduled batch job
```

---

## 🚀 Quick Start Guide

### Step 1: Navigate to Lab Directory

```bash
cd lab-03.1-batch-vs-online
```

### Step 2: Create kind Cluster

```bash
kind create cluster --config kind-mcp-cluster.yaml
```

Verify:
```bash
kubectl get nodes
```

**Expected Output:**
```
NAME                      STATUS   ROLES           AGE   VERSION
mcp-cluster-control-plane Ready    control-plane   30s   v1.30.0
```

---

### Step 3: Build Docker Image

```bash
docker build -t ai-lab-3-1-batch:v1 .
```

---

### Step 4: Load Image into kind

```bash
kind load docker-image ai-lab-3-1-batch:v1 --name mcp-cluster
```

---

### Step 5: Create Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

Verify:
```bash
kubectl get ns ai-ml-lab-3-1
```

---

### Step 6: Run One-Time Batch Job

```bash
kubectl apply -f k8s/job-batch-once.yaml
```

Check job status:
```bash
kubectl get jobs -n ai-ml-lab-3-1
kubectl get pods -n ai-ml-lab-3-1
```

Once completed, view logs:
```bash
POD_NAME=$(kubectl get pods -n ai-ml-lab-3-1 -o jsonpath='{.items[0].metadata.name}')
kubectl logs -n ai-ml-lab-3-1 "$POD_NAME"
```

**Expected Output:**
```json
{"id": 1, "prediction": 6.0}
{"id": 2, "prediction": 15.0}
{"summary": {"records": 2, "avg_prediction": 10.5}}
```

---

### Step 7: Run Scheduled Batch Job (CronJob)

```bash
kubectl apply -f k8s/cronjob-batch.yaml
```

Check CronJob:
```bash
kubectl get cronjobs -n ai-ml-lab-3-1
```

Wait a few minutes, then check jobs:
```bash
kubectl get jobs -n ai-ml-lab-3-1
kubectl get pods -n ai-ml-lab-3-1
```

View recent job logs:
```bash
POD_NAME=$(kubectl get pods -n ai-ml-lab-3-1 --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[-1].metadata.name}')
kubectl logs -n ai-ml-lab-3-1 "$POD_NAME"
```

---

## 📊 Understanding Batch vs Online Inference

### Online Inference (Previous Labs)

```
User Request → API (Always Running) → Prediction → User Response
              ↓
         Low Latency Required
         High Availability
         Continuous Resource Usage
```

**Characteristics:**
- Always-on service (Deployment)
- Real-time predictions
- Low latency requirements (< 100ms)
- Higher resource costs (24/7 running)
- Use cases: Web apps, mobile apps, real-time systems

---

### Batch Inference (This Lab)

```
Schedule → Job Starts → Process Dataset → Output Results → Job Ends
                       ↓
                  High Throughput
                  Lower Latency Requirements
                  Resources Used Only When Running
```

**Characteristics:**
- Job-based execution (Job/CronJob)
- Bulk predictions
- Higher latency acceptable (seconds to hours)
- Lower resource costs (pay only when running)
- Use cases: Nightly reports, bulk scoring, data preprocessing

---

### Cost Comparison

| Aspect | Online Inference | Batch Inference |
|--------|------------------|-----------------|
| **Deployment** | Kubernetes Deployment | Kubernetes Job/CronJob |
| **Resource Usage** | 24/7 continuous | Only when running |
| **Monthly Cost** | $30-100+ | $5-20 |
| **Latency** | <100ms | Seconds to hours OK |
| **Best For** | Real-time requests | Bulk processing |

---

## 🧪 Running Unit Tests

From the `app/` directory:

```bash
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

**Expected Output:**
```
================== test session starts ==================
collected 1 item

tests/test_batch_job.py .                    [100%]

=================== 1 passed in X.XXs ===================
```

**What the test validates:**
- ✅ Batch job can read JSONL input
- ✅ Predictions are calculated correctly
- ✅ Output format is valid JSONL
- ✅ Summary statistics are accurate

---

## 💰 Cost Analysis

### Running in KIND: $0/month

This lab runs entirely locally with no cloud costs.

---

### If Deployed to Cloud: <$10/month

**Assumptions:**
- CronJob runs every 2 hours (12 times/day)
- Each run takes 30 seconds
- Uses 0.25 CPU, 256Mi RAM

**Cost Breakdown:**
```
Monthly execution time: 12 runs/day × 30s × 30 days = 3 hours/month
Compute cost (0.25 CPU): ~$0.50-1.00
Storage (logs, data): ~$0.10-0.50
Total: $0.60-1.50/month
```

**Cost Optimization Tips:**
1. Use spot/preemptible instances (save 60-80%)
2. Batch multiple tasks into single runs
3. Compress output data
4. Set appropriate job retention policies
5. Use cheaper storage for input/output data

---

### Batch vs Online Cost Example

**Scenario:** Score 10,000 customers daily

**Option 1: Online API (Always-On)**
- 1 pod running 24/7
- Cost: ~$30-50/month
- Use case: Real-time scoring on demand

**Option 2: Batch Job (Nightly)**
- Job runs once at 2 AM, takes 10 minutes
- Cost: ~$1-2/month
- Use case: Daily customer scoring report

**Savings:** $28-48/month (93% reduction!)

---

## 🎓 Key Learning Outcomes

### Conceptual Understanding

After completing this lab, you understand:

✅ **When to use batch inference:**
- Large dataset processing
- Non-real-time requirements
- Cost-sensitive applications
- Scheduled reporting needs

✅ **When to use online inference:**
- Real-time user requests
- Low latency requirements
- Interactive applications
- Variable request patterns

✅ **Kubernetes job patterns:**
- Jobs run to completion (vs Deployments that run continuously)
- CronJobs enable scheduled automation
- Pods remain after job completion for log inspection
- Job history and cleanup policies

---

### Technical Skills

You can now:

✅ **Package batch ML code** for Kubernetes  
✅ **Deploy one-time jobs** for data processing  
✅ **Schedule recurring jobs** using CronJobs  
✅ **Monitor job execution** and retrieve outputs  
✅ **Debug failed jobs** using logs and events  
✅ **Optimize costs** by choosing appropriate patterns

---

### Production Patterns

You've learned:

✅ **Job completion criteria** - Exit codes and success conditions  
✅ **Output management** - Using stdout vs persistent storage  
✅ **Schedule syntax** - Cron expressions for job scheduling  
✅ **Resource limits** - Preventing runaway batch jobs  
✅ **History management** - Keeping job history for auditing

---

## 🔧 Troubleshooting

### Issue: Job Stuck in Pending

**Check events:**
```bash
kubectl describe job batch-inference-once -n ai-ml-lab-3-1
```

**Common causes:**
- Image not loaded into kind
- Insufficient cluster resources
- Node selector/affinity issues

**Solution:**
```bash
# Reload image
kind load docker-image ai-lab-3-1-batch:v1 --name mcp-cluster

# Check cluster resources
kubectl top nodes
```

---

### Issue: Pod Status = Error or CrashLoopBackOff

**Check logs:**
```bash
kubectl logs -n ai-ml-lab-3-1 <pod-name>
```

**Common causes:**
- Missing input file
- Python syntax errors
- Missing dependencies

**Solution:**
```bash
# Verify file is in image
docker run --rm ai-lab-3-1-batch:v1 ls -la /app/data/

# Test locally first
cd app
python batch_job.py
```

---

### Issue: CronJob Not Creating Jobs

**Check CronJob status:**
```bash
kubectl describe cronjob batch-inference-scheduled -n ai-ml-lab-3-1
```

**Common causes:**
- Invalid cron syntax
- CronJob suspended
- Schedule in wrong timezone

**Solution:**
```bash
# Verify cron schedule
kubectl get cronjob batch-inference-scheduled -n ai-ml-lab-3-1 -o yaml | grep schedule

# Manually trigger a job
kubectl create job --from=cronjob/batch-inference-scheduled manual-test -n ai-ml-lab-3-1
```

---

### Issue: Can't Find Pod Logs

**List all pods including completed:**
```bash
kubectl get pods -n ai-ml-lab-3-1 --show-all
```

**View logs from completed pod:**
```bash
kubectl logs -n ai-ml-lab-3-1 <completed-pod-name>
```

**If pod was deleted:**
- Jobs keep completed pods by default (for 6 hours)
- Check job's `ttlSecondsAfterFinished` setting
- Consider exporting logs to external storage

---

## 🧹 Cleanup

### Remove Lab Resources

```bash
# Delete CronJob
kubectl delete -f k8s/cronjob-batch.yaml

# Delete Job
kubectl delete -f k8s/job-batch-once.yaml

# Delete Namespace
kubectl delete -f k8s/namespace.yaml
```

### Delete kind Cluster

```bash
kind delete cluster --name mcp-cluster
```

Verify cleanup:
```bash
kubectl config get-contexts
kind get clusters
```

---

## 📚 Next Steps

### Extend This Lab

**1. Add Persistent Storage:**
- Save predictions to a file instead of stdout
- Use Kubernetes Volumes or PersistentVolumeClaims
- Learn about data persistence patterns

**2. Process Larger Datasets:**
- Modify `input.jsonl` to have 1000s of records
- Observe how job duration scales
- Implement progress logging

**3. Add Error Handling:**
- Handle malformed input gracefully
- Implement retry logic
- Send alerts on failure

**4. Export Results:**
- Write predictions to cloud storage (S3, GCS)
- Insert into database
- Trigger downstream workflows

---

### Advanced Topics

**1. Parallel Batch Jobs:**
- Use Job parallelism to process data faster
- Split dataset into chunks
- Aggregate results from multiple pods

**2. Job Dependencies:**
- Chain multiple jobs together
- Use workflow engines (Argo, Kubeflow)
- Implement complex data pipelines

**3. Monitoring & Alerting:**
- Track job success/failure rates
- Alert on job duration anomalies
- Create dashboards for batch metrics

---

## 🎉 Congratulations!

You've successfully completed Lab 3.1!

### What You've Mastered:

✅ **Batch vs Online Patterns** - Know when to use each approach  
✅ **Kubernetes Jobs** - Run one-time batch workloads  
✅ **Kubernetes CronJobs** - Schedule recurring tasks  
✅ **Cost Optimization** - Choose cost-effective deployment patterns  
✅ **Job Monitoring** - Debug and verify batch executions  

### Real-World Impact:

These patterns are used by companies for:
- **Netflix:** Nightly recommendation model scoring
- **Spotify:** Daily playlist generation
- **Uber:** Batch driver/rider matching optimization
- **Airbnb:** Periodic price predictions for listings

You now have the skills to deploy production batch ML workloads!

---

## 📦 Repository Location

This lab lives here:

👉 [github.com/toktechteam/ai_agents_for_devops/tree/main/lab-03.2-batch-vs-online](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-03.2-batch-vs-online)

---

## 📚 eBook Reference

This lab is explained in detail in **Chapter 3** of the eBook:

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

## 📖 Additional Resources

- [Kubernetes Jobs Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [Kubernetes CronJobs Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)
- [Cron Syntax Reference](https://crontab.guru/)
- [MLOps Batch Processing Best Practices](https://ml-ops.org/)

---

Copyright © 2024 TokTechTeam. See [LICENSE](../LICENSE) for details.
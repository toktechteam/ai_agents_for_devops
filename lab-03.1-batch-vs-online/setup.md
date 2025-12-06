# Lab 3.1 Setup Guide – Batch vs Online AI Workloads
## Batch Inference with Kubernetes Jobs

---

## 🎯 What You Will Achieve

By completing this setup, you will:

### Learning Objectives

1. **Understand Batch Processing Patterns** - Learn how batch inference differs from online/real-time inference
2. **Deploy Kubernetes Jobs** - Run one-time batch processing tasks
3. **Implement CronJobs** - Schedule recurring batch workloads
4. **Manage Job Lifecycles** - Monitor, debug, and retrieve outputs from batch jobs
5. **Optimize for Cost** - Understand when batch processing saves money compared to always-on services

### Expected Outcomes

- ✅ A working batch inference job that processes a dataset and exits
- ✅ A scheduled CronJob running batch predictions every 2 minutes
- ✅ Ability to retrieve and analyze batch job outputs from logs
- ✅ Understanding of when to use Jobs vs Deployments
- ✅ Cost awareness for batch vs online ML workloads

### Real-World Skills

**DevOps Engineers** will learn:
- How to productionize batch ML pipelines
- Job scheduling and automation in Kubernetes
- Debugging batch job failures

**Data Engineers** will learn:
- Containerizing data processing workflows
- Orchestrating batch prediction pipelines
- Output management strategies

**ML Engineers** will learn:
- Deploying batch inference workloads
- Choosing between batch and online inference
- Resource optimization for batch jobs

---

## 📋 Prerequisites

### Required Software

Verify you have these installed:

**1. Docker (24+)**
```bash
docker --version
```
Expected: `Docker version 24.x.x or higher`

**2. kind (Kubernetes in Docker)**
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

**5. Git**
```bash
git --version
```
Expected: `git version 2.x.x`

### Required Knowledge

- Basic Docker commands
- Basic Kubernetes concepts (pods, jobs)
- Understanding of `kubectl` CLI
- Familiarity with YAML configuration

---

## 🏗️ Understanding the Architecture

### What You're Building

This lab demonstrates **batch inference** - a pattern where:

1. **A job starts** when triggered (manually or on schedule)
2. **Reads input data** from a file or database
3. **Processes the data** through an ML model
4. **Outputs predictions** to stdout or storage
5. **Job completes** and pod remains for log inspection

### Comparison: Batch vs Online

**Online Inference (Labs 1-2):**
```
Deployment (Always Running)
    ↓
Pod (Restarts if fails)
    ↓
API Server (Waits for requests)
    ↓
Returns predictions in real-time
```

**Batch Inference (This Lab):**
```
Job (Runs Once) or CronJob (Runs on Schedule)
    ↓
Pod (Starts)
    ↓
Process entire dataset
    ↓
Output all predictions
    ↓
Pod (Completes and exits)
```

### Why This Matters

**Use Batch When:**
- Processing large datasets overnight
- Generating periodic reports (daily, weekly)
- Non-real-time predictions acceptable
- Cost optimization is important

**Use Online When:**
- Real-time user requests
- Low latency required (<100ms)
- Variable request patterns
- Interactive applications

---

## 🚀 Step-by-Step Setup

### Step 1: Navigate to Lab Directory

```bash
cd lab-03.1-batch-vs-online
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

### Step 2: Create kind Cluster

Create the cluster:
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

**Verify cluster is running:**
```bash
kubectl get nodes
```

**Expected Output:**
```
NAME                      STATUS   ROLES           AGE   VERSION
mcp-cluster-control-plane Ready    control-plane   30s   v1.30.0
```

**Verify kubectl context:**
```bash
kubectl config current-context
```

**Expected Output:**
```
kind-mcp-cluster
```

---

### Step 3: Examine the Batch Job Code

Before building, let's understand what the batch job does:

```bash
cat app/batch_job.py
```

**Key sections:**

1. **Read input data:**
```python
with open('/app/data/input.jsonl') as f:
    for line in f:
        record = json.loads(line)
```

2. **Compute predictions:**
```python
prediction = sum(record['features'])
```

3. **Output results:**
```python
print(json.dumps({"id": record['id'], "prediction": prediction}))
```

**View input data:**
```bash
cat app/data/input.jsonl
```

**Expected Content:**
```json
{"id": 1, "features": [1.0, 2.0, 3.0]}
{"id": 2, "features": [4.0, 5.0, 6.0]}
```

**Understanding the logic:**
- Record 1: prediction = 1.0 + 2.0 + 3.0 = 6.0
- Record 2: prediction = 4.0 + 5.0 + 6.0 = 15.0
- Average: (6.0 + 15.0) / 2 = 10.5

---

### Step 4: Build Docker Image

Build the batch job container:
```bash
docker build -t ai-lab-3-1-batch:v1 .
```

**Expected Output:**
```
[+] Building 25.3s (11/11) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 345B
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/python:3.11-slim
 => [1/5] FROM docker.io/library/python:3.11-slim
 => [2/5] WORKDIR /app
 => [3/5] COPY app/requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY app/ .
 => exporting to image
 => => exporting layers
 => => writing image sha256:xyz789...
 => => naming to docker.io/library/ai-lab-3-1-batch:v1
```

**Verify image was built:**
```bash
docker images | grep ai-lab-3-1-batch
```

**Expected Output:**
```
ai-lab-3-1-batch   v1      xyz789abc123   1 minute ago   195MB
```

---

### Step 5: Load Image into kind

Load the Docker image into the kind cluster:
```bash
kind load docker-image ai-lab-3-1-batch:v1 --name mcp-cluster
```

**Expected Output:**
```
Image: "ai-lab-3-1-batch:v1" with ID "sha256:xyz789..." not yet present on node "mcp-cluster-control-plane", loading...
```

**Verify image in kind:**
```bash
docker exec -it mcp-cluster-control-plane crictl images | grep ai-lab-3-1-batch
```

**Expected Output:**
```
docker.io/library/ai-lab-3-1-batch   v1      xyz789abc123   195MB
```

---

### Step 6: Create Namespace

Create dedicated namespace for isolation:
```bash
kubectl apply -f k8s/namespace.yaml
```

**Expected Output:**
```
namespace/ai-ml-lab-3-1 created
```

**Verify namespace:**
```bash
kubectl get namespace ai-ml-lab-3-1
```

**Expected Output:**
```
NAME            STATUS   AGE
ai-ml-lab-3-1   Active   10s
```

---

### Step 7: Deploy One-Time Batch Job

Apply the Job manifest:
```bash
kubectl apply -f k8s/job-batch-once.yaml
```

**Expected Output:**
```
job.batch/batch-inference-once created
```

**Check job status:**
```bash
kubectl get jobs -n ai-ml-lab-3-1
```

**Expected Output (initial):**
```
NAME                   COMPLETIONS   DURATION   AGE
batch-inference-once   0/1           3s         3s
```

**Check pod status:**
```bash
kubectl get pods -n ai-ml-lab-3-1
```

**Expected Output (while running):**
```
NAME                         READY   STATUS    RESTARTS   AGE
batch-inference-once-xxxxx   1/1     Running   0          5s
```

**Wait for completion:**
```bash
kubectl wait --for=condition=complete --timeout=60s job/batch-inference-once -n ai-ml-lab-3-1
```

**Expected Output:**
```
job.batch/batch-inference-once condition met
```

**Check final status:**
```bash
kubectl get pods -n ai-ml-lab-3-1
```

**Expected Output (completed):**
```
NAME                         READY   STATUS      RESTARTS   AGE
batch-inference-once-xxxxx   0/1     Completed   0          30s
```

**Understanding the status:**
- `STATUS: Completed` means the job ran successfully
- `READY: 0/1` is normal for completed pods
- Pod remains for log inspection

---

### Step 8: View Batch Job Output

Get the pod name:
```bash
POD_NAME=$(kubectl get pods -n ai-ml-lab-3-1 -o jsonpath='{.items[0].metadata.name}')
echo "Pod name: $POD_NAME"
```

View the logs:
```bash
kubectl logs -n ai-ml-lab-3-1 "$POD_NAME"
```

**Expected Output:**
```json
{"id": 1, "prediction": 6.0}
{"id": 2, "prediction": 15.0}
{"summary": {"records": 2, "avg_prediction": 10.5}}
```

**What this validates:**
- ✅ Job read input.jsonl successfully
- ✅ Predictions calculated correctly (1+2+3=6, 4+5+6=15)
- ✅ Summary statistics computed (avg = 10.5)
- ✅ Output formatted as JSONL
- ✅ Job completed successfully

---

### Step 9: Verify Job Details

Get detailed job information:
```bash
kubectl describe job batch-inference-once -n ai-ml-lab-3-1
```

**Look for these sections:**

**Completions:**
```
Completions:  1/1
```
This shows 1 pod completed successfully out of 1 required.

**Conditions:**
```
Conditions:
  Type    Status  Reason
  ----    ------  ------
  Complete True   <none>
```
This confirms the job completed successfully.

**Events:**
```
Events:
  Type    Reason            Age   Message
  ----    ------            ----  -------
  Normal  SuccessfulCreate  2m    Created pod: batch-inference-once-xxxxx
  Normal  Completed         1m    Job completed
```

---

### Step 10: Deploy CronJob

Apply the CronJob manifest:
```bash
kubectl apply -f k8s/cronjob-batch.yaml
```

**Expected Output:**
```
cronjob.batch/batch-inference-scheduled created
```

**Verify CronJob:**
```bash
kubectl get cronjobs -n ai-ml-lab-3-1
```

**Expected Output:**
```
NAME                        SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
batch-inference-scheduled   */2 * * * *   False     0        <none>          10s
```

**Understanding the schedule:**
- `*/2 * * * *` means "every 2 minutes"
- Cron format: `minute hour day-of-month month day-of-week`
- `SUSPEND: False` means the CronJob is active
- `ACTIVE: 0` means no job is currently running

**View CronJob details:**
```bash
kubectl describe cronjob batch-inference-scheduled -n ai-ml-lab-3-1
```

---

### Step 11: Wait for CronJob Execution

Wait for the first scheduled run (up to 2 minutes):
```bash
echo "Waiting for CronJob to create first job..."
sleep 130  # Wait just over 2 minutes
```

Check for created jobs:
```bash
kubectl get jobs -n ai-ml-lab-3-1
```

**Expected Output:**
```
NAME                              COMPLETIONS   DURATION   AGE
batch-inference-once              1/1           8s         5m
batch-inference-scheduled-xxxxx1  1/1           7s         45s
```

**Check all pods:**
```bash
kubectl get pods -n ai-ml-lab-3-1
```

**Expected Output:**
```
NAME                                    READY   STATUS      RESTARTS   AGE
batch-inference-once-xxxxx              0/1     Completed   0          5m
batch-inference-scheduled-xxxxx1-yyyyy  0/1     Completed   0          50s
```

---

### Step 12: View CronJob Output

Get the latest job's pod:
```bash
LATEST_POD=$(kubectl get pods -n ai-ml-lab-3-1 --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[-1].metadata.name}')
echo "Latest pod: $LATEST_POD"
```

View its logs:
```bash
kubectl logs -n ai-ml-lab-3-1 "$LATEST_POD"
```

**Expected Output:**
```json
{"id": 1, "prediction": 6.0}
{"id": 2, "prediction": 15.0}
{"summary": {"records": 2, "avg_prediction": 10.5}}
```

**What this validates:**
- ✅ CronJob created a job automatically
- ✅ Job ran successfully on schedule
- ✅ Output matches the one-time job
- ✅ Scheduled execution is working

---

### Step 13: Monitor Multiple CronJob Runs

Wait for another execution:
```bash
echo "Waiting for second CronJob execution..."
sleep 130
```

Check all jobs:
```bash
kubectl get jobs -n ai-ml-lab-3-1
```

**Expected Output:**
```
NAME                              COMPLETIONS   DURATION   AGE
batch-inference-once              1/1           8s         7m
batch-inference-scheduled-xxxxx1  1/1           7s         3m
batch-inference-scheduled-xxxxx2  1/1           6s         45s
```

**View job history:**
```bash
kubectl get jobs -n ai-ml-lab-3-1 --sort-by=.metadata.creationTimestamp
```

**What this validates:**
- ✅ CronJob creates new jobs on schedule
- ✅ Each job gets a unique name with timestamp
- ✅ Multiple jobs can coexist
- ✅ Jobs complete independently

---

### Step 14: Examine CronJob Job History

Check CronJob status:
```bash
kubectl get cronjob batch-inference-scheduled -n ai-ml-lab-3-1 -o wide
```

**Expected Output:**
```
NAME                        SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
batch-inference-scheduled   */2 * * * *   False     0        45s             5m
```

**View detailed history:**
```bash
kubectl describe cronjob batch-inference-scheduled -n ai-ml-lab-3-1
```

**Look for:**

**Last Schedule Time:**
```
Last Schedule Time:  Mon, 15 Jan 2024 10:30:00 -0800
```

**Active Jobs:**
```
Active Jobs:  <none>
```
(Should be none if current job completed)

**Events:**
```
Events:
  Type    Reason            Age   Message
  ----    ------            ----  -------
  Normal  SuccessfulCreate  5m    Created job batch-inference-scheduled-xxxxx1
  Normal  SawCompletedJob   5m    Saw completed job: batch-inference-scheduled-xxxxx1
  Normal  SuccessfulCreate  3m    Created job batch-inference-scheduled-xxxxx2
  Normal  SawCompletedJob   3m    Saw completed job: batch-inference-scheduled-xxxxx2
```

---

### Step 15: Test Manual Job Trigger

Create a one-off job from the CronJob template:
```bash
kubectl create job --from=cronjob/batch-inference-scheduled manual-test -n ai-ml-lab-3-1
```

**Expected Output:**
```
job.batch/manual-test created
```

**Check the job:**
```bash
kubectl get jobs -n ai-ml-lab-3-1 manual-test
```

**Wait for completion:**
```bash
kubectl wait --for=condition=complete --timeout=60s job/manual-test -n ai-ml-lab-3-1
```

**View logs:**
```bash
kubectl logs -n ai-ml-lab-3-1 job/manual-test
```

**What this validates:**
- ✅ Can manually trigger jobs from CronJob template
- ✅ Useful for testing without waiting for schedule
- ✅ Manual jobs behave identically to scheduled ones

---

## ✅ Testing and Validation

### Test 1: Verify Job Completion

```bash
kubectl get jobs -n ai-ml-lab-3-1 batch-inference-once
```

**Success criteria:**
- `COMPLETIONS` shows `1/1`
- No `AGE` indicates it's not still running

### Test 2: Verify Pod Exit Code

```bash
kubectl get pod -n ai-ml-lab-3-1 -l job-name=batch-inference-once -o jsonpath='{.items[0].status.containerStatuses[0].state.terminated.exitCode}'
```

**Expected Output:**
```
0
```

**What this means:**
- Exit code 0 = success
- Exit code > 0 = failure

### Test 3: Verify Output Format

```bash
POD_NAME=$(kubectl get pods -n ai-ml-lab-3-1 -l job-name=batch-inference-once -o jsonpath='{.items[0].metadata.name}')
kubectl logs -n ai-ml-lab-3-1 "$POD_NAME" | python3 -m json.tool
```

**Expected:** Valid JSON output with no errors

### Test 4: Verify CronJob Schedule

```bash
kubectl get cronjob batch-inference-scheduled -n ai-ml-lab-3-1 -o jsonpath='{.spec.schedule}'
```

**Expected Output:**
```
*/2 * * * *
```

### Test 5: Count CronJob Executions

```bash
kubectl get jobs -n ai-ml-lab-3-1 -l cronjob=batch-inference-scheduled --no-headers | wc -l
```

**Expected:** Number increases every 2 minutes

---

## 🧪 Running Unit Tests Locally

### Step 1: Navigate to App Directory

```bash
cd app
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed pytest-7.x.x
```

### Step 4: Run Tests

```bash
pytest -v
```

**Expected Output:**
```
================== test session starts ==================
platform linux -- Python 3.11.x, pytest-7.x.x
collected 1 item

tests/test_batch_job.py::test_batch_inference PASSED [100%]

=================== 1 passed in 0.05s ===================
```

### Step 5: Test Batch Job Locally

Run the batch job outside of Kubernetes:
```bash
python batch_job.py
```

**Expected Output:**
```json
{"id": 1, "prediction": 6.0}
{"id": 2, "prediction": 15.0}
{"summary": {"records": 2, "avg_prediction": 10.5}}
```

**What this validates:**
- ✅ Code runs correctly outside Kubernetes
- ✅ Can test changes locally before building image
- ✅ Faster development iteration

---

## 🎓 Understanding What You've Built

### Job Lifecycle

```
1. Job Created
   ↓
2. Pod Scheduled
   ↓
3. Container Starts
   ↓
4. Code Executes
   ↓
5. Container Exits (Code 0)
   ↓
6. Pod Status: Completed
   ↓
7. Job Status: Complete
```

### CronJob Lifecycle

```
CronJob Controller (Always Running)
   ↓
Checks Schedule Every Minute
   ↓
Time Matches Schedule?
   ├─ Yes → Create New Job
   └─ No → Wait
```

### Key Differences from Deployments

| Aspect | Deployment | Job | CronJob |
|--------|-----------|-----|---------|
| **Purpose** | Always-on service | One-time task | Scheduled task |
| **Restarts** | Always restarts | No restart on success | Creates new jobs |
| **Completion** | Never completes | Completes and exits | Each job completes |
| **Use Case** | Web APIs | Data migration | Daily reports |
| **Resource Usage** | Continuous | Duration of job | Sum of all job runs |

### When to Use Each Pattern

**Use Jobs when:**
- One-time data processing needed
- Database migration or initialization
- Batch scoring of existing dataset
- Testing or validation tasks

**Use CronJobs when:**
- Nightly model retraining
- Daily prediction generation
- Periodic data cleanup
- Scheduled report generation

**Use Deployments when:**
- Always-on API service
- Real-time predictions
- User-facing applications
- Continuous availability required

---

## 💰 Cost Analysis

### This Lab (KIND): $0/month

No cloud costs - everything runs locally.

### Cloud Deployment: <$10/month

**Scenario:** CronJob runs every 6 hours (4 times/day)

**Job specifications:**
- Runtime: 1 minute per execution
- CPU: 0.25 cores
- Memory: 256Mi

**Monthly calculation:**
```
Executions per month: 4/day × 30 days = 120 jobs
Total runtime: 120 jobs × 1 minute = 120 minutes = 2 hours

Compute cost (0.25 CPU, 2 hours):
  - GCP: $0.50-1.00
  - AWS: $0.60-1.20
  - Azure: $0.55-1.10

Storage (logs, minimal): $0.10-0.50

Total: $0.60-1.70/month
```

### Optimization Strategies

**1. Use Spot/Preemptible Instances:**
- Save 60-80% on compute costs
- Safe for batch jobs (can retry if preempted)
- Reduces cost to $0.20-0.50/month

**2. Optimize Schedule:**
```
Bad:  */5 * * * *    (every 5 min = 8,640/month)
Good: 0 2 * * *      (daily at 2 AM = 30/month)
Better: 0 2 * * 0    (weekly = 4/month)
```

**3. Batch Multiple Tasks:**
- Combine related jobs into single execution
- Reduces startup overhead
- Lowers total compute time

**4. Set Resource Limits:**
```yaml
resources:
  requests:
    cpu: "100m"      # Minimum needed
    memory: "128Mi"
  limits:
    cpu: "250m"      # Prevent runaway jobs
    memory: "256Mi"
```

---

## 🔧 Troubleshooting

### Issue: Job Never Completes

**Symptom:**
```bash
kubectl get jobs -n ai-ml-lab-3-1
# Shows COMPLETIONS as 0/1 for extended time
```

**Check pod status:**
```bash
kubectl get pods -n ai-ml-lab-3-1
```

**If STATUS is Error or CrashLoopBackOff:**
```bash
kubectl logs -n ai-ml-lab-3-1 <pod-name>
```

**Common causes:**
- Python script has errors
- Missing input file
- Dependencies not installed

**Solution:**
```bash
# Test locally first
cd app
python batch_job.py

# Check Dockerfile includes data
cat Dockerfile | grep COPY
```

---

### Issue: CronJob Not Creating Jobs

**Check CronJob status:**
```bash
kubectl describe cronjob batch-inference-scheduled -n ai-ml-lab-3-1
```

**Look for:**
- `Suspend: False` (should be False)
- `Active Jobs: <none>` (normal between runs)
- Events showing job creation

**Verify schedule:**
```bash
kubectl get cronjob batch-inference-scheduled -n ai-ml-lab-3-1 -o yaml | grep schedule
```

**Test with manual trigger:**
```bash
kubectl create job --from=cronjob/batch-inference-scheduled test-manual -n ai-ml-lab-3-1
```

---

### Issue: Can't Find Completed Pod

**List all pods including completed:**
```bash
kubectl get pods -n ai-ml-lab-3-1 --field-selector=status.phase=Succeeded
```

**Check job completion time:**
```bash
kubectl get job batch-inference-once -n ai-ml-lab-3-1 -o jsonpath='{.status.completionTime}'
```

**Note:** Pods are retained for 6 hours by default (`ttlSecondsAfterFinished: 21600`)

---

### Issue: Too Many Old Jobs

**Symptom:**
```bash
kubectl get jobs -n ai-ml-lab-3-1
# Shows many completed jobs
```

**CronJobs have history limits:**
```yaml
successfulJobsHistoryLimit: 3  # Keep last 3 successful
failedJobsHistoryLimit: 1      # Keep last 1 failed
```

**Manual cleanup:**
```bash
kubectl delete job -n ai-ml-lab-3-1 --field-selector=status.successful=1
```

---

## 🧹 Cleanup

### Step 1: Delete CronJob

```bash
kubectl delete -f k8s/cronjob-batch.yaml
```

**Expected Output:**
```
cronjob.batch "batch-inference-scheduled" deleted
```

**Verify:**
```bash
kubectl get cronjobs -n ai-ml-lab-3-1
```

**Expected:** No resources found

### Step 2: Delete One-Time Job

```bash
kubectl delete -f k8s/job-batch-once.yaml
```

**Expected Output:**
```
job.batch "batch-inference-once" deleted
```

### Step 3: Delete Manual Test Job (if created)

```bash
kubectl delete job manual-test -n ai-ml-lab-3-1
```

### Step 4: Verify All Jobs Deleted

```bash
kubectl get jobs -n ai-ml-lab-3-1
kubectl get pods -n ai-ml-lab-3-1
```

**Expected:** No resources found in both

### Step 5: Delete Namespace

```bash
kubectl delete -f k8s/namespace.yaml
```

**Expected Output:**
```
namespace "ai-ml-lab-3-1" deleted
```

**Verify:**
```bash
kubectl get namespace ai-ml-lab-3-1
```

**Expected:**
```
Error from server (NotFound): namespaces "ai-ml-lab-3-1" not found
```

### Step 6: Delete kind Cluster

```bash
kind delete cluster --name mcp-cluster
```

**Expected Output:**
```
Deleting cluster "mcp-cluster" ...
Deleted nodes: ["mcp-cluster-control-plane"]
```

**Verify:**
```bash
kind get clusters
```

**Expected:**
```
No kind clusters found.
```

---

## 📊 Success Criteria Checklist

Your lab is complete when:

- [ ] kind cluster created and running
- [ ] Docker image built successfully
- [ ] Image loaded into kind cluster
- [ ] Namespace `ai-ml-lab-3-1` created
- [ ] One-time Job completed successfully
- [ ] Job logs show correct predictions (6.0, 15.0, avg 10.5)
- [ ] CronJob created and active
- [ ] CronJob created at least 2 scheduled jobs
- [ ] All scheduled jobs completed successfully
- [ ] Can retrieve logs from any completed job
- [ ] Manual job trigger works
- [ ] Unit tests pass locally
- [ ] You understand batch vs online patterns
- [ ] You can explain when to use each pattern

---

## 📚 Next Steps

### Extend This Lab

**1. Process Larger Datasets:**
```bash
# Create bigger input file
cd app/data
for i in {1..1000}; do
  echo "{\"id\": $i, \"features\": [1.0, 2.0, 3.0]}" >> input_large.jsonl
done
```

**2. Add Parallel Processing:**
```yaml
spec:
  parallelism: 3        # Run 3 pods in parallel
  completions: 10       # Until 10 total completions
```

**3. Export to File Instead of Stdout:**
```python
with open('/output/predictions.json', 'w') as f:
    json.dump(results, f)
```

**4. Add Progress Logging:**
```python
if i % 100 == 0:
    print(f"Processed {i}/{total} records")
```

### Advanced Topics

**1. Use Init Containers:**
- Download data before main container starts
- Prepare workspace
- Validate prerequisites

**2. Add Sidecars for Monitoring:**
- Export metrics during job execution
- Push logs to external system
- Monitor resource usage

**3. Implement Retry Logic:**
```yaml
spec:
  backoffLimit: 3  # Retry up to 3 times
```

**4. Job Dependencies:**
- Use Argo Workflows
- Chain multiple jobs
- Build data pipelines

---

## 🎉 Congratulations!

You've successfully completed Lab 3.1 Setup!

### What You've Mastered:

✅ **Batch Processing Concepts** - Understand batch vs online patterns  
✅ **Kubernetes Jobs** - Deploy one-time batch workloads  
✅ **Kubernetes CronJobs** - Schedule recurring tasks  
✅ **Job Monitoring** - Retrieve outputs and debug failures  
✅ **Cost Optimization** - Choose cost-effective patterns  

### Real-World Applications:

These skills enable you to:
- Deploy nightly model scoring pipelines
- Automate periodic data processing
- Run cost-effective ML inference
- Build production batch ML systems

You're now equipped to handle batch ML workloads in production!

Happy learning! 🚀📊🎯
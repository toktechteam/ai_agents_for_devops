# Lab 03.1 — Setup & Execution Guide

This guide walks you through setting up and running **Lab 03.1 (Vector Similarity Search)** step by step.

Follow the steps in order. Do not skip observation notes.

---

## Environment prerequisites

### Recommended EC2 configuration (tested)

- **OS**: Ubuntu 22.04
- **Instance type**: `t3.medium`
  - 2 vCPU
  - 4 GB RAM
- **Disk**: 30 GB

Why this matters:
- Embedding models load into memory
- Smaller instances may hit memory limits
- This size gives stable performance for CPU-based embeddings

---

## Security Group configuration

If you want to test the API from browser or external tools:

- Allow **inbound port 8000** (optional)

> Note:  
> The lab works without opening port 8000 if you only test via CLI inside the instance.

---

## Step 1: Clone the lab repository

```bash
git clone https://github.com/toktechteam/ai_agents_for_devops.git
cd ai_agents_for_devops/lab-03.1-vector-similarity-search
```

---

## Step 2: Verify Docker

```bash
docker --version
docker compose version
```

(Optional) Create a local virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
```

---

## Step 3: Start the lab services

```bash
docker compose up --build
```

If you modify files and need a clean restart:

```bash
docker compose down -v
docker compose up --build -d
```

Verify containers:

```bash
docker ps
```

You should see:
- API container (port 8000)
- Qdrant container (port 6333)

---

## Step 4: Ingest data (important step)

Enter the API container:

```bash
docker exec -it lab-031-vector-similarity-search-api-1 bash
```

Run ingest:

```bash
python scripts/ingest.py
```

Expected output:

```
{'collection': 'runbooks', 'inserted': 5}
```

### What is happening here?

- Text runbooks are converted into embeddings
- Embeddings are stored in Qdrant
- This builds the semantic search index

---

## Step 5: Run semantic queries

Inside the same container:

```bash
python scripts/query.py "pods restarting crash loop"
```

### Expected behavior:

- Correct runbook appears at the top
- Results are ranked by similarity score
- Related operational issues appear with lower scores

---

## How to read similarity scores

- **Higher score** → closer meaning
- **Lower score** → weaker semantic relation

These scores are distance metrics, not confidence percentages.

In production systems, you:
- Set thresholds
- Filter noise
- Tune relevance

---

## Validation checklist (lab success)

You can consider the lab successful if:

- ✅ Ingest completes without errors
- ✅ Queries return meaningful results
- ✅ Different wording still finds the correct runbook
- ✅ Scores decrease as relevance decreases

---

## Common confusion (important)

- Scripts must be run **inside the API container**
- Running scripts on host without dependencies will fail
- This mirrors real-world containerized systems

---

## What you should reflect on after this lab

Ask yourself:

1. Why keyword search failed here
2. Why vector search worked
3. How this would help during real incidents
4. Why this is required for RAG systems

Understanding these answers is the real outcome of this lab.

---

## Troubleshooting

### Container not starting

```bash
# Check logs
docker compose logs api
docker compose logs qdrant

# Rebuild from scratch
docker compose down -v
docker system prune -f
docker compose up --build
```

### Port already in use

```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill the process or change port in docker-compose.yml
```

### Memory issues

```bash
# Check memory usage
free -h

# If running low, consider upgrading to t3.large (8GB RAM)
```

### Ingest script fails

```bash
# Verify you're inside the container
docker exec -it lab-031-vector-similarity-search-api-1 bash

# Check Python dependencies
pip list | grep sentence-transformers

# Reinstall if needed
pip install -r requirements.txt
```

---

## Next steps

After completing this lab successfully:

1. Review **Chapter 3 - Part 1** in the eBook for deeper theory
2. Experiment with your own queries
3. Observe how scores change with different phrasings
4. Move to **Lab 03.2** to build RAG on top of this foundation

---

## Support

If you encounter issues:

- Check the [GitHub Issues](https://github.com/toktechteam/ai_agents_for_devops/issues)
- Review the eBook chapter for additional context
- Ensure all prerequisites are met

---

> ⚠️ Remember  
> This lab is about **understanding**, not just execution.  
> Take time to observe what happens and why.
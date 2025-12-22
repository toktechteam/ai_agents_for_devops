# Lab 03.1 — Vector Similarity Search (Embeddings + Vector Database)

[![Lab](https://img.shields.io/badge/Lab-03.1-blue.svg)](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-03.1-vector-similarity-search)
[![Chapter](https://img.shields.io/badge/Chapter-3%20Part%201-orange.svg)](https://theopskart.gumroad.com/l/AIAgentsforDevOps)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This lab is part of **Chapter 3 (Part 1)** of the eBook **AI Agents for DevOps**.

---

## 🎯 Why This Lab Exists

DevOps engineers don't search perfectly during incidents.

They type things like:
- "pods restarting again"
- "service behaving weird"
- "db slow maybe pool issue"

Traditional systems rely on **exact keyword matching**, which fails badly under real operational pressure.

This lab exists to demonstrate **why vector similarity search was invented** and how it enables systems to search by **meaning and intent**, not by exact words.

---

## 🛠️ What You Will Build

In this lab, you will build a **real semantic search system** that:

1. Converts operational text into **embeddings** (numerical representations of meaning)
2. Stores embeddings in a **vector database (Qdrant)**
3. Performs **similarity search** using distance metrics
4. Ranks results by **semantic relevance**, not keyword matches

This retrieval layer is the foundation for:
- **RAG** (Retrieval Augmented Generation)
- **AI incident assistants**
- **Internal DevOps knowledge systems**

---

## 🏗️ Architecture (Conceptual)

```
User Query (text)
       ↓
Embedding Model
       ↓
Vector Database (Qdrant)
       ↓
Top-K similar documents (ranked by score)
```

---

## 📊 Before vs After Vector Search

### Before Vector Search (Traditional Search)
- Exact keyword matching
- "pods restarting" ≠ "CrashLoopBackOff"
- Misses relevant runbooks
- Unreliable during incidents

### After Vector Search
- Searches by **intent and meaning**
- Handles messy human queries
- Results ranked by similarity score
- Reliable for real DevOps workflows

---

## 👀 What You Should Observe During This Lab

When you run a query like:

```
pods restarting again
```

You should observe:

- ✅ The correct Kubernetes runbook appears **first**
- ✅ Even though you did not type "Kubernetes" or "CrashLoopBackOff"
- ✅ Related but less relevant issues appear with **lower scores**

> This proves the system understands **semantic meaning**, not literal text.

---

## ✅ How to Verify You Understood This Lab (IMPORTANT)

This lab is **not complete** just because containers are running.

You have completed the lab successfully if you can verify the following.

### Step 1: Ingest Runbooks (Run Once)

Run inside the API container:

```bash
docker exec -it lab-031-vector-similarity-search-api-1 bash
python scripts/ingest.py
```

**Expected output:**
```
{'collection': 'runbooks', 'inserted': 5}
```

This confirms:
- ✅ Text has been converted into embeddings
- ✅ Embeddings are stored in the vector database
- ✅ Retrieval is now possible

---

### Step 2: Run Semantic Queries

Still inside the container, run:

```bash
python scripts/query.py "pods restarting again"
```

**Real example output:**

```
Query: pods restarting again

1. score=0.6645 | Kubernetes Pods CrashLoopBackOff Troubleshooting | service=platform | severity=high
   If pods are CrashLoopBackOff: check logs, describe pod, verify env vars/secrets, 
   check image pull, check liveness/readiness probes, and confirm resource limits.

2. score=0.3884 | Node Disk Pressure in Kubernetes | service=platform | severity=high
3. score=0.1414 | Database Connection Pool Exhaustion | service=db | severity=high
4. score=0.1108 | TLS Certificate Expiry Monitoring | service=security | severity=low
5. score=0.0848 | High Latency in API Service | service=api | severity=medium
```

---

### Step 3: Validate the Learning Outcome

Ask yourself:

| Question | Answer |
|----------|--------|
| ❓ Did the correct runbook appear even without exact keywords? | ✅ Yes |
| ❓ Are results ranked by semantic relevance? | ✅ Yes |
| ❓ Does the score decrease as relevance drops? | ✅ Yes |
| ❓ Would SQL `LIKE` queries achieve this? | ❌ No |

If you can answer these confidently, you have understood:
- Embeddings
- Vector similarity
- Why vector databases exist
- Why this layer is mandatory before RAG or AI agents

---

## 🎓 Key Learning Outcomes

After completing this lab, you should clearly understand:

1. **Vector search understands intent, not exact words**
2. **Similarity scores represent distance in meaning, not confidence**
3. **Embeddings are stored once and queried many times**
4. **Vector databases are stateful infrastructure components**
5. **Retrieval quality directly determines AI system quality**
6. **This lab is the foundation of RAG systems**

---

## 📁 Files You Should Care About

| File/Directory | Purpose |
|----------------|---------|
| `docker-compose.yml` | Orchestrates API and Qdrant services |
| `Dockerfile` | Container for the inference API |
| `app/main.py` | FastAPI service with embedding endpoints |
| `scripts/ingest.py` | Converts runbooks to embeddings and stores them |
| `scripts/query.py` | Performs semantic search queries |
| `data/runbooks.json` | Sample operational runbooks |
| `requirements.txt` | Python dependencies |
| `commands.md` | Quick reference for all commands |
| `README.md` | This file (single source of truth) |

---

## 🚀 Getting Started

All setup steps, prerequisites, and execution commands are documented here:

👉 **[commands.md](commands.md)**

Quick start:

```bash
# Start services
docker compose up --build

# Ingest data (in another terminal)
docker exec -it lab-031-vector-similarity-search-api-1 bash
python scripts/ingest.py

# Run queries
python scripts/query.py "pods restarting again"
```

---

## 🔧 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker compose logs api
docker compose logs qdrant

# Rebuild from scratch
docker compose down -v
docker compose up --build
```

### Ingest Script Fails

```bash
# Verify you're inside the container
docker exec -it lab-031-vector-similarity-search-api-1 bash

# Check if Qdrant is accessible
curl http://qdrant:6333/collections

# Reinstall dependencies if needed
pip install -r requirements.txt
```

### Query Returns No Results

```bash
# Verify data was ingested
docker exec -it lab-031-vector-similarity-search-api-1 bash
python scripts/ingest.py  # Run again

# Check Qdrant collection
curl http://localhost:6333/collections/runbooks
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8000

# Change port in docker-compose.yml if needed
# Or stop conflicting service
```

---

## ⚠️ Important

> Do not just run commands.  
> **Observe the output, ranking, and scores.**  
> Understanding **why** the system behaves this way is the real goal of this lab.

---

## 💡 Understanding Similarity Scores

Similarity scores are **distance metrics**, not confidence percentages:

- **Higher score** (e.g., 0.6645) = closer semantic meaning
- **Lower score** (e.g., 0.0848) = weaker semantic relation

In production systems:
- Set score thresholds to filter noise
- Tune based on your use case
- Monitor score distributions over time

---

## ⭐ Final Note

This lab intentionally stops at **retrieval**.

There is:
- ❌ No LLM generation
- ❌ No agents
- ❌ No RAG pipeline

> Those come **after** you fully understand vector similarity search.

---

## 🧹 Cleanup

```bash
docker compose down -v
docker system prune -f
```

---

## ➡️ What Comes Next

After mastering this lab:

- **Lab 3.2**: Building RAG (Retrieval Augmented Generation) on top of vector search
- **Lab 3.3**: Production-grade vector database optimization
- **Chapter 4**: AI agents that use retrieval for decision-making

---

## 📦 Repository Location

This lab lives here:

👉 [github.com/toktechteam/ai_agents_for_devops/tree/main/lab-03.1-vector-similarity-search](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-03.1-vector-similarity-search)

---

## 📚 eBook Reference

This lab is explained in detail in **Chapter 3 – Part 1** of the eBook:

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
- **Commercial Licensing**: theopskart@gmail.com/toketechteam@gmail.com

---

## ⭐ Acknowledgments

This lab is part of the comprehensive **AI Agents for DevOps** course, designed to teach practical AI implementation in production environments.

If you find this lab helpful, consider:
- ⭐ Starring this repository
- 📖 Getting the full eBook for deeper insights
- 🔄 Sharing with your team

---

## 🎯 Success Criteria

You have successfully completed this lab if:

- ✅ Data ingestion completes without errors
- ✅ Semantic queries return relevant results
- ✅ Different wording still finds the correct runbook
- ✅ Scores decrease as relevance decreases
- ✅ You understand **why** vector search works

---

Copyright © 2024 TokTechTeam. See [LICENSE](../LICENSE) for details.
# Lab 01.2 — API-Based vs Self-Hosted Model Inference (Operational Comparison)

[![Lab](https://img.shields.io/badge/Lab-01.2-blue.svg)](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-01.2-api-vs-selfhosted)
[![Chapter](https://img.shields.io/badge/Chapter-1-orange.svg)](https://theopskart.gumroad.com/l/AIAgentsforDevOps)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This lab is part of **Chapter 1** of the eBook **AI Agents for DevOps**.

---

## 🎯 Purpose of This Lab

This lab demonstrates a core Chapter-1 reality:

> **Two AI services can expose the same API and still behave very differently in production.**

You will compare:
- An **API-based LLM service** (external dependency)
- A **self-hosted ML model** (local inference)

The goal is **not output quality**.  
The goal is to observe **startup behavior, latency, memory usage, and failure modes**.

---

## 🔬 What This Lab Is (and Is Not)

### ✅ This lab IS about:
- API vs self-hosted inference
- Cold start behavior
- Memory characteristics
- External dependency risk
- Operational trade-offs

### ❌ This lab is NOT about:
- ML training
- Model accuracy tuning
- Kubernetes
- UI / frontend
- Production hardening

---

## 📋 Prerequisites

- **OS**: Ubuntu 22.04
- **Docker + Docker Compose**: Installed and working
- **Internet access**: Required for API-based service
- **OpenAI API key**: Free tier is enough ([Get one here](https://platform.openai.com/api-keys))
- **RAM**: Minimum **8 GB** (for self-hosted model)

> ⚠️ Important: This lab requires more RAM than Lab 1.1 due to the self-hosted model.

---

## 🏗️ Lab Architecture (Conceptual)

```
                    NGINX (localhost:8080)
                           |
           +---------------+---------------+
           |                               |
    API Service                    Self-Hosted Service
    (External LLM)                 (Local Model)
           |                               |
    - Fast startup                 - Slow startup
    - Network-dependent            - High memory usage
    - Low memory                   - No network dependency
```

**Components:**

- **NGINX**: Single entry point for all requests (`localhost:8080`)
- **API Service**: Calls external LLM API (OpenAI)
- **Self-Hosted Service**: Loads local model (`facebook/bart-large-cnn`)

> Note: NGINX is used **only for API routing**, not for serving web pages.

---

## 📁 Files You Should Care About

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Orchestrates all services |
| `app_api.py` | API-based service implementation |
| `app_selfhosted.py` | Self-hosted model service |
| `requirements-api.txt` | Dependencies for API service (minimal) |
| `requirements-selfhosted.txt` | Dependencies for self-hosted service (heavy) |
| `nginx.conf` | Routing configuration |
| `.env` | OpenAI API key configuration |
| `README.md` | This file (single source of truth) |

---

## 🚀 Setup Instructions

### Step 1: Create Environment File

Create `.env` in the lab root directory:

```env
OPENAI_API_KEY=replace_with_your_key
```

> Get your API key from: https://platform.openai.com/api-keys

---

### Step 2: Start Services

```bash
docker compose up --build
```

> ⚠️ Do not run in detached mode initially — **observe the logs**.

**What to watch for:**
- API service starts **immediately**
- Self-hosted service takes **much longer** (model loading)
- Memory allocation differences

---

## 🧪 How to Test the Lab

All requests go through **NGINX (port 8080)**.

### 1️⃣ Health Checks

**API-based service:**
```bash
curl http://localhost:8080/api/health
```

**Self-hosted service:**
```bash
curl http://localhost:8080/selfhosted/health
```

Both should return `{"status":"ok"}` once ready.

---

### 2️⃣ Self-Hosted Inference (Local Model)

```bash
curl -X POST http://localhost:8080/selfhosted/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"DevOps engineers manage production systems at scale."}'
```

**Real output from this lab run:**
```json
{
  "summary": "",
  "model_info": "facebook/bart-large-cnn",
  "processing_time_ms": 653.64,
  "method": "local-bart",
  "metadata": {
    "service_type": "self-hosted",
    "network_dependent": false,
    "scaling": "manual",
    "min_length": 50,
    "max_length": 3
  }
}
```

**Important observations:**
- ✅ Model executed **locally**
- ✅ **No network dependency**
- ✅ **Fixed memory usage**
- ⚠️ Empty summary caused by config mismatch (`min_length > max_length`)

> This highlights how self-hosted systems are sensitive to **configuration**, not availability.

---

### 3️⃣ API-Based Inference (External LLM)

```bash
curl -X POST http://localhost:8080/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"DevOps engineers manage production systems at scale."}'
```

**Real output from this lab run:**
```json
{
  "error": "Rate limit exceeded - try again later",
  "retry_suggested": true,
  "processing_time_ms": 615.45,
  "service_type": "api"
}
```

**Important observations:**
- ✅ Service started **instantly**
- ⚠️ Request **failed** due to external rate limiting
- ⚠️ Failure is **outside your infrastructure control**

> This is **expected behavior**, not a bug.

---

## 📊 What You Should Observe

| Aspect | API-Based Service | Self-Hosted Service |
|--------|-------------------|---------------------|
| **Startup time** | Fast | Slow (model loading) |
| **Memory usage** | Low | High & fixed |
| **Latency** | Network + compute | Compute only |
| **Failure modes** | Rate limits, network | Config, memory |
| **Scaling** | Provider-managed | Manual |
| **Cost model** | Per request | Fixed infra |

---

## 💡 Key Chapter-1 Takeaways

1. **Same API ≠ same operational behavior**
2. **API services introduce external failure modes**
3. **Self-hosted models introduce startup and memory cost**
4. **Cold starts matter**
5. **Inference is an infrastructure problem**

---

## ✅ When This Lab Is Complete

You should be able to clearly explain:

- ✅ Why the API call failed but infrastructure was healthy
- ✅ Why the self-hosted service worked without the internet
- ✅ Why startup time and memory differ
- ✅ When each approach makes sense operationally

> If you can do that, the lab succeeded — **regardless of output quality**.

---

## 🧹 Cleanup

```bash
docker compose down
docker system prune -f
```

---

## ➡️ What Comes Next

You've now completed the foundational understanding of ML inference operational challenges:

- **Lab 1.1**: Observed why ML services behave differently
- **Lab 1.2**: Compared API vs self-hosted trade-offs

**Next:** Move to Chapter 2 labs to explore orchestration and scaling patterns.

---

## 📦 Repository Location

This lab lives here:

👉 [github.com/toktechteam/ai_agents_for_devops/tree/main/lab-01.2-api-vs-selfhosted](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-01.2-api-vs-selfhosted)

---

## 📚 eBook Reference

This lab is explained in detail in **Chapter 1** of the eBook:

👉 **AI Agents for DevOps**  
[theopskart.gumroad.com/l/AIAgentsforDevOps](https://theopskart.gumroad.com/l/AIAgentsforDevOps)

---

## 🔧 Troubleshooting

### API Service Returns Rate Limit Error
**This is expected behavior** demonstrating external dependency risks. The lab's goal is to observe this failure mode.

### Self-Hosted Service Won't Start
```bash
# Check available memory
free -h

# Ensure you have at least 8GB RAM
# Consider upgrading to t3.large if needed
```

### NGINX Returns 502 Bad Gateway
```bash
# Check if services are ready
docker compose logs api
docker compose logs selfhosted

# Self-hosted service takes time to load the model
# Wait until you see "Application startup complete" in logs
```

### OpenAI API Key Issues
```bash
# Verify .env file exists and has correct format
cat .env

# Restart services after updating .env
docker compose down
docker compose up --build
```

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
- **Commercial Licensing**: theopskart@gmail.com/toktechteam@gmail.com

---

## ⭐ Acknowledgments

This lab is part of the comprehensive **AI Agents for DevOps** course, designed to teach practical AI implementation in production environments.

If you find this lab helpful, consider:
- ⭐ Starring this repository
- 📖 Getting the full eBook for deeper insights
- 🔄 Sharing with your team

---

Copyright © 2024 TokTechTeam. See [LICENSE](../LICENSE) for details.
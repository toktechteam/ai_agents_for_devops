# Lab 01.1 — Understanding Why AI/ML Inference Breaks Traditional DevOps Assumptions

[![Lab](https://img.shields.io/badge/Lab-01.1-blue.svg)](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-01.1-ml-inference-vs-traditional)
[![Chapter](https://img.shields.io/badge/Chapter-1-orange.svg)](https://theopskart.gumroad.com/l/AIAgentsforDevOps)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This lab is part of **Chapter 1** of the eBook **AI Agents for DevOps**.

---

## 🎯 Purpose of This Lab

This lab exists to **prove, not explain**, one core idea from Chapter 1:

> **AI/ML inference services behave fundamentally differently from traditional applications.**

As a DevOps engineer, you already know how to deploy APIs.  
This lab shows **why deploying an ML model as an API feels wrong, slow, and heavy** — and why that's expected.

---

## 🎓 What You Will Learn (Explicit Outcomes)

After completing this lab, you will be able to:

1. **Observe the startup time difference** between:
   - A traditional REST API
   - An ML model-backed API

2. **Understand why ML services take longer to start**

3. **See why model loading dominates startup time**

4. **Recognize why memory becomes a fixed cost**

5. **Connect these observations directly to Chapter 1 concepts**

> ⚠️ Important  
> This lab is **not** about accuracy, ML theory, or optimization.  
> It is about **operational behavior**.

---

## 🔬 Lab Scope (Important)

This lab focuses only on:

- ✅ **Inference**, not training
- ✅ **Local containers**, not Kubernetes
- ✅ **Observation**, not tuning

If you are looking for Kubernetes, scaling, or observability:  
👉 **That comes later. Do not skip ahead.**

---

## 📋 Prerequisites

- **OS**: Ubuntu 22.04
- **Docker**: Installed and working
- **Docker Compose**: Plugin available
- **RAM**: 4 GB minimum (t3.medium is sufficient)

> Note: No Python installation on host is required.

---

## 🏗️ Lab Structure

You will run **two services**:

### 1. Traditional API
- Starts quickly
- No heavy initialization
- Typical REST API behavior

### 2. ML Inference API
- Loads a model at startup
- Takes noticeably longer to become ready
- Demonstrates ML-specific operational challenges

Both expose the same interface so behavior can be compared fairly.

---

## 📁 Files You Should Care About

| File | Purpose |
|------|---------|
| `Dockerfile.traditional` | Traditional REST API container |
| `Dockerfile.ml` | ML inference service container |
| `app_traditional.py` | Lightweight API implementation |
| `app_ml.py` | Model-loading API implementation |
| `requirements-traditional.txt` | Dependencies for traditional API (minimal) |
| `requirements-ml.txt` | Dependencies for ML service (includes model libraries) |
| `docker_compose.txt` | Runs both services |
| `nginx.conf` | Simple routing configuration |
| `README.md` | This file (single source of truth) |

> Ignore any other files unless instructed.

---

## 🚀 Step-by-Step Instructions

### Step 1: Start the Services

From the lab directory:

```bash
docker compose -f docker_compose.txt up --build
```

> ⚠️ Do not run in detached mode yet.  
> You need to **watch the logs**.

---

### Step 2: Observe Startup Behavior (Do Not Skip)

While containers start, observe carefully:

#### Traditional Service
- ✅ Starts almost immediately
- ✅ Logs appear quickly
- ✅ Ready to accept traffic fast

#### ML Service
- ⏳ Noticeable delay before readiness
- 📊 Logs show:
  - Model initialization
  - Loading steps
- ⚠️ Startup time is significantly longer

> 👉 **This delay is the point of the lab.**

---

### Step 3: Test Both APIs

In a new terminal:

**Traditional API:**
```bash
curl http://localhost/traditional/health
```

**ML API:**
```bash
curl http://localhost/ml/health
```

Both should return healthy responses once fully started.

---

### Step 4: Restart and Compare Again

Stop the services:
```bash
docker compose -f docker_compose.txt down
```

Start them again:
```bash
docker compose -f docker_compose.txt up --build
```

**Repeat your observations.**

Ask yourself:
- Which service is consistently slower to start?
- Which one allocates memory immediately?
- Which one feels "heavier" to operate?

---

## 💡 Understanding What You Just Saw (Critical Section)

### Why the ML Service Is Slow

1. The ML service **loads the entire model into memory** at startup
2. **Models are binary artifacts**, not source code
3. You **cannot "partially load"** a model
4. This cost is **paid before** the service can accept traffic

> This directly maps to Chapter 1: **Models Are Not Code**.

---

### Why This Breaks DevOps Assumptions

**Traditional assumptions:**
- ✅ Fast startup
- ✅ Cheap restarts
- ✅ Horizontal scaling is easy

**ML inference reality:**
- ⚠️ Startup is expensive
- ⚠️ Restarts are painful
- ⚠️ Memory must be allocated upfront

**This is why:**
- Readiness probes need rethinking
- Auto-scaling behaves differently
- Rolling updates become risky

---

## 🎯 Key Takeaways (Tie Back to Chapter 1)

1. **AI inference services are stateful by nature**
2. **Model loading time is unavoidable**
3. **Memory is a fixed requirement, not elastic**
4. **Inference (not training) is the DevOps problem**
5. **Traditional microservice patterns do not apply cleanly**

> If this felt uncomfortable — **that's expected.**

---

## 🧹 Cleanup

```bash
docker compose -f docker_compose.txt down
docker system prune -f
```

---

## ➡️ What Comes Next

**Lab 1.2** builds on this by comparing:
- API-based model serving
- Self-hosted model serving

You will move from **observation** to **decision-making**.

> 👉 Do not skip Lab 1.2.

---

## ✅ Lab Completion Criteria

This lab is complete when:

- ✅ You clearly understand **why the ML service behaves differently**
- ✅ You can **explain the difference** without mentioning ML theory
- ✅ You can **map your observations directly to Chapter 1**

---

## 📦 Repository Location

This lab lives here:

👉 [github.com/toktechteam/ai_agents_for_devops/tree/main/lab-01.1-ml-inference-vs-traditional](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-01.1-ml-inference-vs-traditional)

---

## 📚 eBook Reference

This lab is explained in detail in **Chapter 1** of the eBook:

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
- **Commercial Licensing**: [your-contact-email]

---

## ⭐ Acknowledgments

This lab is part of the comprehensive **AI Agents for DevOps** course, designed to teach practical AI implementation in production environments.

If you find this lab helpful, consider:
- ⭐ Starring this repository
- 📖 Getting the full eBook for deeper insights
- 🔄 Sharing with your team

---

Copyright © 2024 TokTechTeam. See [LICENSE](../LICENSE) for details.

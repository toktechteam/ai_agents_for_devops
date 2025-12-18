# Lab 03.1 — Vector Similarity Search (Embeddings + Vector Database)

[![Lab](https://img.shields.io/badge/Lab-03.1-blue.svg)](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-03.1-vector-similarity-search)
[![Chapter](https://img.shields.io/badge/Chapter-3%20Part%201-orange.svg)](https://theopskart.gumroad.com/l/AIAgentsforDevOps)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This lab is part of **Chapter 3 (Part 1)** of the eBook **AI Agents for DevOps**.

---

## 🎯 Why this lab exists

DevOps engineers don't search perfectly during incidents.

They type things like:
- "pods restarting again"
- "db slow maybe pool issue"
- "service behaving weird"

Traditional systems rely on **exact keyword matching**, which fails badly in real-world operations.

This lab exists to show **why vector search was invented** and how it solves this problem by searching **by meaning**, not by exact words.

---

## 🛠️ What you will build

In this lab, you will build a **real semantic search system** that:

1. Converts text into **embeddings** (numerical representations of meaning)
2. Stores those embeddings in a **vector database (Qdrant)**
3. Retrieves results using **similarity search**
4. Ranks results by **semantic distance**, not keyword match

This is the **retrieval layer** used in:
- RAG (Retrieval Augmented Generation)
- AI incident assistants
- Internal DevOps knowledge systems

---

## 🏗️ Architecture (conceptual)

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
- "CrashLoopBackOff" ≠ "pods restarting"
- Misses relevant runbooks
- Unreliable during incidents

### After Vector Search
- Searches by **intent and meaning**
- Handles messy human queries
- Results ranked by similarity score
- Reliable for real DevOps workflows

---

## 👀 What you should observe during this lab

When you run a query like:

```
pods restarting crash loop
```

You should observe:
- The correct runbook appears **first**
- Even though you didn't type "Kubernetes" or "CrashLoopBackOff"
- Related operational issues appear with **lower scores**

This proves the system understands **semantic meaning**, not text matching.

---

## 🎓 Key learning outcomes

After completing this lab, you should clearly understand:

1. **Vector search understands intent, not exact words**
2. **Similarity scores represent meaning distance**, not confidence
3. **This lab is the foundation of RAG systems**
4. Why traditional databases fail for semantic search
5. Why vector databases are unavoidable in AI systems
6. The infrastructure impact of embeddings (RAM, cold start, storage)

---

## 📦 Repository location

This lab lives here:

👉 [github.com/toktechteam/ai_agents_for_devops/tree/main/lab-03.1-vector-similarity-search](https://github.com/toktechteam/ai_agents_for_devops/tree/main/lab-03.1-vector-similarity-search)

---

## 📚 eBook reference

This lab is explained in detail in **Chapter 3 – Part 1** of the eBook:

👉 **AI Agents for DevOps**  
[theopskart.gumroad.com/l/AIAgentsforDevOps](https://theopskart.gumroad.com/l/AIAgentsforDevOps)

---

## ⚠️ Important

> Do not just run commands.  
> Observe the output, the scores, and **why the system behaves this way**.  
> That understanding is the real goal of this lab.

---

## 🚀 Getting Started

See the [setup.md](setup.md) file for detailed installation and execution instructions.

Quick start:
```bash
git clone https://github.com/toktechteam/ai_agents_for_devops.git
cd ai_agents_for_devops/lab-03.1-vector-similarity-search
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

For full license details and commercial use inquiries, see [LICENSE](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! However, please note:
- This content is tied to a commercial eBook
- Contributions should align with the educational goals
- All contributions will be licensed under the same terms

Before contributing:
1. Read the [LICENSE](LICENSE) file
2. Open an issue to discuss your proposed changes
3. Submit a pull request

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/toktechteam/ai_agents_for_devops/issues)
- **eBook**: [AI Agents for DevOps](https://theopskart.gumroad.com/l/AIAgentsforDevOps)
- **Commercial Licensing**: [toktechteam@gmail.com,theopskart@gmail.com]

---

## ⭐ Acknowledgments

This lab is part of the comprehensive **AI Agents for DevOps** course, designed to teach practical AI implementation in production environments.

If you find this lab helpful, consider:
- ⭐ Starring this repository
- 📖 Getting the full eBook for deeper insights
- 🔄 Sharing with your team

---

Copyright © 2024 TokTechTeam. See [LICENSE](LICENSE) for details.

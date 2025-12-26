# AI Agents for DevOps

**Architect, Deploy, and Automate Like a Pro**

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Book](https://img.shields.io/badge/eBook-Available-blue.svg)](https://theopskart.gumroad.com/l/AIAgentsforDevOps)

This repository contains **hands-on AI agent labs for DevOps engineers**, covering **LangChain, AutoGen, vector search, and AgentOps patterns on Kubernetes**. These labs are the practical companion to the book **AI Agents for DevOps: Architect, Deploy, and Automate Like a Pro**.

The repository is designed for AI-curious DevOps engineers who want to move beyond traditional automation and understand how AI agents actually run in real systems — from infrastructure, scaling, observability, and cost perspectives.

---

## 📘 Book Link

👉 [AI Agents for DevOps on Gumroad](https://theopskart.gumroad.com/l/AIAgentsforDevOps)

---

## 🎯 What This Repository Is About

This repo contains **practical, runnable labs** that map directly to the concepts explained in the book.

### You won't find:
- ❌ Toy demos
- ❌ Magic black boxes
- ❌ Abstract AI theory

### You will find:
- ✅ Real execution models for AI agents
- ✅ Production-style deployment patterns
- ✅ Clear operational behavior (logs, workflows, scaling)
- ✅ DevOps-first mental models for AI systems

**The goal is simple:**

> Help DevOps engineers understand how AI agents behave as systems, not just code.

---

## 🧠 Who This Is For

This repository is ideal if you are:

- **A DevOps / SRE / Platform Engineer**
- **Curious about AI agents on Kubernetes**, LangChain, AutoGen, RAG
- **Tired of hype** and want hands-on clarity
- **Interested in how AI workloads affect:**
  - Infrastructure
  - Scaling
  - Cost
  - Observability
  - Operational responsibility

> If you already know Docker, Kubernetes, CI/CD, and monitoring — **this repo speaks your language**.

---

## 📊 AI Agents for DevOps — Learning Flow

Understanding the fundamental difference between traditional automation and AI agent systems:

```
Traditional Automation
----------------------
Scripts → Pipelines → Jobs → Logs


AI Agent Systems
----------------
          ┌───────────────┐
          │   Alert / Task│
          └───────┬───────┘
                  ↓
          ┌────────────────┐
          │   Agent Planner │  ← decides what to do
          └───────┬────────┘
                  ↓
        ┌─────────┴─────────┐
        │   Tool Execution  │  ← kubectl, APIs, metrics
        └─────────┬─────────┘
                  ↓
          ┌────────────────┐
          │   Agent Reason │  ← analysis & decision
          └───────┬────────┘
                  ↓
          ┌────────────────┐
          │  Result / Logs │
          └────────────────┘

Scaling Model:
- LangChain → long-running services
- AutoGen   → parallel agent executions
```

---

## 🗺️ Learning Roadmap (Labs Overview)

Each lab builds progressively. You are expected to **run, observe, and reason**, not just execute commands.

### Chapter 1 – Foundations

| Lab | Focus |
|-----|-------|
| [lab-01.1-ml-inference-vs-traditional](lab-01.1-ml-inference-vs-traditional/) | Why ML inference ≠ normal API |
| [lab-01.2-api-vs-selfhosted](lab-01.2-api-vs-selfhosted/) | API-based vs self-hosted trade-offs |
| [lab-01.3-ai-ml-fundamentals](lab-01.3-ai-ml-fundamentals/) | Kubernetes does not save you |

**Chapter Focus:**  
How AI inference workloads differ from traditional applications.

---

### Chapter 2 – Infrastructure & Observability

| Lab | Focus |
|-----|-------|
| [lab-02.1-inference-resources](lab-02.1-inference-resources/) | Resource reality: CPU, memory, fixed costs |
| [lab-02.2-observability](lab-02.2-observability/) | Observability for AI inference services |

**Chapter Focus:**  
CPU, memory, latency, metrics, and why AI workloads break old assumptions.

---

### Chapter 3 – Vector Search & Semantic Memory

| Lab | Focus |
|-----|-------|
| [lab-03.1-vector-similarity-search](lab-03.1-vector-similarity-search/) | Semantic search by meaning, not keywords |
| [lab-03.2-batch-vs-online](lab-03.2-batch-vs-online/) | Batch vs online inference patterns |

**Chapter Focus:**  
Why text ≠ meaning, how embeddings work, and how agents retrieve knowledge.

---

### Chapter 4 – First AI Agent

| Lab | Focus |
|-----|-------|
| [lab-04.1-first-ai-agent](lab-04.1-first-ai-agent/) | Building your first infrastructure AI agent |

**Chapter Focus:**  
What an agent actually is: tools, memory, execution loop, and decisions.

---

### Chapter 5 – Agent Frameworks in Production

| Lab | Focus |
|-----|-------|
| [lab-05.1-langchain-production](lab-05.1-langchain-production/) | LangChain agents as services |
| [lab-05.2-autogen-workflow](lab-05.2-autogen-workflow/) | AutoGen agents as workflows |

**Chapter Focus:**  
How different agent frameworks behave operationally:
- **Agents as services** (LangChain-style)
- **Agents as jobs/workflows** (AutoGen-style)
- Scaling, logs, lifecycle, and cost

---

## ⚙️ How to Use This Repo

1. **Read the relevant chapter** in the book
2. **Go to the matching lab folder**
3. **Follow the README.md** inside that lab
4. **Run the lab** locally or on Kubernetes
5. **Observe:**
   - Logs
   - Pod behavior
   - Execution lifecycle
6. **Ask why it behaves that way** — that's the learning

> These labs are intentionally designed to **show behavior, not hide it**.

---

## 🚀 What You'll Be Able to Do After This

By completing these labs, you will be able to:

✅ **Explain how AI agents differ from microservices**  
✅ **Decide when to use:**
   - Managed AI APIs
   - Agent frameworks
   - Multi-agent systems

✅ **Understand:**
   - Agent scaling models
   - Stateless vs stateful agents
   - Cost drivers (tokens, executions)

✅ **Debug agents** using logs and workflows, not guesswork  
✅ **Talk confidently** about AgentOps in interviews and design reviews

---

## 📦 Beyond This Repository

This repo covers the **first stage of the learning journey** (lab-01 → lab-05.2).

Once you complete these, you can move to more advanced labs here:

👉 [Advanced AI Agents for DevOps Labs](https://github.com/toktechteam/ai_agents_for_devops_labs/tree/main)

Those labs go deeper into:
- Real tools
- Advanced workflows
- Production-grade patterns

---

## 🛠️ Prerequisites

### Required Tools
- **Docker** (24+)
- **Kubernetes** (kubectl + kind)
- **Python** (3.11+)
- **curl** (for API testing)

### Required Knowledge
- Basic Docker and Kubernetes
- CI/CD concepts
- REST APIs
- Monitoring basics

---

## 📁 Repository Structure

```
ai-agents-for-devops/
├── LICENSE                          ← Dual license (CC BY-NC 4.0 + MIT)
├── README.md                        ← This file
│
├── lab-01.1-ml-inference-vs-traditional/
├── lab-01.2-api-vs-selfhosted/
├── lab-01.3-ai-ml-fundamentals/
├── lab-02.1-inference-resources/
├── lab-02.2-observability/
├── lab-03.1-vector-similarity-search/
├── lab-03.2-batch-vs-online/
├── lab-04.1-first-ai-agent/
├── lab-05.1-langchain-production/
└── lab-05.2-autogen-workflow/
```

Each lab contains:
- `README.md` - Lab-specific instructions
- `setup.md` - Detailed setup guide
- `k8s/` - Kubernetes manifests
- `app/` - Application code
- `Dockerfile` - Container definition

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

For full license details, see [LICENSE](LICENSE).

---

## ⭐ Support the Project

If this repository helps you:

- ⭐ **Star the repo**
- 🍴 **Fork it** and experiment
- 🧠 **Share it** with other DevOps engineers exploring AI
- 📖 **Get the eBook** for deeper insights

This helps the project grow and reach the right audience.

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
- **Email**: toktechteam@gmail.com / theopskart@gmail.com
- **Commercial Licensing**: Contact us via email

---

## 👤 About the Author

**Roshan Kumar Singh**  
*Manager (Technology) | AI + DevOps Evangelist | Founder – TheOpsKart*

🔗 [LinkedIn](https://www.linkedin.com/in/roshan-singh-82985629/)

Hi, I'm Roshan Kumar Singh — Manager (Technology), AI + DevOps Evangelist, and founder of **TheOpsKart**.

For over **14 years**, I've worked across banking, e-commerce, and travel industries, helping teams build reliable infrastructure and streamline DevOps workflows.

I've **mentored and trained 100+ engineers**, guiding them into Cloud and DevOps roles. My passion lies at the intersection of **DevOps and Artificial Intelligence** — a space where I believe DevOps engineers will play a critical role in the coming years.

I wrote this book and built these labs to help engineers move beyond traditional automation and confidently work with **AI agents as real systems**.

---

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AgentOps Best Practices](https://www.agentops.ai/)

---

## 🎓 Learning Path Recommendation

For maximum learning effectiveness, follow this sequence:

1. **Start with Chapter 1 labs** - Understand the foundation
2. **Move through sequentially** - Each builds on the previous
3. **Don't skip observations** - The "why" matters more than the "how"
4. **Experiment after completion** - Modify and break things
5. **Read the book alongside** - Theory + practice = mastery

---

## 💬 Community

Join the conversation and share your learning:

- Share your lab completions on LinkedIn with `#AIAgentsForDevOps`
- Ask questions in GitHub Issues
- Connect with other learners
- Contribute improvements

---

## 🎉 Acknowledgments

Special thanks to:
- All contributors who improve these labs
- The DevOps and AI communities
- Early readers and testers
- Everyone building the future of AgentOps

---

**Happy Learning! 🚀🤖🔧**

*"The future of DevOps is not replacing automation — it's making automation intelligent."*

---

Copyright © 2024 TokTechTeam. See [LICENSE](LICENSE) for details.

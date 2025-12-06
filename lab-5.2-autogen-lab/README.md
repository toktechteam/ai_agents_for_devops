# Lab 5.2 FREE Version – AutoGen Multi-Agent Incident Response
## Building Collaborative AI Agents for DevOps Automation

---

## 🎯 What You Will Learn

### Core Concepts

By completing this lab, you will master:

1. **Multi-Agent Systems** - Autonomous agents working together:
   - **Agent collaboration**: How multiple AI agents coordinate
   - **Role-based agents**: Specialized agents with distinct responsibilities
   - **Agent communication**: Inter-agent messaging and data sharing
   - **Delegation patterns**: Commander delegates to specialists
   - **Consensus building**: Agents collaborating on solutions

2. **AutoGen Framework** - Microsoft's multi-agent framework:
   - **Agent creation**: Building conversational AI agents
   - **Agent types**: AssistantAgent, UserProxyAgent patterns
   - **Conversation flow**: Managing multi-turn dialogues
   - **Agent memory**: Context retention across interactions
   - **LLM integration**: Connecting agents to language models

3. **Incident Response Automation** - Real-world DevOps workflows:
   - **Alert triage**: Automated incident classification
   - **Investigation delegation**: Routing to appropriate specialists
   - **Root cause analysis**: AI-powered problem diagnosis
   - **Remediation planning**: Automated fix suggestions
   - **Human-in-the-loop**: When to escalate to humans

4. **Agent Communication Patterns** - How agents interact:
   - **Request-response**: Simple query patterns
   - **Delegation**: Passing tasks to specialists
   - **Reporting**: Agents sharing findings
   - **Consensus**: Multiple agents agreeing on actions

### Practical Skills

You will be able to:

- ✅ Build multi-agent systems with AutoGen
- ✅ Design agent roles and responsibilities
- ✅ Implement agent-to-agent communication
- ✅ Create incident response workflows
- ✅ Integrate LLMs with agent frameworks
- ✅ Test agent interactions locally
- ✅ Debug agent conversations
- ✅ Design delegation patterns

### Real-World Applications

**SRE Teams** will learn:
- Automating incident triage with AI agents
- Building intelligent on-call assistants
- Reducing MTTR through agent collaboration
- Scaling incident response capabilities

**DevOps Engineers** will learn:
- Multi-agent automation patterns
- AI-powered alert routing
- Intelligent investigation workflows
- Building self-service diagnostic tools

**Platform Engineers** will learn:
- Agent-based automation architecture
- Role-based agent design
- Integration patterns for AI agents
- Building extensible agent systems

**AI/ML Engineers** will learn:
- Practical multi-agent implementations
- AutoGen framework usage
- Agent orchestration patterns
- Production agent design

---

## 📋 Prerequisites

### Required Software
- **Python:** Version 3.11 or higher
- **pip:** Python package manager
- **Git:** For cloning repositories

### Required API Keys
- **OpenAI API Key:** For LLM-powered agents
  ```bash
  export OPENAI_API_KEY="sk-your-key-here"
  ```

### Required Knowledge
- Basic Python programming
- Understanding of incident response concepts
- Familiarity with DevOps practices
- Basic knowledge of AI/LLM concepts

### Verification Commands

```bash
# Check Python version
python3 --version

# Check pip
pip --version

# Verify API key (optional, can be set later)
echo $OPENAI_API_KEY
```

---

## 🏗️ Architecture Overview

### What You're Building

```
┌─────────────────────────────────────────────────────────┐
│              Multi-Agent Incident Response               │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Alert Input                                   │    │
│  │  {                                             │    │
│  │    "alert": "High CPU on pod payment-svc",    │    │
│  │    "severity": "warning",                      │    │
│  │    "timestamp": "2024-01-15T10:30:00Z"        │    │
│  │  }                                             │    │
│  └────────────────┬───────────────────────────────┘    │
│                   │                                     │
│                   ▼                                     │
│  ┌────────────────────────────────────────────────┐    │
│  │  Agent 1: Incident Commander                   │    │
│  │  Role: Triage and Delegation                   │    │
│  │                                                │    │
│  │  Responsibilities:                             │    │
│  │  ├─ Receive incoming alerts                    │    │
│  │  ├─ Analyze alert severity                     │    │
│  │  ├─ Determine appropriate specialist           │    │
│  │  ├─ Delegate to investigator                   │    │
│  │  └─ Coordinate overall response                │    │
│  │                                                │    │
│  │  Persona:                                      │    │
│  │  "You are an experienced incident commander    │    │
│  │   responsible for triaging alerts and          │    │
│  │   delegating to appropriate specialists."      │    │
│  │                                                │    │
│  │  LLM: GPT-4 (for intelligent routing)         │    │
│  └────────────────┬───────────────────────────────┘    │
│                   │                                     │
│                   │ Delegation Message:                 │
│                   │ "Investigate high CPU on            │
│                   │  payment-svc. Identify root         │
│                   │  cause and suggest remediation."    │
│                   │                                     │
│                   ▼                                     │
│  ┌────────────────────────────────────────────────┐    │
│  │  Agent 2: SRE Investigator                     │    │
│  │  Role: Technical Investigation                 │    │
│  │                                                │    │
│  │  Responsibilities:                             │    │
│  │  ├─ Analyze technical details                  │    │
│  │  ├─ Perform root cause analysis                │    │
│  │  ├─ Identify probable causes                   │    │
│  │  ├─ Suggest remediation steps                  │    │
│  │  └─ Report findings to commander               │    │
│  │                                                │    │
│  │  Persona:                                      │    │
│  │  "You are a senior SRE with expertise in      │    │
│  │   Kubernetes, performance analysis, and        │    │
│  │   incident troubleshooting."                   │    │
│  │                                                │    │
│  │  Analysis Tools (Simulated):                   │    │
│  │  ├─ Check pod CPU usage patterns               │    │
│  │  ├─ Review recent deployments                  │    │
│  │  ├─ Analyze error logs                         │    │
│  │  └─ Check HPA configuration                    │    │
│  │                                                │    │
│  │  LLM: GPT-4 (for analysis and reasoning)      │    │
│  └────────────────┬───────────────────────────────┘    │
│                   │                                     │
│                   │ Investigation Report:               │
│                   │ {                                   │
│                   │   "root_cause": "...",              │
│                   │   "evidence": [...],                │
│                   │   "remediation": [...]              │
│                   │ }                                   │
│                   │                                     │
│                   ▼                                     │
│  ┌────────────────────────────────────────────────┐    │
│  │  Final Response                                │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │  Incident Commander Summary              │  │    │
│  │  │  - Alert triaged and investigated        │  │    │
│  │  │  - Root cause identified                 │  │    │
│  │  │  - Remediation plan created              │  │    │
│  │  │  - Ready for human review/approval       │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Agent Interaction Flow

```
Step 1: Alert Reception
    ↓
┌──────────────────────────────────────┐
│  Incident Commander Agent            │
│  Receives: Alert payload             │
│  Actions:                            │
│  - Parse alert details               │
│  - Assess severity                   │
│  - Determine specialist needed       │
└──────────────┬───────────────────────┘
               │
               │ Message to SRE:
               │ "Investigate high CPU on
               │  pod payment-svc. Alert
               │  severity: warning"
               │
               ▼
Step 2: Investigation
    ↓
┌──────────────────────────────────────┐
│  SRE Investigator Agent              │
│  Receives: Investigation request     │
│  Actions:                            │
│  - Analyze alert context             │
│  - Simulate diagnostic checks        │
│  - Identify probable root cause      │
│  - Generate remediation plan         │
└──────────────┬───────────────────────┘
               │
               │ Report back:
               │ {
               │   "root_cause": "CPU
               │    saturation due to
               │    traffic spike",
               │   "remediation": [...]
               │ }
               │
               ▼
Step 3: Response Synthesis
    ↓
┌──────────────────────────────────────┐
│  Incident Commander Agent            │
│  Receives: Investigation report      │
│  Actions:                            │
│  - Review findings                   │
│  - Synthesize final response         │
│  - Present to user                   │
└──────────────────────────────────────┘
               │
               ▼
Complete Investigation Report
```

---

## 📁 Repository Structure

```
lab-05.2-autogen-incident-response-free/
├── README.md                   ← This file
├── setup.md                    ← Detailed setup guide
├── requirements.txt            ← Python dependencies
├── .env.example                ← Environment template
├── src/
│   ├── run.py                  ← Main application entry
│   ├── agents.py               ← Agent definitions
│   ├── commander.py            ← Incident Commander logic
│   ├── investigator.py         ← SRE Investigator logic
│   ├── config.py               ← Configuration
│   └── utils.py                ← Helper functions
├── examples/
│   ├── sample_alerts.json      ← Example alert payloads
│   └── expected_outputs.md     ← Expected responses
├── scripts/
│   ├── test.sh                 ← Test script
│   └── cleanup.sh              ← Cleanup script
└── tests/
    ├── test_agents.py          ← Agent tests
    └── test_integration.py     ← Integration tests
```

---

## 🚀 Quick Start Guide

### Step 1: Clone Repository

```bash
git clone https://github.com/your-org/ai-agents-devops
cd labs/chapter-05/lab-5.2-autogen-incident-response-free
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Collecting pyautogen
Collecting openai
Collecting python-dotenv
...
Successfully installed pyautogen-0.2.x openai-1.x.x ...
```

### Step 3: Configure API Key

```bash
export OPENAI_API_KEY="sk-your-actual-key-here"
```

**Or create .env file:**
```bash
cp .env.example .env
# Edit .env and add your key
```

### Step 4: Run the Application

```bash
python src/run.py
```

**Expected Output:**
```
🚀 AutoGen Multi-Agent Incident Response System
================================================

Initializing agents...
✓ Incident Commander initialized
✓ SRE Investigator initialized

Processing alert: High CPU on pod payment-service-1123

🚨 Incident Commander received alert: High CPU on pod payment-service-1123

Delegating to SRE Investigator...

🧠 SRE Investigator Analysis:
─────────────────────────────────────────────────────
Root Cause Analysis:
The high CPU usage on payment-service-1123 is likely caused by:
1. Traffic spike beyond normal capacity
2. Memory leak causing excessive garbage collection
3. Inefficient code path being triggered
4. Missing or misconfigured HorizontalPodAutoscaler

Evidence:
- Pod CPU usage: 95% of limit (475m/500m)
- No HPA configured for this deployment
- Recent deployment 2 hours ago may have introduced regression

🔧 Recommended Remediation:
─────────────────────────────────────────────────────
Immediate actions:
1. Scale deployment to 5 replicas to distribute load
   kubectl scale deployment payment-service --replicas=5
   
2. Configure HPA for automatic scaling
   kubectl autoscale deployment payment-service --min=3 --max=10 --cpu-percent=70
   
3. Review recent code changes for performance issues
   
4. Monitor memory usage for potential leaks
   kubectl top pod payment-service-1123

Long-term improvements:
- Implement performance profiling
- Set up proper resource requests and limits
- Configure alerts for abnormal CPU patterns
─────────────────────────────────────────────────────

📊 Investigation Complete
Total conversation turns: 3
Time elapsed: 4.2 seconds
Tokens used: ~450
```

---

## 📊 Understanding Agent Behavior

### Incident Commander Agent

**Role:** Triage and delegation

**System Prompt:**
```python
You are an experienced incident commander responsible for:
1. Receiving and triaging incoming alerts
2. Assessing severity and impact
3. Delegating to appropriate specialist agents
4. Coordinating overall incident response
5. Ensuring clear communication

When you receive an alert:
- Acknowledge receipt
- Assess severity (critical/warning/info)
- Determine which specialist should investigate
- Provide clear delegation instructions
- Track progress and synthesize findings
```

**Behavior:**
- Acts as the entry point for all alerts
- Makes routing decisions
- Doesn't perform deep technical analysis
- Focuses on coordination and communication

### SRE Investigator Agent

**Role:** Technical investigation

**System Prompt:**
```python
You are a senior SRE with expertise in:
1. Kubernetes troubleshooting
2. Performance analysis
3. Root cause identification
4. Remediation planning

When investigating an alert:
- Analyze the technical details
- Identify probable root causes
- Suggest immediate and long-term fixes
- Provide specific kubectl commands when applicable
- Consider operational best practices
```

**Behavior:**
- Performs deep technical analysis
- Generates actionable remediation steps
- Provides specific commands and configurations
- Considers both immediate fixes and preventive measures

---

## 🧪 Testing Different Scenarios

### Scenario 1: High CPU Alert

```bash
python src/run.py --alert "High CPU usage on pod web-app-xyz"
```

**Expected:** Commander delegates to SRE, who analyzes CPU patterns and suggests scaling

### Scenario 2: Pod Crash

```bash
python src/run.py --alert "Pod crash loop in production namespace"
```

**Expected:** SRE investigates crash logs and suggests fixes

### Scenario 3: Memory Issues

```bash
python src/run.py --alert "OOMKilled event on database pod"
```

**Expected:** SRE analyzes memory usage and recommends limits adjustment

---

## 🎓 Key Learning Outcomes

### Conceptual Understanding

After completing this lab, you understand:

✅ **Multi-Agent Systems:**
- How multiple AI agents collaborate
- Role-based agent design
- Agent-to-agent communication
- Delegation patterns

✅ **AutoGen Framework:**
- Creating conversational agents
- Managing agent interactions
- LLM integration
- Conversation flow control

✅ **Incident Response Automation:**
- Alert triage automation
- Investigation delegation
- Root cause analysis with AI
- Remediation planning

✅ **Agent Design Patterns:**
- Specialized vs. generalized agents
- When to use multiple agents
- Communication protocols
- Consensus building

### Technical Skills

You can now:

✅ **Build multi-agent systems** with AutoGen
✅ **Design agent roles** and responsibilities
✅ **Implement delegation** patterns
✅ **Integrate LLMs** into agent workflows
✅ **Test agent interactions**
✅ **Debug agent conversations**
✅ **Create incident response** workflows

### Real-World Patterns

You've learned:

✅ **Commander pattern** - Central coordinator delegating to specialists
✅ **Specialist agents** - Domain-specific expertise
✅ **Conversation management** - Multi-turn dialogues
✅ **Human-in-the-loop** - When AI escalates to humans

---

## 🆚 FREE vs PAID Comparison

| Feature | FREE Version | PAID Version |
|---------|-------------|--------------|
| **Number of Agents** | 2 (Commander + SRE) | 4+ (Commander, SRE, Security, Network) |
| **Tool Execution** | Simulated | ✅ Real kubectl (sandboxed) |
| **State Management** | In-memory | ✅ Redis persistence |
| **Audit Logging** | Console only | ✅ PostgreSQL audit trail |
| **Agent Specialization** | Basic | ✅ Advanced domain experts |
| **RBAC** | ❌ | ✅ Role-based access control |
| **Multi-round Dialogues** | Simple | ✅ Complex negotiations |
| **Tool Sandboxing** | ❌ | ✅ Secure execution |
| **Cost Tracking** | Basic | ✅ Detailed per-agent tracking |
| **Production Ready** | Learning | ✅ Yes |

---

## 💰 Cost Analysis

### Development/Testing: $0.50-1.00/day

**LLM costs:**
```
Testing: 20 investigations/day
Average: 400 tokens per investigation
Cost: 20 × 400 / 1000 × $0.002 = $0.016/day

Monthly: ~$0.50
```

### Light Production Use: $5-10/month

**With moderate usage:**
```
100 investigations/day
Monthly: 100 × 30 = 3,000 investigations
Tokens: 3,000 × 400 = 1,200,000 tokens
Cost: 1,200 × $0.002 = $2.40/month

Adding buffer for retries: ~$5/month
```

### Cost Optimization

**Strategies:**
1. Use GPT-3.5 for simple triage: 90% cheaper
2. Cache common investigation patterns
3. Optimize prompts to reduce tokens
4. Implement early termination for duplicate alerts

---

## 🔧 Troubleshooting

### Issue: Missing API Key

**Error:**
```
Error: OpenAI API key not found
```

**Solution:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
# Or add to .env file
```

### Issue: AutoGen Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'autogen'
```

**Solution:**
```bash
pip install -r requirements.txt
# Or specifically:
pip install pyautogen
```

### Issue: Agents Not Responding

**Check:**
```bash
# Verify API key is valid
python -c "import openai; openai.api_key='your-key'; print(openai.Model.list())"

# Check agent initialization
python src/run.py --debug
```

### Issue: Conversation Gets Stuck

**Solution:**
- Add max_consecutive_auto_reply limit
- Implement conversation termination conditions
- Check for circular delegation

---

## 🧹 Cleanup

```bash
# Run cleanup script
bash scripts/cleanup.sh

# Or manually
rm -rf .venv
rm -f .env
```

---

## 📚 Next Steps

### Extend This Lab

**1. Add More Agents:**
```python
# Security Agent
security_agent = AssistantAgent(
    name="SecuritySpecialist",
    system_message="You are a security expert..."
)

# Network Agent
network_agent = AssistantAgent(
    name="NetworkEngineer",
    system_message="You are a network specialist..."
)
```

**2. Implement Tool Execution:**
```python
def execute_kubectl(command):
    # Safe kubectl execution
    return subprocess.run(command, capture_output=True)
```

**3. Add Memory/State:**
```python
# Track conversation history
conversation_history = []

# Store investigation results
investigation_cache = {}
```

### Explore PAID Version

The PAID version adds:
- **4+ specialized agents** (SRE, Security, Network, Database)
- **Real tool execution** with sandboxed kubectl
- **Redis state management**
- **PostgreSQL audit logging**
- **Advanced workflows** with multi-agent negotiation
- **RBAC** for secure operations
- **Production observability**

---

## 🎉 Congratulations!

You've built your first multi-agent system!

### What You've Mastered:

✅ **Multi-Agent Design** - Collaborative AI agents  
✅ **AutoGen Framework** - Agent creation and orchestration  
✅ **Incident Response** - Automated triage and investigation  
✅ **Agent Communication** - Delegation and reporting patterns  
✅ **LLM Integration** - Connecting agents to language models  

You now understand how multiple AI agents work together!

Happy learning! 🔧
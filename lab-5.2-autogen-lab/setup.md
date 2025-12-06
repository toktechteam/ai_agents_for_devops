# Lab 5.2 FREE Setup Guide – AutoGen Multi-Agent Incident Response
## Building Your First Multi-Agent System

---

## 🎯 What You Will Achieve

By completing this setup, you will:

### Learning Objectives

1. **Install and Configure AutoGen** - Microsoft's multi-agent framework
2. **Create Two Collaborative Agents** - Commander and Investigator
3. **Implement Agent Communication** - Delegation and reporting patterns
4. **Test Multi-Agent Workflows** - Incident response automation
5. **Understand Agent Orchestration** - How agents coordinate

### Expected Outcomes

- ✅ Working AutoGen environment
- ✅ Two functional AI agents (Commander + Investigator)
- ✅ Agent-to-agent communication working
- ✅ Incident response workflow operational
- ✅ Test suite passing
- ✅ Understanding of multi-agent patterns

### Real-World Skills

**DevOps Engineers** will learn:
- Setting up multi-agent systems
- Building AI-powered automation
- Testing agent interactions

**SRE Teams** will learn:
- Automating incident response
- Creating AI assistants
- Agent-based troubleshooting

**ML Engineers** will learn:
- Deploying multi-agent frameworks
- Agent orchestration patterns
- LLM integration in agents

---

## 📋 Prerequisites

### Required Software

**1. Python 3.10 or higher**
```bash
python3 --version
```

**Expected:** `Python 3.10.x` or higher

**2. pip (Python package manager)**
```bash
pip --version
```

**3. Git (for cloning repositories)**
```bash
git --version
```

### Required API Keys

**OpenAI API Key:**
```bash
# You'll need this for LLM-powered agents
export OPENAI_API_KEY="sk-your-key-here"
```

Get your key from: https://platform.openai.com/api-keys

### Required Knowledge

- Basic Python programming
- Understanding of AI/LLM concepts
- Familiarity with incident response workflows

---

## 🏗️ Understanding Multi-Agent Architecture

### What You're Building

```
┌─────────────────────────────────────────────┐
│  Multi-Agent Incident Response System      │
│                                             │
│  Alert Input                                │
│      ↓                                      │
│  ┌─────────────────────────────┐           │
│  │  Incident Commander Agent   │           │
│  │  - Receives alert           │           │
│  │  - Assesses severity        │           │
│  │  - Delegates investigation  │           │
│  └─────────┬───────────────────┘           │
│            │                                │
│            │ "Investigate high CPU"         │
│            │                                │
│            ▼                                │
│  ┌─────────────────────────────┐           │
│  │  SRE Investigator Agent     │           │
│  │  - Analyzes problem         │           │
│  │  - Identifies root cause    │           │
│  │  - Suggests remediation     │           │
│  └─────────┬───────────────────┘           │
│            │                                │
│            │ Reports findings               │
│            │                                │
│            ▼                                │
│  Final Response with Remediation           │
└─────────────────────────────────────────────┘
```

### Agent Communication Flow

```
1. User submits alert
   ↓
2. Commander Agent receives it
   ↓
3. Commander delegates to SRE Investigator
   ↓
4. SRE Investigator performs analysis
   ↓
5. SRE reports back to Commander
   ↓
6. Commander presents final response
```

---

## 🚀 Step-by-Step Setup

### Step 1: Verify Python Installation

**Check Python version:**
```bash
python3 --version
```

**Expected Output:**
```
Python 3.10.12
```

**If Python < 3.10, install newer version:**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11
```

**macOS:**
```bash
brew install python@3.11
```

---

### Step 2: Clone Repository (or Navigate to Lab Directory)

**If cloning:**
```bash
git clone https://github.com/your-org/ai-agents-devops
cd labs/chapter-05/lab-5.2-autogen-incident-response-free
```

**Verify you're in the correct directory:**
```bash
ls
```

**Expected Output:**
```
README.md  requirements.txt  setup.md  src/  examples/  scripts/  tests/
```

---

### Step 3: Create Virtual Environment (Recommended)

**Create virtual environment:**
```bash
python3 -m venv .venv
```

**Activate virtual environment:**

**Linux/macOS:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Verify activation:**
```bash
which python
```

**Expected:** Path should include `.venv`

---

### Step 4: Install Dependencies

**Install all required packages:**
```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Collecting pyautogen==0.2.18
  Downloading pyautogen-0.2.18-py3-none-any.whl (234 kB)
Collecting openai>=1.0.0
  Downloading openai-1.12.0-py3-none-any.whl (226 kB)
Collecting python-dotenv>=1.0.0
  Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
Collecting pyyaml>=6.0
  Downloading PyYAML-6.0.1-cp311-cp311-linux_x86_64.whl (757 kB)
Collecting pytest>=7.4.0
  Downloading pytest-7.4.4-py3-none-any.whl (325 kB)
...
Successfully installed pyautogen-0.2.18 openai-1.12.0 python-dotenv-1.0.1 ...
```

**Verify installation:**
```bash
python -c "import autogen; print(autogen.__version__)"
```

**Expected Output:**
```
0.2.18
```

---

### Step 5: Configure OpenAI API Key

**Option 1: Environment Variable (Recommended for testing)**
```bash
export OPENAI_API_KEY="sk-your-actual-key-here"
```

**Verify:**
```bash
echo $OPENAI_API_KEY
```

**Expected:** Your API key should be displayed

**Option 2: Create .env file (Recommended for development)**
```bash
cp .env.example .env
```

**Edit .env:**
```bash
nano .env
# or
vim .env
```

**Add your key:**
```
OPENAI_API_KEY=sk-your-actual-key-here
```

**Save and exit**

---

### Step 6: Examine Agent Code

Before running, understand the agent structure.

**View agent definitions:**
```bash
cat src/agents.py | head -50
```

**Key components:**

**Incident Commander:**
```python
commander = AssistantAgent(
    name="IncidentCommander",
    system_message="""You are an experienced incident commander.
    Your role:
    - Receive and triage incoming alerts
    - Assess severity and impact
    - Delegate to appropriate specialists
    - Coordinate overall response
    """,
    llm_config={"model": "gpt-4", "temperature": 0.1}
)
```

**SRE Investigator:**
```python
investigator = AssistantAgent(
    name="SREInvestigator",
    system_message="""You are a senior SRE with expertise in:
    - Kubernetes troubleshooting
    - Performance analysis
    - Root cause identification
    Your task: Analyze technical issues and suggest fixes.
    """,
    llm_config={"model": "gpt-4", "temperature": 0.3}
)
```

---

### Step 7: Run Your First Investigation

**Start the application:**
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

───────────────────────────────────────────────────────
🚨 Incident Commander:
Alert received: High CPU on pod payment-service-1123
Severity: Warning
Delegating to SRE Investigator for technical analysis...
───────────────────────────────────────────────────────

───────────────────────────────────────────────────────
🧠 SRE Investigator:
Analyzing high CPU usage on payment-service-1123...

Root Cause Analysis:
The pod is experiencing CPU saturation (>90% utilization).
Probable causes:
1. Traffic spike beyond capacity
2. Inefficient code path being executed
3. Memory pressure causing excessive GC
4. Missing Horizontal Pod Autoscaler configuration

Evidence supporting this analysis:
- Pod CPU at 95% of 500m limit (475m used)
- No HPA configured for this deployment
- Recent deployment 2 hours ago may have regression

🔧 Recommended Remediation:

Immediate Actions:
1. Scale deployment to handle current load:
   kubectl scale deployment payment-service --replicas=5
   
2. Configure HPA for automatic scaling:
   kubectl autoscale deployment payment-service \
     --min=3 --max=10 --cpu-percent=70
   
3. Monitor the situation:
   kubectl top pod payment-service-1123
   kubectl logs payment-service-1123 --tail=100

Long-term Improvements:
- Review recent code changes for performance regressions
- Implement application performance profiling
- Set up proper resource requests and limits
- Configure alerts for abnormal CPU patterns
- Consider implementing circuit breakers
───────────────────────────────────────────────────────

───────────────────────────────────────────────────────
🚨 Incident Commander:
Investigation complete. Summary:

Root Cause: CPU saturation due to traffic spike and 
missing autoscaling configuration.

Immediate Action Required: Scale deployment and 
configure HPA.

Status: Ready for human review and approval.
───────────────────────────────────────────────────────

📊 Investigation Complete
═══════════════════════════════════════════════════════
Total conversation turns: 4
Agents involved: 2 (Commander, Investigator)
Time elapsed: 5.7 seconds
Estimated tokens used: ~520
Estimated cost: ~$0.0104
═══════════════════════════════════════════════════════
```

**What this validates:**
- ✅ Agents initialized successfully
- ✅ Commander received and triaged alert
- ✅ Delegation to SRE worked
- ✅ SRE performed analysis
- ✅ Remediation suggestions generated
- ✅ Multi-agent communication working

---

### Step 8: Test Different Alert Scenarios

**Test high CPU alert:**
```bash
python src/run.py --alert "High CPU on pod web-app-xyz"
```

**Test pod crash:**
```bash
python src/run.py --alert "CrashLoopBackOff in production namespace"
```

**Test memory issue:**
```bash
python src/run.py --alert "OOMKilled event on database pod"
```

**Expected:** Different investigations tailored to each alert type

---

### Step 9: Run Automated Tests

**Run all tests:**
```bash
pytest -v
```

**Expected Output:**
```
==================== test session starts ====================
platform linux -- Python 3.11.x, pytest-7.4.x
collected 8 items

tests/test_agents.py::test_commander_initialization PASSED        [12%]
tests/test_agents.py::test_investigator_initialization PASSED     [25%]
tests/test_agents.py::test_commander_delegation PASSED            [37%]
tests/test_agents.py::test_investigator_analysis PASSED           [50%]
tests/test_integration.py::test_full_workflow PASSED              [62%]
tests/test_integration.py::test_high_cpu_scenario PASSED          [75%]
tests/test_integration.py::test_crash_scenario PASSED             [87%]
tests/test_integration.py::test_memory_scenario PASSED            [100%]

==================== 8 passed in 12.45s ====================
```

**Run specific test:**
```bash
pytest tests/test_agents.py::test_commander_delegation -v
```

**Run with output:**
```bash
pytest -v -s
```

---

### Step 10: Examine Agent Conversation Logs

**View detailed conversation:**
```bash
python src/run.py --debug
```

**Expected output shows message exchange:**
```
DEBUG: Commander -> Investigator
{
  "role": "user",
  "content": "Investigate high CPU on pod payment-service-1123"
}

DEBUG: Investigator -> Commander
{
  "role": "assistant",
  "content": "Root cause identified: Traffic spike + missing HPA..."
}
```

---

### Step 11: Understand Agent Communication

**View communication flow:**
```bash
python src/run.py --show-messages
```

**Expected:**
```
Message Flow:
═════════════

[1] User → Commander
    "High CPU on pod payment-service-1123"

[2] Commander → Investigator
    "Please investigate high CPU on payment-service-1123.
     Identify root cause and suggest remediation."

[3] Investigator → Commander
    "Analysis complete. Root cause: Traffic spike.
     Recommendation: Scale deployment and add HPA."

[4] Commander → User
    "Investigation complete. See detailed report."
```

---

### Step 12: Customize Agent Behavior

**Modify agent persona:**
```bash
nano src/agents.py
```

**Example customization:**
```python
# Make investigator more detailed
investigator = AssistantAgent(
    name="SREInvestigator",
    system_message="""You are a senior SRE with 10+ years experience.
    Provide extremely detailed analysis with:
    - Step-by-step reasoning
    - Multiple evidence points
    - Specific kubectl commands
    - Both immediate and long-term recommendations
    """,
    llm_config={
        "model": "gpt-4",
        "temperature": 0.2  # Slightly more creative
    }
)
```

**Test changes:**
```bash
python src/run.py
```

---

## ✅ Testing and Validation

### Test 1: Agent Initialization

**Verify agents load correctly:**
```bash
python -c "
from src.agents import create_agents
commander, investigator = create_agents()
print(f'Commander: {commander.name}')
print(f'Investigator: {investigator.name}')
"
```

**Expected Output:**
```
Commander: IncidentCommander
Investigator: SREInvestigator
```

### Test 2: API Key Configuration

**Verify OpenAI connection:**
```bash
python -c "
import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
models = client.models.list()
print('✓ OpenAI API key valid')
"
```

**Expected:** `✓ OpenAI API key valid`

### Test 3: Agent Communication

**Test delegation pattern:**
```bash
pytest tests/test_agents.py::test_commander_delegation -v
```

**Expected:**
```
PASSED tests/test_agents.py::test_commander_delegation

Test validates:
  ✓ Commander receives alert
  ✓ Commander delegates to investigator
  ✓ Message format is correct
  ✓ Delegation includes context
```

### Test 4: Investigation Quality

**Test analysis depth:**
```bash
pytest tests/test_integration.py::test_investigation_quality -v
```

**Expected:**
```
PASSED tests/test_integration.py::test_investigation_quality

Test validates:
  ✓ Root cause identified
  ✓ Evidence provided
  ✓ Remediation suggestions given
  ✓ Both immediate and long-term fixes included
  ✓ Specific commands provided
```

### Test 5: Multiple Scenarios

**Run scenario suite:**
```bash
bash scripts/test.sh
```

**Expected Output:**
```
🧪 Testing Multiple Incident Scenarios
========================================

Scenario 1: High CPU
  ✓ Commander triaged correctly
  ✓ Investigation completed
  ✓ Remediation suggested

Scenario 2: Pod Crash
  ✓ Commander triaged correctly
  ✓ Investigation completed
  ✓ Remediation suggested

Scenario 3: Memory Issue
  ✓ Commander triaged correctly
  ✓ Investigation completed
  ✓ Remediation suggested

All scenarios passed! ✅
```

---

## 🎓 Understanding What You've Built

### Multi-Agent Pattern

**Traditional approach:**
```python
# Single monolithic function
def investigate_alert(alert):
    # Do everything in one place
    analysis = analyze(alert)
    remediation = suggest_fixes(analysis)
    return remediation
```

**Multi-agent approach:**
```python
# Specialized agents collaborating
commander.initiate_chat(
    investigator,
    message=f"Investigate: {alert}"
)
# Commander delegates
# Investigator specializes
# Both collaborate on solution
```

### Benefits of Multi-Agent Design

**Separation of concerns:**
- Commander handles coordination
- Investigator handles technical depth
- Each agent focused on expertise

**Scalability:**
- Easy to add new specialist agents
- Agents can be swapped or upgraded
- Parallel investigation possible

**Maintainability:**
- Each agent's logic is isolated
- Changes don't cascade
- Testing is simpler

---

## 💰 Cost Analysis

### Development/Testing: $0.50-1.00/day

**LLM usage:**
```
Testing: 20 investigations/day
Average conversation: 4 turns
Tokens per turn: ~130
Total tokens: 20 × 4 × 130 = 10,400 tokens

GPT-4 cost: 10.4K / 1000 × $0.002 = $0.021/day
With overhead: ~$0.50/day
Monthly: ~$15
```

### Light Production: $5-10/month

**100 investigations/day:**
```
Monthly investigations: 3,000
Tokens: 3,000 × 520 = 1,560,000 tokens
Cost: 1,560 × $0.002 = $3.12/month

With retries and overhead: ~$5-7/month
```

### Cost Optimization

**Strategies:**
1. **Use GPT-3.5 for triage**: Commander uses cheaper model
2. **Cache common patterns**: Store frequent investigation types
3. **Optimize prompts**: Reduce unnecessary tokens
4. **Early termination**: Skip investigation if duplicate alert

**Optimized costs:**
```
Commander (GPT-3.5): 90% cheaper
Investigator (GPT-4): When deep analysis needed
Result: $0.50-1.00/month for light production
```

---

## 🔧 Troubleshooting

### Issue: ModuleNotFoundError for autogen

**Error:**
```
ModuleNotFoundError: No module named 'autogen'
```

**Solution:**
```bash
pip install pyautogen
# Note: Package is "pyautogen" not "autogen"
```

### Issue: OpenAI API Key Not Found

**Error:**
```
openai.error.AuthenticationError: No API key provided
```

**Solution:**
```bash
# Check if key is set
echo $OPENAI_API_KEY

# If empty, set it
export OPENAI_API_KEY="sk-your-key-here"

# Or use .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### Issue: Agents Not Responding

**Check API key validity:**
```bash
python -c "
from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
print(client.models.list())
"
```

**If error, regenerate API key at:** https://platform.openai.com/api-keys

### Issue: Conversation Loops Indefinitely

**Add termination conditions:**
```python
commander = AssistantAgent(
    name="IncidentCommander",
    max_consecutive_auto_reply=3,  # Limit turns
    is_termination_msg=lambda msg: "investigation complete" in msg.lower()
)
```

### Issue: Rate Limit Errors

**Error:**
```
RateLimitError: You exceeded your current quota
```

**Solutions:**
1. Check OpenAI account has credits
2. Add rate limiting in code
3. Implement retry logic with backoff

---

## 🧹 Cleanup

**Deactivate virtual environment:**
```bash
deactivate
```

**Remove virtual environment:**
```bash
rm -rf .venv
```

**Clean generated files:**
```bash
bash scripts/cleanup.sh
```

**Or manually:**
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
rm -f .env
```

---

## 📊 Success Criteria Checklist

Your lab is complete when:

- [ ] Python 3.10+ installed
- [ ] Dependencies installed successfully
- [ ] OpenAI API key configured
- [ ] Agents initialize without errors
- [ ] First investigation completes successfully
- [ ] Commander delegates to investigator
- [ ] Investigator provides analysis and remediation
- [ ] All tests pass (8/8)
- [ ] Multiple scenarios tested
- [ ] You understand agent communication flow
- [ ] You understand multi-agent benefits
- [ ] You can customize agent behavior

---

## 📚 Next Steps

### Extend the System

**1. Add more agents:**
```python
security_agent = AssistantAgent(
    name="SecuritySpecialist",
    system_message="You are a security expert..."
)

network_agent = AssistantAgent(
    name="NetworkEngineer",
    system_message="You are a network specialist..."
)
```

**2. Implement tool execution:**
```python
def execute_kubectl(command):
    # Add actual kubectl execution
    pass
```

**3. Add conversation memory:**
```python
# Track investigation history
conversation_db = {}

# Reference past investigations
if similar_alert_in_history:
    return cached_solution
```

### Explore PAID Version

The PAID version includes:
- **4+ specialized agents**
- **Real kubectl execution**
- **Redis for state management**
- **PostgreSQL audit logging**
- **Advanced multi-agent workflows**
- **RBAC for security**

---

## 🎉 Congratulations!

You've built your first multi-agent system!

### What You've Accomplished:

✅ **Multi-Agent Setup** - Two agents collaborating  
✅ **AutoGen Framework** - Working with modern AI tools  
✅ **Agent Communication** - Delegation patterns  
✅ **Incident Response** - Automated investigation  
✅ **Testing** - Validated agent behavior  

You now understand how AI agents work together!

Happy learning! 🚀🤖👥🔧
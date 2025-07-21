# FREE Lab - Chapter 01 Part 01 - Hands-on Lab 1.1: Setting Up Your First Model Inference API

**From the Book:** "AI Agents for DevOps: Architect, Deploy, and Automate Like a Pro"

## 🎯 Lab Objective
Experience the operational differences between traditional APIs and model inference services by deploying both and comparing their characteristics. This lab demonstrates why AI/ML services require fundamentally different DevOps patterns compared to traditional web applications.

## 📋 Prerequisites
- Docker and Docker Compose installed
- 8GB RAM minimum (12GB recommended)
- Python 3.8+ environment
- Stable internet connection (for model downloads)
- Basic understanding of REST APIs

## ⏱️ Time Required
**45 minutes** (including model download time)

## 📁 Lab Files Structure
```
labs/chapter-01/lab-11-free/
├── README.md                      # This guide
├── docker-compose.yml             # Multi-service deployment
├── app_traditional.py             # Rule-based sentiment API
├── app_ml.py                     # ML transformer-based API
├── Dockerfile.traditional        # Traditional API container
├── Dockerfile.ml                 # ML API container
├── nginx.conf                    # Load balancer configuration
├── requirements-traditional.txt   # Lightweight dependencies
├── requirements-ml.txt           # ML framework dependencies
└── setup.md                     # Step-by-step instructions
```

## 🚀 What You'll Experience

### 1. Deploy a Traditional REST API (starts in seconds)
- **Startup Time**: ~3 seconds
- **Memory Usage**: ~50MB
- **Response Time**: <10ms
- **Technology**: Rule-based sentiment analysis
- **Scaling**: Perfect horizontal scaling

### 2. Deploy an ML Model API (watch the startup time)
- **Startup Time**: ~30-45 seconds (model loading)
- **Memory Usage**: ~1.2GB (model weights)
- **Response Time**: 100-500ms
- **Technology**: DistilBERT transformer model
- **Scaling**: Cold start challenges

### 3. Compare Resource Usage Patterns
- Monitor CPU and memory consumption differences
- Observe startup behavior variations
- Analyze response time patterns under load
- Study scaling characteristics

### 4. Implement Proper Health Checks for Each
- Traditional API: Simple liveness checks
- ML API: Separate liveness vs readiness checks
- Understand why ML APIs need different health check strategies

### 5. Observe Scaling Behavior Differences
- Traditional: Instant horizontal scaling
- ML: Cold start problem demonstration
- Resource allocation challenges
- Cost implications analysis

## 🎓 Key Insights You'll Gain

### Why Model Loading Time Matters
- **Cold Start Problem**: New ML service instances take 30+ seconds to become ready
- **Production Impact**: Cannot handle traffic spikes with traditional auto-scaling
- **Solution Preview**: Warm pools, model caching (covered in paid version)

### How Memory Patterns Differ
- **Traditional APIs**: Predictable, low memory usage (~50MB)
- **ML APIs**: High baseline memory for model weights (~1.2GB)
- **Scaling Cost**: Each replica multiplies memory requirements
- **Optimization**: Model quantization and sharing strategies (paid version)

### When Horizontal Scaling Breaks Down
- **Traditional Pattern**: Add more replicas = handle more traffic
- **ML Reality**: New replicas = 30s delay + 1.2GB RAM each
- **Business Impact**: Poor user experience during scaling events
- **Advanced Solutions**: Smart scheduling and resource pooling

### Why Warm Pools are Necessary
- **Problem**: Cannot wait 30s for new capacity
- **Traditional Solution**: Pre-warmed instances consume resources
- **Smart Solution**: Dynamic warm pool management (paid version)
- **Cost Balance**: Availability vs resource costs

## 🏗️ Real Scenario Context
You're a DevOps engineer tasked with deploying a sentiment analysis service for a customer feedback platform. The business wants to upgrade from a simple rule-based system to an advanced AI model. You'll experience firsthand the operational challenges this seemingly simple upgrade introduces.

**Business Requirements:**
- Handle customer feedback in real-time
- Scale automatically during marketing campaigns
- Maintain 99.9% uptime
- Keep infrastructure costs reasonable

**Your Challenge:**
Deploy both systems and discover why the AI upgrade requires rethinking your entire operational strategy.

## 💡 Learning Outcomes

By completing this lab, you will:

1. **Understand AI/ML Operational Complexity**
   - Experience the difference between deploying traditional vs ML services
   - Recognize why existing DevOps patterns may not work for AI workloads

2. **Master Health Check Strategies**
   - Learn when to use liveness vs readiness probes
   - Understand why ML services need different monitoring approaches

3. **Identify Scaling Challenges**
   - Witness the cold start problem in action
   - Understand resource planning for ML workloads

4. **Recognize Cost Implications**
   - See how memory requirements affect scaling costs
   - Understand why ML services need different cost optimization strategies

5. **Gain Career-Relevant Skills**
   - Hands-on experience with ML deployment challenges
   - Understanding of production AI/ML operational patterns
   - Knowledge that's immediately applicable in modern DevOps roles

## 🔬 Experiments You'll Perform

### Experiment 1: Startup Time Analysis
Compare cold start times and analyze the impact on service availability.

### Experiment 2: Resource Monitoring
Track CPU, memory, and disk usage patterns for both service types.

### Experiment 3: Load Testing
Observe how each service handles concurrent requests and scaling scenarios.

### Experiment 4: Health Check Behavior
Understand the difference between service availability and readiness.

### Experiment 5: Scaling Simulation
Experience the challenges of horizontal scaling with ML workloads.

## 🚨 Common Challenges You'll Encounter

1. **Long Model Download Time**: First run takes extra time for model download
2. **Memory Pressure**: ML service may struggle on systems with <8GB RAM
3. **Cold Start Delays**: New ML instances take time to become ready
4. **Resource Competition**: Both services competing for system resources

**These challenges are intentional** - they represent real production problems you'll face when deploying AI/ML systems.

## 📈 Career Value

This lab provides direct experience with:
- **AI/ML Operations**: Growing field with high demand
- **Container Orchestration**: Essential DevOps skill
- **Performance Analysis**: Critical for senior roles
- **Resource Planning**: Key for infrastructure roles
- **Monitoring Strategy**: Foundation for SRE positions

## 🛠️ Quick Start

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd labs/chapter-01/lab-11-free
   ```

2. **Start the Environment**
   ```bash
   docker-compose up -d
   ```

3. **Monitor the Startup**
   ```bash
   docker-compose logs -f
   ```

4. **Begin Experiments**
   Follow the detailed instructions in `setup.md`

## 🎯 Success Criteria

You'll know you've successfully completed this lab when you can:
- ✅ Deploy both traditional and ML APIs successfully
- ✅ Explain the startup time differences
- ✅ Identify memory usage patterns
- ✅ Demonstrate the scaling challenges
- ✅ Articulate why ML services need different operational approaches

## 🔄 What's Next?

This FREE lab gives you hands-on experience with basic AI/ML deployment challenges. You'll understand the fundamental operational differences and why traditional DevOps patterns need adaptation for AI workloads.

**Ready for Production-Grade AI/ML Operations?**
The PAID version of this lab includes:
- Kubernetes deployment strategies
- Advanced monitoring with Prometheus/Grafana
- Auto-scaling solutions for ML workloads
- Production optimization techniques
- Real-world troubleshooting scenarios
- Interview preparation materials

## 💬 Questions for Reflection

After completing this lab, consider:
1. How would you explain the cold start problem to a business stakeholder?
2. What would happen to your cloud costs if you naively scaled ML services?
3. How might you design a system to handle both predictable and spike traffic?
4. What monitoring strategies would you implement for production ML services?

---

**🎓 Part of the comprehensive "AI Agents for DevOps" learning path**
**📚 This is a FREE lab - upgrade to PAID for production-grade scenarios**
**📚 Reach out to us at help@theopskart.com/toktechteam@gmail.com or visit our website www.theopskart.com**

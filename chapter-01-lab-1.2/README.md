# FREE Lab - Chapter 1 Part 2 - Hands-on Lab 1.2: Comparing API vs Self-hosted Model Performance

**From the Book:** "AI Agents for DevOps: Architect, Deploy, and Automate Like a Pro"

##  Lab Objective
Build intuition for the trade-offs between API-based and self-hosted model serving through hands-on comparison. Experience the operational and cost implications of each approach using a real document summarization service.

##  Prerequisites
- Completed Lab 1.1 (Model Inference API basics)
- OpenAI API key (free tier sufficient for testing)
- Docker and Docker Compose installed
- 8GB RAM minimum (for self-hosted model)
- Basic understanding of API consumption

##  Time Required
**60 minutes** (including model downloads and performance testing)

## 📁 Lab Files Structure
```
labs/chapter-01/lab-12-free/
├── README.md                           # This comprehensive guide
├── docker-compose.yml                  # Multi-service deployment
├── src/
│   ├── api_service.py                  # OpenAI API-based service
│   ├── selfhosted_service.py           # Local model service
│   └── shared/
│       ├── models.py                   # Data models
│       └── utils.py                    # Common utilities
├── config/
│   ├── api_config.yaml                 # API service configuration
│   └── selfhosted_config.yaml          # Self-hosted configuration
├── requirements-api.txt                # Lightweight API dependencies
├── requirements-selfhosted.txt         # Heavy ML dependencies
├── Dockerfile.api                      # API service container
├── Dockerfile.selfhosted               # Self-hosted service container
├── test_performance.py                 # Performance comparison script
└── setup.md                           # Manual setup instructions
```

##  What You'll Experience

### 1. Deploy API-Based Document Summarization
- **Startup Time**: ~3 seconds (instant model access)
- **Memory Usage**: ~100MB (no model weights)
- **Latency**: ~200-500ms (network + OpenAI processing)
- **Cost Model**: Pay-per-request ($0.002/request)
- **Scaling**: Instant (OpenAI handles it)

### 2. Deploy Self-Hosted Model Summarization
- **Startup Time**: ~45 seconds (model loading)
- **Memory Usage**: ~2.5GB (model weights + processing)
- **Latency**: ~50-150ms (local processing only)
- **Cost Model**: Fixed infrastructure (~$500/month base)
- **Scaling**: 5+ minutes for new instances

### 3. Measure Performance Differences
- Compare end-to-end latency patterns
- Analyze cost breakeven calculations
- Monitor resource utilization differences
- Test concurrent request handling

### 4. Experience Cold Start Impact
- API services: No cold start (OpenAI always ready)
- Self-hosted: Significant cold start delay
- Load balancing and failover behavior

### 5. Understand Operational Complexity
- API: Simple deployment, external dependency
- Self-hosted: Complex deployment, full ownership

##  Key Insights You'll Gain

### When to Use API Services
- **Low Volume**: <10,000 requests/month
- **Variable Load**: Unpredictable traffic patterns
- **Fast MVP**: Need to ship quickly
- **Limited DevOps**: Small team, simple operations
- **Latest Models**: Access to cutting-edge capabilities

### When to Use Self-Hosted Models
- **High Volume**: >100,000 requests/month
- **Consistent Load**: Predictable traffic
- **Data Privacy**: Sensitive information processing
- **Cost Control**: Predictable infrastructure costs
- **Customization**: Need model fine-tuning

### Latency Breakdown Analysis
- **API Service**: Network (100-300ms) + Processing (100-200ms)
- **Self-hosted**: Processing only (50-150ms)
- **Critical Insight**: Network latency often dominates API calls

### Cost Model Understanding
- **API**: Variable cost, scales with usage
- **Self-hosted**: Fixed cost, economies of scale kick in
- **Breakeven Point**: ~25,000 requests/month (varies by model)

##  Real Scenario Context
You're a DevOps engineer at a content management startup. The product team wants to add AI-powered document summarization to help users quickly understand long documents. The business requirements are:

**Business Requirements:**
- Summarize documents up to 10,000 words
- Handle 1,000-50,000 requests per month (growing)
- Response time under 2 seconds
- Cost-effective solution
- High availability (99.9% uptime)

**Your Challenge:**
Evaluate both approaches and provide a technical recommendation with cost analysis and operational trade-offs.

##  Learning Outcomes

By completing this lab, you will:

1. **Master Cost-Performance Trade-offs**
   - Calculate breakeven points for API vs self-hosted
   - Understand variable vs fixed cost models
   - Analyze total cost of ownership (TCO)

2. **Gain Latency Analysis Skills**
   - Decompose end-to-end response times
   - Identify network vs processing bottlenecks
   - Optimize for different latency requirements

3. **Understand Scaling Patterns**
   - Experience instant API scaling vs infrastructure scaling
   - Learn capacity planning for each approach
   - Recognize scaling limitations and solutions

4. **Develop Architecture Decision Skills**
   - Evaluate technical trade-offs systematically
   - Consider operational complexity in decisions
   - Balance business requirements with technical constraints

5. **Build Production Readiness Intuition**
   - Understand dependency management strategies
   - Learn monitoring requirements for each approach
   - Recognize failure modes and mitigation strategies

##  Experiments You'll Perform

### Experiment 1: Startup Time Comparison
Compare cold start behavior and time to readiness for both approaches.

### Experiment 2: Latency Benchmarking
Measure response times under different load conditions and document sizes.

### Experiment 3: Cost Calculation
Calculate costs at different usage volumes (100, 1K, 10K, 100K requests/month).

### Experiment 4: Concurrent Load Testing
Test how each approach handles multiple simultaneous requests.

### Experiment 5: Failure Mode Analysis
Simulate network issues, rate limits, and service failures.

## Common Challenges You'll Encounter

1. **API Rate Limiting**: Experience OpenAI rate limits in action
2. **Model Loading Time**: Self-hosted service takes time to become ready
3. **Memory Pressure**: Large models consume significant resources
4. **Network Variability**: API latency varies with network conditions
5. **Cost Estimation**: Complex calculations with multiple variables

**These challenges represent real production decisions** you'll face when architecting AI-powered systems.

##  Career Value

This lab provides direct experience with:
- **Cloud vs On-Premise**: Classic infrastructure decision-making
- **Cost Optimization**: Critical for senior engineering roles
- **Performance Analysis**: Essential for systems architecture
- **Vendor Management**: Understanding external service dependencies
- **Capacity Planning**: Key skill for infrastructure roles

### Interview Questions You'll Be Prepared For:
- "When would you choose an API service vs self-hosting?"
- "How do you calculate the cost breakeven point for build vs buy?"
- "What are the latency implications of external API dependencies?"
- "How do you design for high availability with external services?"

##  Quick Start

1. **Set Up Environment**
   ```bash
   git clone <repository-url>
   cd labs/chapter-01/lab-12-free
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Start Services**
   ```bash
   docker-compose up -d
   ```

3. **Run Performance Tests**
   ```bash
   python test_performance.py
   ```

4. **Analyze Results**
   Follow detailed instructions in `setup.md`

##  Success Criteria

You'll know you've successfully completed this lab when you can:
- ✅ Deploy both API and self-hosted summarization services
- ✅ Measure and explain latency differences
- ✅ Calculate cost breakeven points accurately
- ✅ Identify when to use each approach
- ✅ Articulate operational trade-offs clearly
- ✅ Design monitoring strategies for both approaches

##  Expected Performance Results

| Metric | API Service | Self-hosted |
|--------|-------------|-------------|
| Startup Time | 3 seconds | 45 seconds |
| Memory Usage | 100MB | 2.5GB |
| Response Latency | 200-500ms | 50-150ms |
| Cold Start Impact | None | Significant |
| Cost @ 1K req/month | $2 | $500 |
| Cost @ 100K req/month | $200 | $500 |
| Scaling Time | Instant | 5+ minutes |

##  What's Next?

This FREE lab demonstrates the fundamental trade-offs between API and self-hosted ML services. You'll understand cost models, performance characteristics, and operational complexity differences.

**Ready for Production-Grade ML Architecture?**
The PAID version of this lab includes:
- Multi-region deployment strategies
- Advanced monitoring and alerting
- Hybrid architectures (API + self-hosted)
- Cost optimization techniques
- Enterprise-scale scenarios
- Disaster recovery planning

##  Questions for Reflection

After completing this lab, consider:
1. At what request volume would you switch from API to self-hosted?
2. How would you handle API service outages in production?
3. What metrics would you monitor for each approach?
4. How would you explain the cost trade-offs to a non-technical stakeholder?
5. What security implications exist for each approach?

---

** Part of the comprehensive "AI Agents for DevOps" learning path**
** This is a FREE lab - upgrade to PAID for production-grade scenarios**

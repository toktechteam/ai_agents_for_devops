# Setup Instructions - Lab 1.2 FREE

##  Prerequisites Check

Before starting, verify you have:

```bash
# Check Docker
docker --version
# Should show: Docker version 20.x or higher

# Check Docker Compose
docker-compose --version  
# Should show: docker-compose version 1.29 or higher

# Check available memory
free -h
# Should show at least 4GB available (8GB recommended)

# Check OpenAI API Key
echo $OPENAI_API_KEY
# Should show your API key (get free one from OpenAI)
```

##  OpenAI API Key Setup

If you don't have an OpenAI API key:

```bash
# 1. Visit: https://platform.openai.com/api-keys
# 2. Create account and generate API key
# 3. Set environment variable:
export OPENAI_API_KEY="your-api-key-here"

# 4. Add to your shell profile for persistence:
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

##  Manual Setup Steps

### 1. Create Project Structure
```bash
# Create lab directory
mkdir -p labs/chapter-01/lab-12-free
cd labs/chapter-01/lab-12-free

# Create source directories
mkdir -p src/shared
mkdir -p config
mkdir -p test_results
```

### 2. Create Docker Files

Create `Dockerfile.api`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["python", "src/api_service.py"]
```

Create `Dockerfile.selfhosted`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements-selfhosted.txt .
RUN pip install --no-cache-dir -r requirements-selfhosted.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Create model cache directory
RUN mkdir -p /app/models

# Health check (longer timeout for ML)
HEALTHCHECK --interval=60s --timeout=30s --start-period=60s --retries=5 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["python", "src/selfhosted_service.py"]
```

Create `Dockerfile.tester`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install requests

# Copy test script
COPY test_performance.py .
COPY src/ ./src/

# Create results directory
RUN mkdir -p /app/results

CMD ["python", "test_performance.py"]
```

### 3. Create Requirements Files

Create `requirements-api.txt`:
```
Flask==2.3.3
openai==0.28.1
PyYAML==6.0.1
pydantic==1.10.12
requests==2.31.0
```

Create `requirements-selfhosted.txt`:
```
Flask==2.3.3
torch==2.0.1
transformers==4.33.2
PyYAML==6.0.1
pydantic==1.10.12
requests==2.31.0
```

### 4. Create Nginx Configuration
Create `nginx.conf`:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api-service:8000;
    }
    
    upstream selfhosted {
        server selfhosted-service:8000;
    }
    
    server {
        listen 80;
        
        location /api/ {
            proxy_pass http://api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_read_timeout 60s;
        }
        
        location /selfhosted/ {
            proxy_pass http://selfhosted/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_read_timeout 60s;
        }
        
        location / {
            return 200 'API vs Self-hosted Comparison Lab\nAPI Service: /api/\nSelf-hosted Service: /selfhosted/\n';
            add_header Content-Type text/plain;
        }
    }
}
```

##  Deployment Steps

### 1. Set Environment Variable
```bash
# Ensure OpenAI API key is set
export OPENAI_API_KEY="your-api-key-here"

# Verify it's set
echo "API Key: ${OPENAI_API_KEY:0:10}..."
```

### 2. Build and Start Services
```bash
# Build all images (this will take several minutes for ML dependencies)
docker-compose build

# Start services
docker-compose up -d

# Monitor startup progress
docker-compose logs -f
```

### 3. Verify Service Startup

Check service status:
```bash
# Check container status
docker-compose ps

# Should show:
# - api-service (healthy)
# - selfhosted-service (starting/healthy)
# - nginx-lb (healthy)
# - portainer (healthy)
```

Monitor the self-hosted service startup (takes ~45 seconds):
```bash
# Watch self-hosted service logs
docker-compose logs -f selfhosted-service

# Look for these key messages:
# " Loading local summarization model..."
# " Loading model: facebook/bart-large-cnn"
# " Model loaded successfully in X.XXs"
```

### 4. Test Basic Connectivity
```bash
# Test API service (should respond immediately)
curl http://localhost:8001/health

# Test self-hosted service (wait until model loaded)
curl http://localhost:8002/health

# Test load balancer
curl http://localhost:8080/
```

##  Running the Experiments

### Experiment 1: Basic Functionality Test
```bash
# Test API service
curl -X POST http://localhost:8001/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial Intelligence has revolutionized many industries. Machine learning algorithms can process vast amounts of data to identify patterns and make predictions. This technology is being applied in healthcare, finance, and many other sectors. Neural networks have particularly advanced the field, enabling computers to perform tasks that were once thought to be exclusively human capabilities. The development continues at a rapid pace with new breakthroughs happening regularly."
  }'

# Test self-hosted service (ensure model is loaded first)
curl -X POST http://localhost:8002/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial Intelligence has revolutionized many industries. Machine learning algorithms can process vast amounts of data to identify patterns and make predictions. This technology is being applied in healthcare, finance, and many other sectors. Neural networks have particularly advanced the field, enabling computers to perform tasks that were once thought to be exclusively human capabilities. The development continues at a rapid pace with new breakthroughs happening regularly."
  }'
```

### Experiment 2: Performance Comparison
```bash
# Run comprehensive performance tests
python test_performance.py

# This will test:
# - Latency differences
# - Concurrent load handling
# - Cost calculations
# - Generate detailed report
```

### Experiment 3: Resource Monitoring
```bash
# Monitor resource usage in real-time
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# Access Portainer for visual monitoring
# Open: http://localhost:9000
# Setup admin password and connect to local Docker
```

### Experiment 4: Cold Start Comparison
```bash
# Test cold start behavior
echo "=== Cold Start Test ==="

# Stop and restart API service
echo "Restarting API service..."
docker-compose restart api-service
time curl -f http://localhost:8001/health

# Stop and restart self-hosted service
echo "Restarting self-hosted service..."
docker-compose restart selfhosted-service

# Monitor startup time
echo "Monitoring self-hosted startup..."
start_time=$(date +%s)
while ! curl -f http://localhost:8002/ready 2>/dev/null; do
  echo "Still loading model..."
  sleep 5
done
end_time=$(date +%s)
echo "Self-hosted ready in $((end_time - start_time)) seconds"
```

### Experiment 5: Cost Analysis
```bash
# Get service metrics for cost comparison
echo "=== Cost Analysis ==="

# API service characteristics
curl http://localhost:8001/metrics | jq .characteristics.cost_model

# Self-hosted service characteristics  
curl http://localhost:8002/metrics | jq .characteristics.cost_model

# Direct comparison
curl http://localhost:8001/compare | jq .breakeven_analysis
```

##  What to Observe and Document

### 1. Startup Time Differences
- **API Service**: Ready in ~3 seconds
- **Self-hosted**: Takes 45+ seconds for model loading
- **Business Impact**: Self-hosted can't handle immediate traffic after restart

### 2. Memory Usage Patterns
```bash
# Check memory usage
docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}"

# Expected results:
# api-service: ~100-200MB
# selfhosted-service: ~2.5-3GB
```

### 3. Latency Characteristics
- **API Service**: 200-800ms (network + OpenAI processing)
- **Self-hosted**: 50-200ms (local processing only)
- **Key Insight**: Network latency often dominates API calls

### 4. Cost Implications
Document at different volumes:
- **1K requests/month**: API cheaper ($2 vs $500)
- **25K requests/month**: Break-even point
- **100K requests/month**: Self-hosted much cheaper ($500 vs $200)

### 5. Scaling Behavior
- **API**: Instant scaling (OpenAI handles it)
- **Self-hosted**: 5+ minutes for new instances (cold start problem)

##  Troubleshooting

### Common Issues

**OpenAI API errors:**
```bash
# Check API key
echo $OPENAI_API_KEY

# Test API connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models | jq .data[0].id
```

**Self-hosted model loading fails:**
```bash
# Check logs for specific error
docker-compose logs selfhosted-service

# Common fixes:
# 1. Ensure 8GB+ RAM available
# 2. Check internet for model download
# 3. Wait full 60 seconds for initial download
```

**Out of memory errors:**
```bash
# Check system resources
free -h
docker system df

# Free up space if needed
docker system prune -f
```

**Performance test failures:**
```bash
# Ensure both services are ready
curl http://localhost:8001/health
curl http://localhost:8002/ready

# Check if API key is working
curl http://localhost:8001/metrics | grep api_status
```

##  Expected Results Summary

After successful setup, you should observe:

| Metric | API Service | Self-hosted Service |
|--------|-------------|-------------------|
| Startup Time | 3 seconds | 45 seconds |
| Memory Usage | 100MB | 2.5GB |
| Response Latency | 300-600ms | 80-150ms |
| Cost @ 1K req/month | $2 | $500 |
| Cost @ 100K req/month | $200 | $500 |
| Scaling Time | Instant | 5+ minutes |

##  Cleanup
```bash
# Stop all services
docker-compose down

# Remove images (optional)
docker-compose down --rmi all

# Clean up system (optional)
docker system prune -f

# Remove test results
rm -rf test_results/
```

##  Success Validation

You've successfully completed the lab when you can:
- ✅ Both services respond to health checks
- ✅ Both services can summarize text successfully
- ✅ Performance tests run and generate report
- ✅ You understand the cost/performance trade-offs
- ✅ You can explain when to use each approach

##  Next Steps

1. **Analyze Results**: Review the generated performance report
2. **Document Insights**: Record your observations about trade-offs
3. **Apply Learning**: Consider how this applies to your current projects
4. **Share Knowledge**: Explain the concepts to a colleague

**Ready for production-grade scenarios?** The PAID version includes multi-region deployments, advanced monitoring, and enterprise decision frameworks!

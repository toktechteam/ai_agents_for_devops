# Setup Instructions - Lab 1.1 FREE

## 📋 Prerequisites Check

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

# Check available disk space
df -h
# Should show at least 5GB free space
```

### Install docker and docker-compose command
```
# 1. Update the packages
sudo yum update -y

# 2. Install Docker
sudo amazon-linux-extras enable docker
sudo yum install -y docker

# 3. Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# 4. Add ec2-user to docker group (so you can run docker without sudo)
sudo usermod -aG docker ec2-user

# 5. Install Docker Compose (v2 via plugin method)
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '"tag_name": "\K[^"]+')
sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose

# 6. Apply executable permissions
sudo chmod +x /usr/local/bin/docker-compose

# 7. Verify installations
docker --version
docker-compose --version


```



## 🛠️ Manual Setup Steps

### 1. Create Project Structure
```bash
# Create lab directory
mkdir -p labs/chapter-01/lab-11-free
cd labs/chapter-01/lab-11-free

# Create Docker files (you'll need to create these)
touch Dockerfile.traditional
touch Dockerfile.ml
touch nginx.conf
```

### 2. Create Traditional API Dockerfile
Create `Dockerfile.traditional`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements-traditional.txt .
RUN pip install --no-cache-dir -r requirements-traditional.txt

# Copy application code
COPY app_traditional.py app.py

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["python", "app.py"]
```

### 3. Create ML API Dockerfile  
Create `Dockerfile.ml`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements-ml.txt .
RUN pip install --no-cache-dir -r requirements-ml.txt

# Copy application code
COPY app_ml.py app.py

# Health check (longer timeout for ML)
HEALTHCHECK --interval=60s --timeout=30s --start-period=60s --retries=5 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["python", "app.py"]
```

### 4. Create Requirements Files

Create `requirements-traditional.txt`:
```
Flask==2.3.3
gunicorn==21.2.0
```

Create `requirements-ml.txt`:
```
Flask==2.3.3
torch==2.0.1
transformers==4.33.2
tensorflow==2.13.0
gunicorn==21.2.0
```

### 5. Create Nginx Configuration
Create `nginx.conf`:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream traditional {
        server traditional-api:8000;
    }
    
    upstream ml {
        server ml-api:8000;
    }
    
    server {
        listen 80;
        
        location /traditional/ {
            proxy_pass http://traditional/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location /ml/ {
            proxy_pass http://ml/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location / {
            return 200 'Load Balancer Active\nTraditional API: /traditional/\nML API: /ml/\n';
            add_header Content-Type text/plain;
        }
    }
}
```

## 🚀 Deployment Steps

### 1. Build and Start Services
```bash
# Build images (this will take a few minutes for ML dependencies)
docker-compose build

# Start services
docker-compose up -d

# Monitor startup progress
docker-compose logs -f
```

### 2. Verify Services are Running
```bash
# Check service status
docker-compose ps

# Should show:
# - traditional-api (healthy)
# - ml-api (starting/healthy) 
# - nginx-lb (healthy)
# - portainer (healthy)
```

### 3. Wait for ML Model Loading
```bash
# Monitor ML API startup (takes ~30 seconds)
docker-compose logs -f ml-api

# Look for: "✅ Model loaded successfully"
```

### 4. Test Basic Connectivity
```bash
# Test traditional API (should respond immediately)
curl http://localhost:8001/health

# Test ML API (wait until model loaded)
curl http://localhost:8002/health

# Test load balancer
curl http://localhost:8080/
```

## 🧪 Running the Experiments

### Experiment 1: Startup Time Comparison
```bash
# Kill services
docker-compose down

# Time traditional API startup
echo "Starting traditional API..."
time docker-compose up -d traditional-api
# Watch logs: docker-compose logs -f traditional-api

# Time ML API startup  
echo "Starting ML API..."
time docker-compose up -d ml-api
# Watch logs: docker-compose logs -f ml-api
```

### Experiment 2: Performance Testing
```bash
# Test traditional API
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'

# Test ML API (ensure it's ready first)
curl -X POST http://localhost:8002/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'

# Compare response times and accuracy
```

### Experiment 3: Resource Monitoring
```bash
# Monitor resource usage
docker stats

# Access Portainer for visual monitoring
# Open: http://localhost:9000
# Setup admin password and connect to local Docker
```

### Experiment 4: Load Testing
```bash
# Simple parallel requests to traditional API
echo "Testing traditional API with 10 parallel requests..."
for i in {1..10}; do
  (curl -s -X POST http://localhost:8001/analyze \
    -H "Content-Type: application/json" \
    -d '{"text": "Test message '$i'"}' && echo) &
done
wait

# Same test for ML API
echo "Testing ML API with 10 parallel requests..."
for i in {1..10}; do
  (curl -s -X POST http://localhost:8002/analyze \
    -H "Content-Type: application/json" \
    -d '{"text": "Test message '$i'"}' && echo) &
done
wait
```

## 🔍 Troubleshooting

### Common Issues

**ML API stuck in "starting" state:**
```bash
# Check logs for errors
docker-compose logs ml-api

# Common fixes:
# 1. Ensure 4GB+ RAM available
# 2. Wait full 60 seconds for model download
# 3. Check internet connection for model download
```

**Out of memory errors:**
```bash
# Check system resources
free -h
docker system df

# Cleanup if needed:
docker system prune -f
```

**Port conflicts:**
```bash
# Check if ports are in use
netstat -tulpn | grep :8001
netstat -tulpn | grep :8002

# Kill conflicting processes or change ports in docker-compose.yml
```

## 📊 Expected Results

After successful setup, you should observe:

1. **Traditional API**: Starts in ~3 seconds, uses ~50MB RAM
2. **ML API**: Takes ~30 seconds to start, uses ~1.2GB RAM  
3. **Response Times**: Traditional <10ms, ML 100-500ms
4. **Load Handling**: Traditional scales well, ML shows bottlenecks

## 🧹 Cleanup
```bash
# Stop all services
docker-compose down

# Remove images (optional)
docker-compose down --rmi all

# Clean up system (optional)
docker system prune -f
```

## 🚀 Next Steps

Once you've completed the experiments:
1. Document your observations
2. Compare startup times and resource usage
3. Note the operational challenges with ML APIs
4. Consider how these patterns affect production deployments

**Ready for production-grade ML ops?** The PAID version includes Kubernetes deployment, auto-scaling, monitoring, and optimization strategies!

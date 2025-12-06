## Prerequisites
- EC2 instance with Ubuntu 22.04 or 24.04 LTS
- Instance type: t3.medium or larger (4GB RAM minimum)
- Storage: 20GB minimum
- Security Group configured (see below)
- Internet connection

## Step 0: EC2 Security Group Configuration

Configure your EC2 Security Group with these inbound rules:

| Type | Protocol | Port Range | Source | Description |
|------|----------|------------|--------|-------------|
| SSH | TCP | 22 | Your IP | SSH access |
| Custom TCP | TCP | 8082 | 0.0.0.0/0 | Web Interface |
| Custom TCP | TCP | 30000-30100 | 0.0.0.0/0 | Kubernetes NodePorts |

```bash
# If using AWS CLI to update security group:
aws ec2 authorize-security-group-ingress \
    --group-id <your-sg-id> \
    --protocol tcp \
    --port 8082 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-id <your-sg-id> \
    --protocol tcp \
    --port 30000-30100 \
    --cidr 0.0.0.0/0
```

## Step 1: System Updates and Basic Tools

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y curl wget git build-essential software-properties-common \
    apt-transport-https ca-certificates gnupg lsb-release net-tools tmux \
    vim nano htop jq unzip
```

## Step 2: Install Python 3.12 (Latest Stable)

```bash
# Add deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.12
sudo apt install -y python3.12 python3.12-dev python3.12-venv python3-pip

# Verify installation
python3.12 --version
# Should show: Python 3.12.x
```

## Step 3: Install Docker (Latest)

```bash
# Remove old versions
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
    sudo apt remove $pkg 2>/dev/null || true
done

# Add Docker's official GPG key
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version
# Should show: Docker version 25.x.x or 26.x.x
```

## Step 4: Install kubectl (Latest)

```bash
# Download latest kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Install
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify
kubectl version --client
# Should show: v1.30.x or v1.31.x
```

## Step 5: Install Kind 0.30.0 (Latest)

```bash
# For AMD64 (most EC2 instances)
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.30.0/kind-linux-amd64

# Install
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Verify
kind version
# Should show: kind v0.23.0
```

## Step 6: Install Helm 3 (Latest)

```bash
# Install Helm using the official script
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify installation
helm version
# Should show: version.BuildInfo{Version:"v3.15.x"...}
```

## Step 7: Create Project Directory

```bash
# Create and enter project directory
mkdir -p ~/mcp-devops-agent
cd ~/mcp-devops-agent
```

## Step 8: Create Python Virtual Environment

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Verify Python version in venv
python --version
# Should show: Python 3.12.x
```

## Step 9: Install Python Dependencies

```bash
# Create requirements.txt (copy the content from the artifact)
cat > requirements.txt << 'EOF'
openai==1.52.0
anthropic==0.39.0
kubernetes==30.1.0
pyyaml==6.0.2
requests==2.32.3
urllib3==2.2.3
prometheus-client==0.21.0
pydantic==2.9.2
pydantic-settings==2.6.1
typing-extensions==4.12.2
python-dotenv==1.0.1
aiofiles==24.1.0
aiohttp==3.10.10
httpx==0.27.2
flask==3.0.3
flask-cors==5.0.0
flask-socketio==5.3.7
python-socketio==5.11.4
eventlet==0.36.1
werkzeug==3.0.4
pytest==8.3.3
pytest-asyncio==0.24.0
black==24.10.0
flake8==7.1.1
mypy==1.11.2
rich==13.9.4
colorama==0.4.6
structlog==24.4.0
loguru==0.7.2
jsonschema==4.23.0
orjson==3.10.7
click==8.1.7
watchdog==5.0.3
python-dateutil==2.9.0.post0
tenacity==9.0.0
cryptography==43.0.1
certifi==2024.8.30
psutil==6.0.0
docker==7.1.0
EOF

# Install dependencies
pip install -r requirements.txt

# Verify key packages
pip list | grep -E "openai|flask|kubernetes"
```

## Step 10: Create Kind Cluster Configuration

```bash
cat > kind-config.yaml << 'EOF'
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: mcp-cluster
nodes:
  - role: control-plane
    image: kindest/node:v1.30.0@sha256:047357ac0cfea04663786a612ba1eaba9702bef25227a794b52890dd8bcd692e
    extraPortMappings:
      # NodePort for services
      - containerPort: 30000
        hostPort: 30000
        protocol: TCP
        listenAddress: "0.0.0.0"
      - containerPort: 30001
        hostPort: 30001
        protocol: TCP
        listenAddress: "0.0.0.0"
      # Grafana
      - containerPort: 30030
        hostPort: 30030
        protocol: TCP
        listenAddress: "0.0.0.0"
      # Web UI
      - containerPort: 30080
        hostPort: 30080
        protocol: TCP
        listenAddress: "0.0.0.0"
      # Prometheus
      - containerPort: 30090
        hostPort: 30090
        protocol: TCP
        listenAddress: "0.0.0.0"
      # Alertmanager
      - containerPort: 30093
        hostPort: 30093
        protocol: TCP
        listenAddress: "0.0.0.0"
networking:
  apiServerAddress: "127.0.0.1"
  apiServerPort: 6443
  podSubnet: "10.244.0.0/16"
  serviceSubnet: "10.96.0.0/12"
EOF
```

## Step 11: Create Kubernetes Cluster

```bash
# Create cluster
kind create cluster --config kind-config.yaml --wait 120s

# Verify cluster
kubectl cluster-info
kubectl get nodes
# Should show 1 node in Ready state
```
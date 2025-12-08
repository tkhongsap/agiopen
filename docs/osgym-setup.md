# OSGym Infrastructure Setup Guide

OSGym is the open-source distributed data engine used to train and run Lux models. This guide covers setting up the OSGym infrastructure for development and benchmarking.

## Table of Contents

1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running Workers](#running-workers)
6. [Local Benchmarking](#local-benchmarking)
7. [Architecture](#architecture)
8. [Troubleshooting](#troubleshooting)

---

## Overview

OSGym provides a scalable infrastructure for running computer-use agents in virtualized environments. Key features:

| Feature | Specification |
|---------|---------------|
| **Scale** | 1,000+ OS replicas in parallel |
| **Speed** | 1,420 multi-turn trajectories per minute |
| **Cost** | $0.20-0.30 USD per day per OS replica |
| **Latency** | Sub-second action execution |

### Key Components

- **State Managers**: Individual per-replica VM management
- **Orchestration Layer**: Hardware-aware VM grouping
- **Data Server**: High-level Python interface
- **API Gateway**: REST endpoints for external access

---

## System Requirements

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 4 cores | 16+ cores |
| **RAM** | 8 GB | 32+ GB |
| **Storage** | 50 GB SSD | 200+ GB NVMe |
| **GPU** | Optional | NVIDIA (for model inference) |

### Software Requirements

- **OS**: Ubuntu 20.04+ or similar Linux distribution
- **Python**: 3.10 or higher
- **Virtualization**: KVM/QEMU support
- **Container Runtime**: Docker (optional, for containerized deployment)

---

## Installation

### Step 1: Create Environment

```bash
# Create conda environment
conda create -n osgym python=3.10
conda activate osgym

# Or use venv
python -m venv osgym-env
source osgym-env/bin/activate
```

### Step 2: Install System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    libgl1 \
    libglx-mesa0 \
    linux-headers-$(uname -r) \
    python3-dev \
    build-essential \
    qemu-kvm \
    libvirt-daemon-system \
    libvirt-clients \
    bridge-utils \
    virtinst

# Verify KVM support
sudo kvm-ok
```

### Step 3: Install Python Dependencies

```bash
# Clone OSGym repository
git clone https://github.com/agiopen-org/osgym.git
cd osgym

# Install requirements
pip install -r requirements.txt

# Or install from PyPI
pip install osgym
```

### Step 4: Configure Permissions

```bash
# Add user to KVM and libvirt groups
sudo usermod -aG kvm $USER
sudo usermod -aG libvirt $USER

# Apply group changes (or log out and back in)
newgrp kvm
newgrp libvirt
```

---

## Configuration

### Environment Variables

Create a `.env` file in the OSGym directory:

```bash
# .env
OSGYM_API_PORT=20000
OSGYM_VM_COUNT=4
OSGYM_VM_MEMORY=4096
OSGYM_VM_CPUS=2
OSGYM_DISPLAY_RESOLUTION=1920x1080
OSGYM_LOG_LEVEL=INFO

# Optional: For cloud deployment
OSGYM_CLOUD_PROVIDER=aws
OSGYM_REGION=us-west-2
```

### VM Configuration

Configure VM settings in `config/vm_config.yaml`:

```yaml
# config/vm_config.yaml
vm_defaults:
  memory_mb: 4096
  vcpus: 2
  disk_size_gb: 20
  display:
    resolution: "1920x1080"
    depth: 24

network:
  type: "bridge"
  bridge_name: "virbr0"

storage:
  pool_path: "/var/lib/osgym/images"
  base_image: "ubuntu-22.04-desktop.qcow2"

applications:
  - name: "chrome"
    install_command: "apt-get install -y google-chrome-stable"
  - name: "libreoffice"
    install_command: "apt-get install -y libreoffice"
  - name: "vscode"
    install_command: "snap install code --classic"
```

### Task Configuration

Define tasks in `config/tasks.yaml`:

```yaml
# config/tasks.yaml
tasks:
  - id: "web_search_001"
    type: "web_navigation"
    instruction: "Search for 'artificial intelligence' on Google"
    timeout: 120
    success_criteria:
      - type: "url_contains"
        value: "google.com/search"
      - type: "element_present"
        selector: "#search"

  - id: "form_fill_001"
    type: "form_automation"
    instruction: "Fill out the contact form with test data"
    timeout: 180
    form_data:
      name: "Test User"
      email: "test@example.com"
      message: "This is a test message"
```

---

## Running Workers

### Start Workers (Development)

```bash
# Start with default settings (4 VMs)
./start_workers.sh

# Start with custom VM count
./start_workers.sh --vm-count 8

# Start with verbose logging
./start_workers.sh --log-level DEBUG
```

### Start Workers (Local Benchmarking)

```bash
# Local mode with reduced resources
./start_workers.sh --local

# Local mode with specific configuration
./start_workers.sh --local --vm-count 2 --memory 2048
```

### Start Workers (Production)

```bash
# Production mode with full resources
./start_workers.sh --production

# With custom configuration file
./start_workers.sh --config config/production.yaml
```

### Using Docker

```bash
# Build Docker image
docker build -t osgym:latest .

# Run container with KVM access
docker run -d \
    --name osgym \
    --privileged \
    --device /dev/kvm \
    -p 20000:20000 \
    -v /var/lib/osgym:/var/lib/osgym \
    osgym:latest

# View logs
docker logs -f osgym
```

---

## Local Benchmarking

### Running Benchmarks

```bash
# Run standard benchmark suite
python -m osgym.benchmark --suite standard

# Run specific benchmark
python -m osgym.benchmark --task web_navigation

# Run with custom configuration
python -m osgym.benchmark --config benchmarks/custom.yaml
```

### Benchmark Configuration

```yaml
# benchmarks/custom.yaml
benchmark:
  name: "Custom Web Navigation"
  tasks:
    - "web_search_001"
    - "form_fill_001"

  settings:
    max_steps: 50
    timeout_per_step: 30
    retry_on_failure: true

  metrics:
    - success_rate
    - average_steps
    - time_to_complete
    - error_rate
```

### Viewing Results

```bash
# Generate benchmark report
python -m osgym.benchmark.report --output report.html

# Export metrics to JSON
python -m osgym.benchmark.export --format json --output metrics.json
```

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         OSGym System                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   Client     │    │   Client     │    │   Client     │       │
│  │  (Python)    │    │   (REST)     │    │   (CLI)      │       │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘       │
│         │                   │                   │                │
│         └───────────────────┼───────────────────┘                │
│                             │                                    │
│                   ┌─────────▼─────────┐                         │
│                   │   API Gateway     │                         │
│                   │   (Port 20000)    │                         │
│                   └─────────┬─────────┘                         │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │                │
│  ┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐         │
│  │   Worker    │    │   Worker    │    │   Worker    │         │
│  │   Group 1   │    │   Group 2   │    │   Group N   │         │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘         │
│         │                   │                   │                │
│    ┌────┴────┐         ┌────┴────┐         ┌────┴────┐          │
│    │ VM │ VM │         │ VM │ VM │         │ VM │ VM │          │
│    └────┴────┘         └────┴────┘         └────┴────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Client Request**: Action submitted to API Gateway
2. **Orchestration**: Request routed to appropriate worker group
3. **VM Execution**: Action executed in virtualized environment
4. **Screenshot Capture**: Current state captured and returned
5. **Response**: Result (success/failure + screenshot) returned to client

---

## Troubleshooting

### Common Issues

#### KVM Not Available

```bash
# Check if KVM is enabled
lsmod | grep kvm

# If not loaded, load the modules
sudo modprobe kvm
sudo modprobe kvm_intel  # or kvm_amd for AMD CPUs

# Verify
sudo kvm-ok
```

#### Permission Denied

```bash
# Check group membership
groups $USER

# Add to required groups
sudo usermod -aG kvm,libvirt $USER

# Restart session or use newgrp
newgrp kvm
```

#### Port Already in Use

```bash
# Check what's using port 20000
sudo lsof -i :20000

# Kill the process or use a different port
./start_workers.sh --port 20001
```

#### VM Start Failure

```bash
# Check libvirt status
sudo systemctl status libvirtd

# Restart libvirt
sudo systemctl restart libvirtd

# Check VM logs
sudo virsh list --all
sudo virsh console <vm-name>
```

#### Out of Memory

```bash
# Check available memory
free -h

# Reduce VM count or memory per VM
./start_workers.sh --vm-count 2 --memory 2048
```

### Logs and Debugging

```bash
# View OSGym logs
tail -f logs/osgym.log

# View specific worker logs
tail -f logs/worker-0.log

# Enable debug mode
export OSGYM_LOG_LEVEL=DEBUG
./start_workers.sh
```

### Health Check

```bash
# Check API health
curl http://localhost:20000/health

# Check VM status
curl http://localhost:20000/status

# List active VMs
curl http://localhost:20000/vms
```

---

## External Resources

| Resource | URL |
|----------|-----|
| OSGym Paper | https://arxiv.org/abs/2511.11672 |
| GitHub Repository | https://github.com/agiopen-org/osgym |
| HuggingFace Dataset | https://huggingface.co/datasets/agiopen-org/osgym |
| Discord Community | https://discord.gg/PVAtX8PzxK |

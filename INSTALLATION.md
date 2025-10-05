# Installation Guide

Complete installation instructions for Performia, including both Docker and manual setup options.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Option 1: Quick Start (Manual)](#option-1-quick-start-manual)
- [Option 2: Docker Setup (Recommended for Production)](#option-2-docker-setup-recommended-for-production)
- [Docling Installation (RAG Knowledge Base)](#docling-installation-rag-knowledge-base)
- [Database Configuration](#database-configuration)
- [Environment Variables](#environment-variables)
- [Post-Installation Checklist](#post-installation-checklist)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Python 3.11+**
   ```bash
   # Check Python version
   python --version  # or python3 --version

   # Install Python (macOS)
   brew install python@3.11

   # Install Python (Ubuntu/Debian)
   sudo apt update
   sudo apt install python3.11 python3.11-venv python3-pip

   # Install Python (Windows)
   # Download from https://www.python.org/downloads/
   ```

2. **Node.js 18+ and npm**
   ```bash
   # Check Node version
   node --version
   npm --version

   # Install Node (macOS)
   brew install node@18

   # Install Node (Ubuntu/Debian)
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt install -y nodejs

   # Install Node (Windows)
   # Download from https://nodejs.org/
   ```

3. **Git**
   ```bash
   # Check Git version
   git --version

   # Install Git (macOS)
   brew install git

   # Install Git (Ubuntu/Debian)
   sudo apt install git

   # Install Git (Windows)
   # Download from https://git-scm.com/
   ```

4. **Docker** (Optional, for containerized deployment)
   ```bash
   # Install Docker Desktop
   # macOS/Windows: https://www.docker.com/products/docker-desktop/

   # Install Docker (Ubuntu/Debian)
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh

   # Verify Docker installation
   docker --version
   docker-compose --version
   ```

### System Requirements

- **RAM**: 8GB minimum, 16GB recommended (for Whisper and Demucs models)
- **Storage**: 10GB minimum (for models and dependencies)
- **CPU**: Multi-core processor recommended for audio processing
- **GPU**: Optional, CUDA-compatible GPU accelerates audio processing

---

## Option 1: Quick Start (Manual)

Best for development and testing on local machines.

### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/PerformanceSuite/Performia.git
cd Performia
```

### Step 2: Install Backend Dependencies

```bash
# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt
```

**Expected installation time**: 5-10 minutes

**Note**: Installing `docling` adds ~2-3GB of dependencies. See [Docling Installation](#docling-installation-rag-knowledge-base) for details.

### Step 3: Install Frontend Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install npm packages
npm install

# Return to root directory
cd ..
```

**Expected installation time**: 2-3 minutes

### Step 4: Configure Environment

```bash
# Copy environment template
cp .env.template .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

Required environment variables:
```bash
# AI Models
ANTHROPIC_API_KEY=your-anthropic-api-key
OPENAI_API_KEY=your-openai-api-key

# GitHub Integration (optional)
GITHUB_TOKEN=your-github-personal-access-token

# Database (SQLite by default)
DATABASE_URL=sqlite:///performia.db

# MCP Memory Storage (optional)
MCP_MEMORY_DIR=/path/to/.mcp-memory
```

### Step 5: Initialize Database

```bash
# Create necessary directories
mkdir -p uploads output

# Initialize job database (SQLite)
# Database is auto-created on first run
python backend/src/services/api/main.py &
sleep 2
pkill -f "python backend/src/services/api/main.py"
```

### Step 6: Start Services

**Terminal 1 - Backend API:**
```bash
# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start backend server
python backend/src/services/api/main.py
```

Backend runs on: `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
# Navigate to frontend
cd frontend

# Start development server
npm run dev
```

Frontend runs on: `http://localhost:5001`

### Step 7: Verify Installation

1. Open browser to `http://localhost:5001`
2. You should see the Performia interface with demo song "Yesterday"
3. Click Play to test real-time syllable highlighting
4. Check backend logs for any errors

---

## Option 2: Docker Setup (Recommended for Production)

Best for production deployments and consistent environments.

### Step 1: Install Docker

Follow Docker installation instructions in [Prerequisites](#prerequisites).

### Step 2: Clone Repository

```bash
git clone https://github.com/PerformanceSuite/Performia.git
cd Performia
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.template .env

# Edit .env with your configuration
nano .env
```

### Step 4: Build and Run with Docker Compose

```bash
# Build Docker images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

Services will be available at:
- **Frontend**: `http://localhost:5001`
- **Backend API**: `http://localhost:8000`
- **Backend API Docs**: `http://localhost:8000/docs`

### Step 5: Verify Installation

```bash
# Check running containers
docker-compose ps

# Test backend health
curl http://localhost:8000/health

# Test frontend
curl http://localhost:5001
```

### Managing Docker Services

```bash
# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild after code changes
docker-compose up -d --build
```

---

## Docling Installation (RAG Knowledge Base)

Docling is used for the RAG-based knowledge system that helps AI agents avoid repeating mistakes.

### What is Docling?

Docling processes documentation into vector embeddings for semantic search. It helps Claude agents:
- Remember past mistakes and solutions
- Access project-specific knowledge
- Improve code generation quality

### Installation Size Warning

**Docling adds approximately 2-3GB of dependencies**, including:
- Transformers models
- Sentence transformers
- Accelerate
- Huggingface Hub
- PyTorch models

### Installing Docling

Docling is included in `requirements.txt`. If you want to install it separately:

```bash
# Activate virtual environment
source venv/bin/activate

# Install docling with all dependencies
pip install docling==2.55.1

# Install additional RAG dependencies
pip install chromadb sentence-transformers
```

### Verifying Docling Installation

Use the provided verification script:

```bash
# Run Docling check script
python scripts/check_docling.py
```

Expected output:
```
Checking Docling installation...
✅ Docling installed
✅ ChromaDB installed
✅ Sentence Transformers installed

✅ All RAG dependencies ready!
```

### Building Knowledge Base

```bash
# Ingest knowledge base documents
python knowledge_rag.py

# Test knowledge base
python verify_knowledge.py
```

The knowledge base automatically rebuilds when source files change.

### Skipping Docling (Optional)

If you don't need the knowledge base RAG system:

```bash
# Create requirements without docling
grep -v "docling" requirements.txt > requirements.minimal.txt

# Install minimal dependencies
pip install -r requirements.minimal.txt
```

**Note**: Some agent features may be limited without the knowledge base.

---

## Database Configuration

Performia supports SQLite (default) and PostgreSQL for job storage.

### SQLite (Default)

Best for development and single-user setups.

```bash
# Set in .env
DATABASE_URL=sqlite:///performia.db

# Database is auto-created on first run
# No additional setup required
```

Pros:
- Zero configuration
- File-based, portable
- Perfect for development

Cons:
- Not suitable for high concurrency
- Limited to single server

### PostgreSQL (Production)

Best for production deployments with multiple users.

#### Install PostgreSQL

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### Create Database

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE performia;
CREATE USER performia_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE performia TO performia_user;
\q
```

#### Configure Environment

```bash
# Set in .env
DATABASE_URL=postgresql://performia_user:secure_password@localhost:5432/performia
```

#### Initialize Schema

```bash
# Schema is auto-created by SQLAlchemy on first run
python backend/src/services/api/main.py
```

---

## Environment Variables

Complete reference for `.env` configuration.

### Required Variables

```bash
# AI Model APIs (required for audio analysis)
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
```

### Optional Variables

```bash
# GitHub Integration
GITHUB_TOKEN=ghp_xxxxx

# Database
DATABASE_URL=sqlite:///performia.db  # or PostgreSQL URL

# Slack Integration
SLACK_TOKEN=xoxb-xxxxx

# MCP Memory
MCP_MEMORY_DIR=/Users/username/.mcp-memory

# Custom Paths
UPLOAD_DIR=/path/to/uploads
OUTPUT_DIR=/path/to/output
```

### Generating Secure Secrets

Use the provided script to generate secure random secrets:

```bash
python scripts/generate_secrets.py
```

Output:
```bash
# Add these to your .env file
SECRET_KEY=random_secure_key_here
DB_PASSWORD=random_password_here
```

### Environment File Security

**Important**: Never commit `.env` to version control!

```bash
# Verify .env is in .gitignore
grep ".env" .gitignore

# If not present, add it
echo ".env" >> .gitignore
```

---

## Post-Installation Checklist

After installation, verify everything is working:

### 1. Backend Health Check

```bash
# Check backend is running
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "jobs_count": 0, "database": "performia.db"}
```

### 2. Frontend Accessibility

```bash
# Open browser to frontend
open http://localhost:5001  # macOS
xdg-open http://localhost:5001  # Linux
start http://localhost:5001  # Windows
```

### 3. Test Audio Upload

1. Navigate to `http://localhost:5001`
2. Click "Upload Song" or drag/drop an audio file
3. Wait for processing (~30 seconds)
4. Verify Song Map is displayed

### 4. Check Dependencies

```bash
# Verify Python packages
pip list | grep -E "fastapi|openai-whisper|librosa|demucs"

# Verify Node packages
cd frontend && npm list react vite typescript
```

### 5. Run Tests

```bash
# Backend tests
pytest backend/tests/

# Frontend tests
cd frontend && npm test
```

### 6. Verify Knowledge Base (Optional)

```bash
# Check Docling installation
python scripts/check_docling.py

# Verify knowledge base
python verify_knowledge.py
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Python Version Mismatch

**Problem**: `ERROR: Python 3.11 or higher is required`

**Solution**:
```bash
# Check Python version
python --version

# Use python3 explicitly
python3 --version

# Create venv with specific version
python3.11 -m venv venv
```

#### 2. Port Already in Use

**Problem**: `Address already in use: 8000` or `5001`

**Solution**:
```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use different port
# Backend: python backend/src/services/api/main.py --port 8001
# Frontend: vite --port 5002
```

#### 3. Missing Dependencies

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

#### 4. Whisper Model Download Fails

**Problem**: `Failed to download Whisper model`

**Solution**:
```bash
# Pre-download Whisper model
python -c "import whisper; whisper.load_model('base')"

# Or use smaller model
python -c "import whisper; whisper.load_model('tiny')"

# Check internet connection and retry
```

#### 5. Frontend Build Errors

**Problem**: `npm ERR! code ELIFECYCLE`

**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Try with different Node version (use nvm)
nvm install 18
nvm use 18
npm install
```

#### 6. Database Connection Errors

**Problem**: `Could not connect to database`

**Solution**:

For SQLite:
```bash
# Ensure database directory exists
mkdir -p data

# Check file permissions
chmod 644 performia.db

# Remove corrupted database
rm performia.db
# Restart backend to recreate
```

For PostgreSQL:
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list  # macOS

# Test connection
psql -U performia_user -d performia -h localhost

# Check credentials in .env
```

#### 7. Docling Installation Issues

**Problem**: `Failed building wheel for docling`

**Solution**:
```bash
# Install build dependencies (Ubuntu/Debian)
sudo apt install python3-dev build-essential

# Install build dependencies (macOS)
xcode-select --install

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Retry installation
pip install docling==2.55.1
```

#### 8. CUDA/GPU Issues

**Problem**: `CUDA not available` or slow performance

**Solution**:
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Install CUDA-enabled PyTorch (if you have NVIDIA GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Or use CPU-only (slower but works everywhere)
pip install torch torchvision torchaudio
```

#### 9. Audio File Format Not Supported

**Problem**: `Unsupported audio format: .m4a`

**Solution**:
```bash
# Install ffmpeg for format conversion
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html

# Convert audio file
ffmpeg -i song.m4a song.wav
```

#### 10. Memory Errors During Processing

**Problem**: `MemoryError: Unable to allocate array`

**Solution**:
```bash
# Use smaller Whisper model
# Edit backend code to use 'tiny' or 'small' instead of 'base'

# Process audio in chunks
# Increase system swap space

# Close other applications to free memory

# For Demucs, use lighter model
# Edit demucs config to use 'htdemucs' instead of 'htdemucs_ft'
```

### Getting Help

If you encounter issues not covered here:

1. **Check logs**:
   ```bash
   # Backend logs
   tail -f backend.log

   # Frontend logs (in browser console)
   # Open DevTools (F12) → Console tab
   ```

2. **Search existing issues**:
   - [GitHub Issues](https://github.com/PerformanceSuite/Performia/issues)

3. **Create new issue**:
   - Include error message
   - Include system info: OS, Python version, Node version
   - Include relevant logs
   - Include steps to reproduce

4. **Community support**:
   - [GitHub Discussions](https://github.com/PerformanceSuite/Performia/discussions)

---

## Next Steps

After successful installation:

1. Read the [Usage Guide](./USAGE.md) to learn how to use Performia
2. Review the [Architecture](./ARCHITECTURE.md) to understand the system
3. Check the [API Reference](./API.md) for integration details
4. See [Contributing Guide](./CONTRIBUTING.md) if you want to contribute

---

*For questions or issues, please see the [Troubleshooting](#troubleshooting) section or open an issue on GitHub.*

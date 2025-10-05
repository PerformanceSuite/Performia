# Command Center - Quick Start Guide

**Production-ready R&D Command Center built in parallel using git worktrees!**

## 🎉 What Was Built

4 specialized agents worked simultaneously to create a complete full-stack application:

- **Backend Agent**: FastAPI + SQLAlchemy + Alembic (2,858 lines)
- **Frontend Agent**: React 19 + TypeScript + Vite (1,547 lines)
- **Docker Agent**: Production Docker Compose setup (982 lines)
- **Docs Agent**: Comprehensive documentation (4,830+ lines)

**Total**: ~10,000 lines of production code in one parallel session!

## 🚀 Get Started in 3 Commands

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env with your secrets (use scripts/generate_secrets.py)

# 2. Start everything
./scripts/setup.sh

# 3. Access the application
open http://localhost:3000
```

## 📊 What You Get

### Dashboard
- Multi-repository tracking
- Technology radar with 60+ technologies (auto-imported)
- Real-time GitHub commit sync
- Research progress tracking

### Technology Radar
- Domain grouping (Core Engine, Immersive, Interactive)
- Status lifecycle (Research → Prototype → Beta → Production)
- Relevance scoring (1-10)
- Rich metadata (latency, platform, vendor)

### Research Hub
- Document upload (PDF, MD, HTML, DOCX)
- Docling processing → ChromaDB indexing
- AI-powered analysis with grounded summaries
- Notes and recommendations

### Knowledge Base
- Semantic search across all research
- Category filtering
- Markdown rendering
- Export to PDF/Markdown

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Frontend (React 19)                 │
│         http://localhost:3000                    │
│  ┌──────────┬──────────┬──────────┬──────────┐  │
│  │Dashboard │  Radar   │ Research │Knowledge │  │
│  └──────────┴──────────┴──────────┴──────────┘  │
└─────────────────────────────────────────────────┘
                     ↓ HTTP/REST
┌─────────────────────────────────────────────────┐
│           Backend (FastAPI + Python)             │
│         http://localhost:8000                    │
│  ┌──────────────────┬──────────────────┐         │
│  │ GitHub Service   │  RAG Service     │         │
│  │ (Multi-repo)     │  (Docling)       │         │
│  └──────────────────┴──────────────────┘         │
└─────────────────────────────────────────────────┘
        ↓                           ↓
┌───────────────┐          ┌───────────────┐
│  PostgreSQL   │          │   ChromaDB    │
│   (Data)      │          │  (Vectors)    │
└───────────────┘          └───────────────┘
```

## 📁 Project Structure

```
commandcenter/
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── models/             # SQLAlchemy (4 models)
│   │   ├── schemas/            # Pydantic validation
│   │   ├── routers/            # API endpoints
│   │   └── services/           # Business logic
│   ├── alembic/                # Database migrations
│   └── requirements.txt
├── frontend/                    # React + TypeScript
│   ├── src/
│   │   ├── components/         # UI components
│   │   ├── hooks/              # Custom hooks
│   │   ├── services/           # API client
│   │   └── types/              # TypeScript types
│   └── package.json
├── scripts/                     # Automation
│   ├── setup.sh               # Production setup
│   ├── dev.sh                 # Development mode
│   ├── check_docling.py       # Verify RAG setup
│   └── generate_secrets.py    # Generate secrets
├── docker-compose.yml          # Production
├── docker-compose.dev.yml      # Development
├── Makefile                    # Convenience commands
└── DOCKER_README.md            # Complete docs
```

## 🛠️ Development Workflow

### Start Backend (Manual)
```bash
cd commandcenter/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Start Frontend (Manual)
```bash
cd commandcenter/frontend
npm install
npm run dev
```

### Start Everything (Docker)
```bash
# Development mode (hot reload)
./scripts/dev.sh

# Production mode
./scripts/setup.sh

# Using Makefile
make dev     # Development
make up      # Production
make logs    # View logs
make down    # Stop all services
```

## 📚 Documentation

- **DOCKER_README.md** - Complete Docker setup guide
- **backend/README.md** - Backend API documentation
- **frontend/SETUP.md** - Frontend architecture
- **API docs** - http://localhost:8000/docs (Swagger UI)

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Database
DATABASE_URL=postgresql://commandcenter:changeme@localhost:5432/commandcenter

# Security
SECRET_KEY=<generate with scripts/generate_secrets.py>

# RAG
RAG_STORAGE_PATH=./rag_storage
CHROMADB_PATH=./rag_storage/chromadb

# GitHub
GITHUB_API_RATE_LIMIT=5000
```

Generate secure secrets:
```bash
python scripts/generate_secrets.py
```

## 🎯 Next Steps

1. **Add Your First Repository**
   - Go to Settings → Repository Management
   - Add GitHub token
   - Select repository

2. **Import Research Data**
   - Technologies auto-populate from research reports
   - Or manually add technologies

3. **Start Researching**
   - Select technology from Radar
   - Upload research documents
   - Get AI analysis
   - Save to knowledge base

4. **Search Knowledge**
   - Use semantic search
   - Filter by category
   - Export findings

## 🐛 Troubleshooting

**Docker issues:**
```bash
make clean    # Remove all containers and volumes
make up       # Start fresh
```

**Docling not working:**
```bash
python scripts/check_docling.py
```

**Database migrations:**
```bash
cd backend
alembic upgrade head
```

## 🤝 Contributing

See CONTRIBUTING.md for development guidelines.

## 📄 License

See LICENSE file.

---

**Built with parallel development using git worktrees!**

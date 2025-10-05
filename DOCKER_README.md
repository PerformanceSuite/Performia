# Command Center - Docker Setup Guide

Complete Docker setup for one-command deployment of the Command Center system.

## 🚀 Quick Start

### Production Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd <repo-directory>

# 2. Run setup script
./scripts/setup.sh

# Or use Make
make setup
```

That's it! The system will be running at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs
- **Database**: localhost:5432
- **Redis**: localhost:6379

### Development Setup

```bash
# Start with hot reload
./scripts/dev.sh

# Or use Make
make dev
```

## 📋 Prerequisites

- Docker 20.10+
- Docker Compose 2.0+ (or docker-compose 1.29+)
- 8GB+ RAM recommended
- 10GB+ disk space for images and volumes

## 🏗️ Architecture

### Services

1. **PostgreSQL** (postgres:16-alpine)
   - Database for application data
   - Persistent volume for data storage
   - Health checks enabled

2. **Redis** (redis:7-alpine)
   - Caching and session storage
   - Persistent volume for data
   - Health checks enabled

3. **Backend** (Python 3.11)
   - FastAPI application
   - Docling for document processing (~2-3GB)
   - Audio processing libraries (librosa, torch)
   - RAG knowledge base with ChromaDB

4. **Frontend** (Node 20 + Nginx)
   - React 19 + TypeScript
   - Vite build system
   - Nginx for production serving
   - Multi-stage build for optimization

## 🛠️ Configuration

### Environment Variables

Copy `.env.template` to `.env` and configure:

```bash
# Required
DB_PASSWORD=your-secure-password
SECRET_KEY=your-secret-key  # Generate: openssl rand -hex 32
ANTHROPIC_API_KEY=your-key
OPENAI_API_KEY=your-key

# Optional
GITHUB_TOKEN=your-token
SLACK_TOKEN=your-token
```

### Docker Compose Files

- `docker-compose.yml` - Production configuration
- `docker-compose.dev.yml` - Development with hot reload

## 📝 Common Commands

### Using Make (Recommended)

```bash
make help              # Show all available commands
make up                # Start production services
make down              # Stop all services
make restart           # Restart all services
make logs              # View logs
make shell-backend     # Shell into backend container
make shell-frontend    # Shell into frontend container
make shell-db          # PostgreSQL shell
make clean             # Remove all containers and volumes (⚠️  deletes data!)
make dev               # Start development mode
make build             # Build all images
make build-no-cache    # Build without cache
make ps                # Show service status
make health            # Check service health
```

### Using Docker Compose Directly

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild and start
docker compose up -d --build

# Execute commands in containers
docker compose exec backend bash
docker compose exec frontend sh
docker compose exec postgres psql -U commandcenter -d commandcenter
```

## 🔍 Troubleshooting

### Port Conflicts

If ports 3000, 8000, 5432, or 6379 are already in use:

```yaml
# Edit docker-compose.yml and change port mappings:
ports:
  - "3001:3000"  # Frontend
  - "8001:8000"  # Backend
  - "5433:5432"  # PostgreSQL
  - "6380:6379"  # Redis
```

### Build Failures

```bash
# Clear Docker cache and rebuild
make build-no-cache

# Or manually
docker compose build --no-cache
```

### Database Connection Issues

```bash
# Check PostgreSQL health
docker compose exec postgres pg_isready -U commandcenter

# View PostgreSQL logs
docker compose logs postgres

# Reset database (⚠️  deletes all data!)
docker compose down -v
docker compose up -d
```

### Memory Issues

The backend requires significant RAM for Docling and ML models:

```bash
# Check Docker resource limits
docker stats

# Increase Docker Desktop memory allocation to 8GB+
```

## 🧹 Cleanup

```bash
# Stop and remove containers (keeps volumes)
make down

# Remove everything including data (⚠️  DANGEROUS!)
make clean

# Clean up Docker system
make prune
```

## 🏭 Production Deployment

### Security Checklist

- [ ] Change `DB_PASSWORD` from default
- [ ] Generate secure `SECRET_KEY`
- [ ] Configure real API keys
- [ ] Enable HTTPS (use reverse proxy)
- [ ] Set `DEBUG=false`
- [ ] Review CORS settings
- [ ] Enable authentication
- [ ] Set up backups for volumes

### Recommended Setup

1. Use a reverse proxy (Nginx/Traefik) for HTTPS
2. Set up automated backups:
   ```bash
   docker run --rm -v commandcenter_postgres_data:/data -v $(pwd)/backups:/backup \
     alpine tar czf /backup/postgres-$(date +%Y%m%d).tar.gz /data
   ```
3. Monitor with Docker stats or tools like Prometheus
4. Use Docker secrets for sensitive data

## 📊 Volume Management

Persistent data is stored in Docker volumes:

```bash
# List volumes
docker volume ls | grep commandcenter

# Backup volume
docker run --rm -v commandcenter_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres_backup.tar.gz /data

# Restore volume
docker run --rm -v commandcenter_postgres_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/postgres_backup.tar.gz -C /
```

## 🔧 Development Mode

Development mode features:
- Hot reload for both frontend and backend
- Source code mounted as volumes
- Debug mode enabled
- Separate dev database
- Live code changes without rebuilds

```bash
# Start dev mode
make dev

# Or
./scripts/dev.sh
```

## 📈 Performance Optimization

### Backend
- Docling installation adds ~2-3GB to image
- Consider using pre-built image for faster startups
- Multi-stage builds keep production image smaller

### Frontend
- Production build uses multi-stage Dockerfile
- Nginx serves static files efficiently
- Gzip compression enabled
- Static asset caching configured

## 🐛 Debug Mode

```bash
# Run backend with debug logs
docker compose exec backend python -m pdb api/server.py

# View detailed logs
docker compose logs -f --tail=100 backend
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

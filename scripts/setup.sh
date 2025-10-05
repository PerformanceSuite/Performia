#!/bin/bash
# Production setup script for Command Center
set -e

echo "🚀 Setting up Command Center (Production)..."

# Check prerequisites
if ! command -v docker >/dev/null 2>&1; then
    echo "❌ Docker is required but not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose >/dev/null 2>&1 && ! docker compose version >/dev/null 2>&1; then
    echo "❌ Docker Compose is required but not installed. Please install Docker Compose first."
    exit 1
fi

# Determine docker compose command
if docker compose version >/dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Copy env if not exists
if [ ! -f .env ]; then
    if [ -f .env.template ]; then
        cp .env.template .env
        echo "📝 Created .env from template - please configure it with your actual values"
        echo ""
        echo "⚠️  IMPORTANT: Edit .env and set the following:"
        echo "   - DB_PASSWORD (default: changeme)"
        echo "   - SECRET_KEY (generate a secure random key)"
        echo "   - ANTHROPIC_API_KEY (your API key)"
        echo "   - OPENAI_API_KEY (your API key)"
        echo "   - GITHUB_TOKEN (optional, for GitHub integration)"
        echo ""
        read -p "Press Enter to continue after editing .env, or Ctrl+C to exit..."
    else
        echo "❌ No .env.template found. Please create .env manually."
        exit 1
    fi
fi

# Pull images
echo "📥 Pulling Docker images..."
$DOCKER_COMPOSE pull

# Build services
echo "🔨 Building services..."
$DOCKER_COMPOSE build

# Start services
echo "🚀 Starting services..."
$DOCKER_COMPOSE up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 5

# Check service status
echo ""
echo "📊 Service Status:"
$DOCKER_COMPOSE ps

echo ""
echo "✅ Command Center started successfully!"
echo ""
echo "📍 Access Points:"
echo "   🌐 Frontend:    http://localhost:3000"
echo "   🔧 Backend API: http://localhost:8000/docs"
echo "   💾 PostgreSQL:  localhost:5432"
echo "   🔴 Redis:       localhost:6379"
echo ""
echo "📝 Useful Commands:"
echo "   View logs:        $DOCKER_COMPOSE logs -f"
echo "   Stop services:    $DOCKER_COMPOSE down"
echo "   Restart:          $DOCKER_COMPOSE restart"
echo "   Shell (backend):  $DOCKER_COMPOSE exec backend bash"
echo "   Shell (frontend): $DOCKER_COMPOSE exec frontend sh"
echo ""

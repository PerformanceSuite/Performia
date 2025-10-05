#!/bin/bash
# Development mode startup script for Command Center
set -e

echo "🛠️  Starting Command Center (Development Mode)..."

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
        echo "📝 Created .env from template - using development defaults"
    else
        echo "⚠️  No .env file found, using environment defaults"
    fi
fi

# Start services with development config
echo "🚀 Starting development services with hot reload..."
$DOCKER_COMPOSE -f docker-compose.dev.yml up --build

# This will run in foreground with logs streaming
# Press Ctrl+C to stop all services

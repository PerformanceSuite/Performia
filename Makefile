.PHONY: help setup up down restart logs shell-backend shell-frontend clean dev build test ps

# Detect docker compose command
DOCKER_COMPOSE := $(shell if docker compose version >/dev/null 2>&1; then echo "docker compose"; else echo "docker-compose"; fi)

help: ## Show this help message
	@echo "Command Center - Docker Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

setup: ## Initial setup - copy env and start production services
	@./scripts/setup.sh

up: ## Start production services in detached mode
	@echo "🚀 Starting production services..."
	@$(DOCKER_COMPOSE) up -d
	@echo "✅ Services started!"

down: ## Stop and remove all containers
	@echo "🛑 Stopping services..."
	@$(DOCKER_COMPOSE) down
	@echo "✅ Services stopped!"

restart: ## Restart all services
	@echo "🔄 Restarting services..."
	@$(DOCKER_COMPOSE) restart
	@echo "✅ Services restarted!"

logs: ## Tail logs from all services
	@$(DOCKER_COMPOSE) logs -f

shell-backend: ## Open bash shell in backend container
	@$(DOCKER_COMPOSE) exec backend bash

shell-frontend: ## Open sh shell in frontend container
	@$(DOCKER_COMPOSE) exec frontend sh

shell-db: ## Open psql shell in database
	@$(DOCKER_COMPOSE) exec postgres psql -U commandcenter -d commandcenter

clean: ## Stop services and remove volumes (WARNING: deletes all data!)
	@echo "⚠️  WARNING: This will delete all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(DOCKER_COMPOSE) down -v; \
		echo "✅ Cleanup complete!"; \
	else \
		echo "❌ Cancelled"; \
	fi

dev: ## Start development environment with hot reload
	@./scripts/dev.sh

build: ## Build all Docker images
	@echo "🔨 Building images..."
	@$(DOCKER_COMPOSE) build
	@echo "✅ Build complete!"

build-no-cache: ## Build all Docker images without cache
	@echo "🔨 Building images (no cache)..."
	@$(DOCKER_COMPOSE) build --no-cache
	@echo "✅ Build complete!"

ps: ## Show status of all services
	@$(DOCKER_COMPOSE) ps

test: ## Run tests (when implemented)
	@echo "🧪 Running tests..."
	@$(DOCKER_COMPOSE) exec backend pytest
	@$(DOCKER_COMPOSE) exec frontend npm test

prune: ## Clean up Docker system (removes unused images, containers, networks)
	@echo "🧹 Cleaning up Docker system..."
	@docker system prune -f
	@echo "✅ Cleanup complete!"

health: ## Check health status of all services
	@echo "🏥 Checking service health..."
	@$(DOCKER_COMPOSE) ps --format "table {{.Name}}\t{{.Status}}\t{{.Health}}"

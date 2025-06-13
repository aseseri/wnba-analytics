# Makefile for WNBA Analytics Project

# Color codes for prettier output
GREEN  := $(shell tput -T xterm setaf 2)
YELLOW := $(shell tput -T xterm setaf 3)
RESET  := $(shell tput -T xterm sgr0)

# Use .PHONY to ensure these commands run even if a file with the same name exists
.PHONY: all test test-backend test-frontend setup seed-db build-model clean up down build logs

# Default command when you just type "make"
all: up

# ==============================================================================
# 			APPLICATION LIFECYCLE
# ==============================================================================
up: ## Start all services in detached mode
	@echo "$(GREEN)--> Starting all services...$(RESET)"
	@docker compose up -d

down: ## Stop all services
	@echo "$(YELLOW)--> Stopping all services...$(RESET)"
	@docker compose down

build: ## Build or rebuild all services
	@echo "$(YELLOW)--> Building all services...$(RESET)"
	@docker compose up --build -d

clean: ## Stop and REMOVE all containers, networks, and volumes
	@echo "$(YELLOW)--> Tearing down all services and volumes...$(RESET)"
	@docker compose down -v

logs: ## Follow logs for all services
	@echo "$(GREEN)--> Following logs...$(RESET)"
	@docker compose logs -f

# ==============================================================================
# 			DEVELOPMENT & TESTING
# ==============================================================================
setup: up seed-db build-model ## Run this once to setup a new environment
	@echo "$(GREEN)✅ Initial setup complete!$(RESET)"

seed-db: ## Run the database seed script (requires services to be up)
	@echo "$(YELLOW)--> Seeding database...$(RESET)"
	@docker compose exec backend python seed_database.py

build-model: ## Run the ML model training script (requires services to be up)
	@echo "$(YELLOW)--> Building similarity model...$(RESET)"
	@docker compose exec backend python build_similarity_model.py

test: test-backend test-frontend ## Run all backend and frontend tests

test-backend: ## Run backend python tests
	@echo "$(GREEN)--> Running backend tests...$(RESET)"
	@docker compose run --rm backend pytest
	@docker compose down

test-frontend: ## Run frontend javascript tests
	@echo "$(GREEN)--> Running frontend tests...$(RESET)"
	@docker compose run --rm frontend npm test -- --watchAll=false
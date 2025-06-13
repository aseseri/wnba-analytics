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
setup: up seed-db build-model ## Run this once to setup a new LOCAL environment from scratch
	@echo "$(GREEN)✅ Initial local setup complete! Database is seeded and model is built.$(RESET)"

seed-db: ## Run the database seed script on the LOCAL docker DB
	@echo "$(YELLOW)--> Seeding LOCAL database...$(RESET)"
	@docker compose exec backend python seed_database.py

build-model: ## Run the ML model training script
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

test-ci: ## Simulate the CI environment perfectly
	@echo "$(YELLOW)--> Running tests in a clean CI-like environment...$(RESET)"
	@docker run --rm \
		-v "$(shell pwd)/backend":/app \
		-w /app \
		python:3.11-slim \
		sh -c "pip install -r requirements.txt && pip install pytest && pytest"

# ==============================================================================
# 			PRODUCTION BUILDS
# ==============================================================================
build-frontend-prod: ## Build the production frontend image for deployment
	@echo "$(YELLOW)--> Building production frontend image...$(RESET)"
	@gcloud builds submit --config frontend/cloudbuild.yaml \
	  --substitutions=_API_BASE_URL=https://wnba-backend-service-776933261932.us-west1.run.app \
	  ./frontend

# You could also add one for the backend for consistency
build-backend-prod: ## Build the production backend image for deployment
	@echo "$(YELLOW)--> Building production backend image...$(RESET)"
	@gcloud builds submit ./backend --tag gcr.io/wnba-analytics-prod/wnba-backend

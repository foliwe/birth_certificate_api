.PHONY: help install run dev seed test lint format clean docker-build docker-run

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements.txt
	pip install pytest pytest-asyncio httpx black flake8 mypy

run:  ## Run the application
	python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev:  ## Run in development mode with auto-reload
	python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

seed:  ## Populate database with sample data
	python app/seed_data.py

test-db:  ## Test database connection
	python app/test_db.py

test:  ## Run tests
	python -m pytest tests/ -v

lint:  ## Run linting
	flake8 app/
	mypy app/

format:  ## Format code
	black app/

clean:  ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -f *.db *.sqlite *.sqlite3

docker-build:  ## Build Docker image
	docker build -t birth-certificate-api .

docker-run:  ## Run with Docker Compose
	docker-compose up --build

docker-down:  ## Stop Docker containers
	docker-compose down

docker-logs:  ## View Docker logs
	docker-compose logs -f
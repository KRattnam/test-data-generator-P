# TDG Makefile - shortcut commands

.PHONY: help run stop restart logs shell db-shell redis-shell migrate test lint demo

help:
	@echo ""
	@echo " TDG- Test Data Generator"
	@echo ""
	@echo " make run Start all services"
	@echo " make stop stop all services"
	@echo " make restart stop + start"
	@echo " make logs Follow all logs"
	@echo " make shell Open bash in tdg-api container"
	@echo " make db-shell Open psql in postgres container"
	@echo " make redis-shell Open redis-cli"
	@echo " make migrate Run Alembic DB migrations"
	@echo " make test Run test suite"
	@echo " make lint Run ruff linter"
	@echo " make demo Run the 5-minute demo script"
	@echo " make fresh Stop + destroy volumes + restart (fresh DB)"
	@echo ""

run:
	docker compose up -d
	@echo ""
	@echo " Services started:"
	@echo " API: http://localhost:8000"
	@echo " API Docs: http://localhost:8000/docs"
	@echo " Grafana: http://localhost:3000 (admin/admin)"
	@echo " Prometheus: http://localhost:9090"
	@echo ""

# Stop all Services
stop:
	docker compose down

# Stop and Restart
restart: stop run

#Follow logs for all services ( ctrl + C to exit)
logs:
	docker compose logs -f

# Follow logs for one service: make logs-api
logs-%:
	docker compose logs -f $*

# Open bas shell inside the API container
shell:
	Ddocker compose exec tdg-api bash

# OPEN POSTGRESQL SHELL
db-shell:
	docker compose exec postgres psql -U tdg_user -d tdg

# Open Redis CLI
redis-shell:
	docker compose exec redis redis-cli

# RUn alembic migrations ( creates/ updates tabes)
migrate:
	docker compose exec tdg-api alembic upgrade head

# Run test suite
test:
	docker compose exec tdg-api pytest tests/ -v --cov=tdg --cov-report=term-missing

# Run Linter
lint:
	docker compose exec tdg-api ruff check tdg/ tests/

# Run the demo script
demo:
	./scripts/demo.sh

# Full reset - destroys all data
fresh:
	docker compose down -v
	docker compose up -d
	@echo " Fresh Stack started - all data cleared"

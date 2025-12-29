# Makefile for EcoPath Django Project

.PHONY: help migrate collectstatic createsuperuser test

help:
	@echo "Commands:"
	@echo "  migrate         - Apply database migrations"
	@echo "  collectstatic   - Collect static files for production"
	@echo "  createsuperuser - Create a new superuser"
	@echo "  test            - Run the pytest test suite"

migrate:
	@python manage.py migrate

collectstatic:
	@python manage.py collectstatic --noinput

createsuperuser:
	@python manage.py createsuperuser

test:
	@pytest

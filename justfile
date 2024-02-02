# Run all lints
lints:
    ruff check . && mypy . && black . && isort .

# Build containers
build CON_NAME='':
    docker compose up -d --build {{CON_NAME}}

# Up anyone container
up CON_NAME='':
    docker compose up -d {{CON_NAME}}

# Create migration
migration MIGRATION_NAME='':
    alembic revision --autogenerate -m "{{MIGRATION_NAME}}"

# Upgrade migration
upgrade VERSION='head':
    alembic upgrade {{VERSION}}

# Downgrade migrations
downgrade VERSION='-1':
    alembic downgrade {{VERSION}}

# Run tests
test ARGS='tests':
    poetry run pytest -v --cov=src --cov-report=html --durations=10 --failed-first -n 4 {{ARGS}}

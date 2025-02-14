# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.13-slim AS python-base

# Python configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Base stage for dev and prod
FROM python-base AS base
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install --no-cache-dir pipenv

ENV PYTHONPATH=/app
WORKDIR /app
COPY Pipfile Pipfile.lock ./

# Development stage
FROM base AS api-dev
RUN pipenv install --dev --system --deploy
COPY . .
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# Test stage
FROM base AS api-test
RUN pipenv install --dev --system --deploy
COPY . .
CMD ["pytest", "-v"]

# Production stage
FROM base AS api-prod
RUN pipenv install --system --deploy
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]

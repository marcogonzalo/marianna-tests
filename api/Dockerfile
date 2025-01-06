# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim AS python-base
WORKDIR /app

FROM python-base AS api-base
RUN pip install --no-cache-dir --upgrade pip
# Install pipenv and global requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pipenv
# Install dependencies into the system (--system flag is important here!)
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
# Copy after installing dependencies to leverage Docker cache
COPY . .
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# Create a non-root user with UID 5678 for security best practices
RUN addgroup --system appgroup && \
    adduser --system --uid 5678 --ingroup appgroup --no-create-home --disabled-password --gecos "" appuser && \
    chown -R appuser:appgroup /app
    
FROM api-base AS api-dev
# Switch to non-root user for better security
USER appuser
# Development command
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

FROM api-base AS api-prod
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1
# Switch to non-root user for better security
USER appuser
# Production command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]

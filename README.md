# Assessment System

A system for creating and managing assessments with different scoring methods.

## Prerequisites

- Docker and Docker Compose
- Python 3.x (for local development)
- Node.js 22.x (for local client development)

## Project Structure

- `api/`: FastAPI backend service
- `client/`: React 19 frontend application with Vite

## Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Copy the environment files and configure your variables:
```bash
# API environment
cd api
cp .env.example .env.development

# Client environment
cd ../client
cp .env.example .env.development
```

3. Start the development environment:
```bash
docker-compose up
```

This will start:
- The client application at http://localhost:5173
- The API service at http://localhost:8000
- A PostgreSQL database at localhost:5432

### API Documentation

Once the API is running, you can access:
- Interactive API documentation (Swagger UI): http://localhost:8000/docs
- Alternative API documentation (ReDoc): http://localhost:8000/redoc

## Test Environment

To run the test suite:

```bash
# Run all tests
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

# Run specific tests
docker-compose -f docker-compose.test.yml run api pytest api/tests/specific_test.py

# Run with coverage report
docker-compose -f docker-compose.test.yml run api pytest --cov=api api/tests/
```

## Production Environment

To deploy the application in production:

1. Configure production environment variables:
```bash
# API production environment
cd api
cp .env.example .env
# Edit .env.prod with your production settings

# Client production environment
cd ../client
cp .env.example .env
# Edit .env.prod with your production settings
```

2. Build and start the production services:
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

This will start:
- The client application at http://localhost:5173 (served by nginx)
- The API service at http://localhost:8000
- A PostgreSQL database at localhost:5432

3. Create the initial admin user in production (if first deployment):
```bash
docker-compose -f docker-compose.prod.yml exec api pipenv run create-admin
```

### Production Health Checks

The production environment includes health checks for all services:
- Client: http://localhost:5173/health
- API: http://localhost:8000/health
- Database: Automatically checked by Docker

## Development Without Docker

### API Setup

```bash
cd api
pipenv shell
pipenv install
pipenv run create-admin  # Create initial admin user
uvicorn main:app --reload
```

### Client Setup

```bash
cd client
npm install
npm run dev
```

The client will be available at http://localhost:5173

## Environment Variables

### API Environment Variables:
- `DATABASE_URL`: PostgreSQL connection string
- `ENVIRONMENT`: Development/production environment
- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: JWT secret key (required in production)
- `CORS_ORIGINS`: Allowed CORS origins

### Client Environment Variables:
- `VITE_API_URL`: API endpoint URL (default: http://api:8000 in Docker)
- `HOST`: Host to bind the development server (default: 0.0.0.0)

Check `.env.example` files in both api/ and client/ directories for all available configuration options.

## Common Issues

1. If you get permission errors with the database volume:
```bash
sudo chown -R 1000:1000 postgres_data/
```

2. If the client build fails with TypeScript errors in production:
```bash
# You can force the build with
docker-compose -f docker-compose.prod.yml build --build-arg TSC_COMPILE_ON_ERROR=true
```

3. If you need to reset the database:
```bash
# Stop all containers and remove volumes
docker-compose down -v
# Then restart with
docker-compose up --build
``` 
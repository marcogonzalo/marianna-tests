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
cp .env.example .env

# Client environment
cd ../client
cp .env.example .env
```

3. Start the development environment:
```bash
docker-compose up
```

This will start:
- The client application at http://localhost:5137
- The API service at http://localhost:8000
- A PostgreSQL database at localhost:5432

### API Documentation

Once the API is running, you can access:
- Interactive API documentation (Swagger UI): http://localhost:8000/docs
- Alternative API documentation (ReDoc): http://localhost:8000/redoc

## Running Tests

To run the test suite:

```bash
# Run all tests
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

# Run specific tests
docker-compose -f docker-compose.test.yml run api pytest api/tests/specific_test.py
```

## Development Without Docker

### API Setup

```bash
cd api
pipenv install
pipenv shell
uvicorn main:app --reload
```

### Client Setup

```bash
cd client
npm install
npm run dev
```

The client will be available at http://localhost:5137

## Environment Variables

### API Environment Variables:
- `DATABASE_URL`: PostgreSQL connection string
- `ENVIRONMENT`: Development/production environment
- `DEBUG`: Enable/disable debug mode

### Client Environment Variables:
- `VITE_API_URL`: API endpoint URL (default: http://api:8000 in Docker)
- `HOST`: Host to bind the development server (default: 0.0.0.0)

Check `.env.example` files in both api/ and client/ directories for all available configuration options. 
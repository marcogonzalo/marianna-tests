# Assessment System

A system for creating and managing assessments with different scoring methods.

## Prerequisites

- Docker and Docker Compose
- Python 3.x (for local development)
- Node.js (for local client development)

## Project Structure

- `api/`: FastAPI backend service
- `client/`: Frontend application

## Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Copy the environment file and configure your variables:
```bash
cd api
cp .env.example .env
```

3. Start the development environment:
```bash
docker-compose up
```

This will start:
- The API service at http://localhost:8000
- The client application at http://localhost:3000
- A PostgreSQL database

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

## Environment Variables

Key environment variables for the API:

- `DATABASE_URL`: PostgreSQL connection string
- `ENVIRONMENT`: Development/production environment
- `DEBUG`: Enable/disable debug mode

Check `.env.example` for all available configuration options. 
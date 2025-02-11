from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from assessments.routes import router as assessments_router
from database import create_db_and_tables
import os

CLIENT_URL = os.getenv("CLIENT_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # Clean up tasks here

app = FastAPI(
    title="Assessments API",
    description="API for managing assessments and their questions",
    version="1.0.0",
    lifespan=lifespan
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the assessments router
app.include_router(assessments_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from assessments.routes import router as assessments_router
from database import create_db_and_tables
import os

app = FastAPI(
    title="Assessments API",
    description="API for managing assessments and their questions",
    version="1.0.0"
)

CLIENT_URL = os.getenv("CLIENT_URL")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include the assessments router
app.include_router(assessments_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

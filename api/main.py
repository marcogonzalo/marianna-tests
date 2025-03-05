from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager
from app.assessments.routes import assessments_router
from app.responses.routes import responses_router
from app.users.routes import users_router, accounts_router, examinees_router
from app.auth.routes import auth_router
from app.assessments.models import Assessment, Question, Choice
from app.responses.models import AssessmentResponse, QuestionResponse
from app.users.models import Account, User
from app.auth.models import TokenBlacklist

CLIENT_URL = os.getenv("CLIENT_URL")


@asynccontextmanager
async def lifespan(app: FastAPI):
    from database import create_db_and_tables

    print("Starting up...")
    if os.getenv("ENV") not in ["production"]:
        print("Development mode: Creating database tables...")
        create_db_and_tables()
    yield
    print("Shutting down...")

app = FastAPI(
    title="Assessments API",
    description="API for managing assessments and their questions",
    version="1.0.0",
    # lifespan=lifespan
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
app.include_router(responses_router)
app.include_router(users_router)
app.include_router(accounts_router)
app.include_router(examinees_router)
app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}

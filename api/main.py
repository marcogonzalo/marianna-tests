from fastapi import FastAPI
from assessments.routes import router as assessments_router
from database import create_db_and_tables

app = FastAPI(
    title="Assessments API",
    description="API for managing assessments and their questions",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include the assessments router
app.include_router(assessments_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
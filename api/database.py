import os
from typing import Generator
from sqlmodel import SQLModel, Session, create_engine
from utils.database import get_database_url

# Default to SQLite for development if no DATABASE_URL is provided
DATABASE_URL = get_database_url()

engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("ENV") != "production",
)


def create_db_and_tables():
    print("Creating tables...")
    tables = SQLModel.metadata.tables
    print(f"Tables to be created: {', '.join(tables.keys())}")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

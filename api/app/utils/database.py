import os


def _get_database_url_from_env_vars():
    DB_SCHEME = os.getenv("DB_SCHEME", "postgresql")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "assessments")
    return f"{DB_SCHEME}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_database_url():
    url = os.getenv("DATABASE_URL", _get_database_url_from_env_vars())
    return url

import os


def get_database_url():
    url = os.getenv("DATABASE_URL")
    if not url:
        url = get_database_url_from_env_vars()
    return url


def get_database_url_from_env_vars():
    DB_SCHEME = os.getenv("DB_SCHEME", "postgresql")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "assessments")
    return f"{DB_SCHEME}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

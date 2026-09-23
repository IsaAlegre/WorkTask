import os


def database_url() -> str:
    url = os.environ.get("DATABASE_URL", "sqlite:///tasks.db")
    # Fly entrega "postgres://..." y SQLAlchemy necesita saber qué driver usar
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return url.replace(prefix, "postgresql+psycopg://", 1)
    return url
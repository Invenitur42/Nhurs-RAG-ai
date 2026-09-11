"""
Initialize the database: create pgvector extension and all tables.
Run once after starting Postgres:

    python -m app.db.init_db
"""

from sqlalchemy import text

from app.db.session import engine, Base
from app.models import User, Document, DocumentChunk  # noqa: F401 – register models


def init_db() -> None:
    with engine.begin() as conn:
        # Enable the vector extension (required for embeddings)
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

    # Create all tables defined on Base
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully (extension + tables).")


if __name__ == "__main__":
    init_db()

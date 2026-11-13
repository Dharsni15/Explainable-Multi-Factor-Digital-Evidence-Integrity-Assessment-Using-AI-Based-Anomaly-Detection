# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.config import DATABASE_URL

# SQLite connect_args needed for multithreading in FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Database session dependency for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_database_schema():
    """Ensures all columns exist in SQLite tables on application startup."""
    from sqlalchemy import text
    with engine.connect() as conn:
        try:
            result = conn.execute(text("PRAGMA table_info(evidence)"))
            existing_cols = {row[1] for row in result.fetchall()}
            new_cols = [
                ("baseline_created_at", "DATETIME"),
                ("verification_filepath", "VARCHAR(500)"),
                ("verification_filename", "VARCHAR(255)"),
                ("latest_verification_hash", "VARCHAR(64)"),
                ("latest_verification_result", "VARCHAR(100)"),
                ("latest_verification_status", "VARCHAR(50)"),
                ("latest_metadata_status", "VARCHAR(50)"),
                ("latest_metadata_diff_json", "TEXT")
            ]
            for col_name, col_type in new_cols:
                if col_name not in existing_cols:
                    conn.execute(text(f"ALTER TABLE evidence ADD COLUMN {col_name} {col_type}"))
            conn.commit()
        except Exception:
            pass


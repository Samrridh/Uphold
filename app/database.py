from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


def _default_database_url() -> str:
    # Vercel filesystem is read-only except /tmp; local dev uses a file in the project.
    if os.getenv("VERCEL"):
        return "sqlite:////tmp/uphold.db"
    return "sqlite:///./local.db"


DATABASE_URL = os.getenv("DATABASE_URL") or _default_database_url()

_connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)
engine = create_engine(DATABASE_URL, connect_args=_connect_args)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""Vercel FastAPI entrypoint (supported name per Vercel docs)."""
from app.main import app

__all__ = ["app"]

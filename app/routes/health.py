"""Lightweight diagnostics for deployment (keys / DB). No secrets returned."""

from fastapi import APIRouter
from sqlalchemy import text

from app.database import engine
from app.services.crypto import load_private_key_auto, load_public_key_auto

router = APIRouter(tags=["Health"])


@router.get("/health/keys")
def health_keys():
    """Whether signing/verify keys load. Open this in the browser when certify fails."""
    out: dict = {}

    try:
        load_private_key_auto()
        out["private_key"] = "ok"
    except Exception as e:
        out["private_key"] = "error"
        out["private_key_error"] = f"{type(e).__name__}: {str(e)[:400]}"

    try:
        load_public_key_auto()
        out["public_key"] = "ok"
    except Exception as e:
        out["public_key"] = "error"
        out["public_key_error"] = f"{type(e).__name__}: {str(e)[:400]}"

    return out


@router.get("/health/db")
def health_db():
    """Quick DB connectivity check."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"database": "ok"}
    except Exception as e:
        return {"database": "error", "detail": f"{type(e).__name__}: {str(e)[:400]}"}

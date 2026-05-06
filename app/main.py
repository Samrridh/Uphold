import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.routes import health, proofs, sign, verify, ai_summarize
from app.database import engine, Base
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Uphold - Document Certification API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_private_network=True,
)

app.include_router(sign.router, prefix="/api", tags=["Sign"])
app.include_router(verify.router, prefix="/api", tags=["Verify"])
app.include_router(proofs.router, prefix="/api", tags=["Proofs"])
app.include_router(health.router, prefix="/api")
app.include_router(ai_summarize.router,prefix="/api",tags=["AI"])


if os.getenv("VERCEL"):

    @app.get("/")
    def root_redirect():
        return RedirectResponse(url="/index.html", status_code=307)

else:
    _PUBLIC = Path(__file__).resolve().parent.parent / "public"
    if _PUBLIC.is_dir():
        app.mount("/", StaticFiles(directory=str(_PUBLIC), html=True), name="public")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import sign, verify,proofs
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

app.include_router(sign.router,prefix="/api", tags=["Sign"])
app.include_router(verify.router,prefix="/api",tags=["Verify"])
app.include_router(proofs.router, prefix="/api", tags=["Proofs"])

@app.get("/")
def root():
    return {"message": "DocSign API is running"}
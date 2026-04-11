from fastapi import FastAPI
from app.routes import sign, verify
from app.database import engine, Base
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Uphold - Document Certification API")

app.include_router(sign.router,prefix="/api", tags=["Sign"])
app.include_router(verify.router,prefix="/api",tags=["Verify"])

@app.get("/")
def root():
    return {"message": "DocSign API is running"}
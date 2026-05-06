from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.ai_summarize import summarize_file

router = APIRouter()

ALLOWED_EXTENSIONS  = {".pdf",".txt",".md", '.csv'}
MAX_SIZE = 10*1024*1024

@router.post("/ai/summarize")
async def ai_summarize(file:UploadFile = File(...)):
    content = await file.read()

    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=413,detail="Max file size 10MB")
    
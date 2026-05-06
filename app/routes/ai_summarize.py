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
    
    filename = file.filename or ""
    ext = "." + filename.rsplit(".",1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Supported are pdf,txt,md,csv",
        )

    if not content.strip():
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        summary = summarize_file(content,filename)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
        
    except Exception:
        raise HTTPException(status_code=502,detail="Request failed")
    
    return {"filename":filename, "summary":summary}
from fastapi import APIRouter,UploadFile,File,Form
from app.services.crypto import load_public_key,hash_document, verify_document
import os

router = APIRouter()

@router.post("/verify")
async def verify(
    file: UploadFile = File(...),
    signature: str = Form(...)
):
    content = await file.read()
    doc_hash = hash_document(content)
    public_key = load_public_key(os.getenv("PUBLIC_KEY_PATH"))
    is_valid = verify_document(content,signature,public_key)

    return{
        "doc_hash": doc_hash,
        "valid": is_valid,
        "message": "Document is authentic" if is_valid else "Document has been tampered"
    }
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.services.crypto import load_public_key_auto, hash_document, verify_document

router = APIRouter()


@router.post("/verify")
async def verify(
    file: UploadFile = File(...),
    signature: str = Form(...)
):
    content = await file.read()
    doc_hash = hash_document(content)
    try:
        public_key = load_public_key_auto()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    is_valid = verify_document(content,signature,public_key)

    return{
        "doc_hash": doc_hash,
        "valid": is_valid,
        "message": "Document is authentic" if is_valid else "Document has been tampered"
    }
from fastapi import APIRouter,UploadFile,File,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.crypto import load_private_key,hash_document,sign_document
from app.services.storage import save_proof,get_proof_by_hash
from fastapi import HTTPException
import os

router = APIRouter()

@router.post("/sign")
async def sign(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    doc_hash = hash_document(content)

    existing = get_proof_by_hash(db, doc_hash)
    if existing:
        raise HTTPException(status_code=400, detail="Document already signed")
    
    private_key = load_private_key(os.getenv("PRIVATE_KEY_PATH"))
    signature = sign_document(content,private_key)
    proof = save_proof(db,file.filename,doc_hash,signature)

    return{
        "id": proof.id,
        "filename": proof.filename,
        "doc_hash": doc_hash,
        "signature": signature,
        "signed_at": proof.signed_at
    }
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.storage import get_proof_by_hash

router = APIRouter()


@router.get("/proofs/{doc_hash}")
def get_proof(doc_hash: str, db: Session = Depends(get_db)):
    proof = get_proof_by_hash(db, doc_hash)
    if not proof:
        raise HTTPException(
            status_code=404, detail="No proof found for this document"
        )
    return {
        "id": proof.id,
        "filename": proof.filename,
        "doc_hash": proof.doc_hash,
        "signature": proof.signature,
        "signed_at": proof.signed_at,
    }

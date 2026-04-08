from sqlalchemy.orm import Session
from app.models.proof import Proof

def save_proof(db:Session, filename: str, doc_hash:str, signature:str) -> Proof:
    proof = Proof(filename=filename,doc_hash=doc_hash,signature=signature)
    db.add(proof)
    db.commit()
    db.refresh(proof)
    return proof

def get_proof_by_harsh(db: Session, doc_hash:str) -> Proof | None:
    return db.query(Proof).filter(Proof.doc_hash == doc_hash).first()
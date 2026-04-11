from sqlalchemy import Column, String, DateTime
from app.database import Base
from datetime import datetime
import uuid

class Proof(Base):
    __tablename__ = 'proofs'
    id = Column(String,primary_key=True,default=lambda:str(uuid.uuid4()))
    filename = Column(String,nullable=False)
    doc_hash = Column(String,nullable = False, unique=True)
    signature = Column(String,nullable = False)
    signed_at = Column(DateTime,default=datetime.utcnow)
    
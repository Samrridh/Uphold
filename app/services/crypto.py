from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import hashlib

def load_private_key(path:str):
    with open(path,'rb') as f:
        return serialization.load_pem_private_key(f.read(),password=None)
    
def load_public_key(path:str):
    with open(path,'rb') as f:
        return serialization.load_pem_public_key(f.read())

def hash_document(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def sign_document(content:bytes, private_key) -> str:
    signature = private_key.sign(
        content,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature.hex()

def verify_document(content:bytes,signature_hex:str,public_key) -> bool:
    try:
        public_key.verify(
            bytes.fromhex(signature_hex),
            content,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    



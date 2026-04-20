import base64
import binascii
import hashlib
import os
import re

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def _normalize_pem_from_env(raw: str) -> str:
    pem = raw.strip()
    if "\\n" in pem and pem.count("\n") < 2:
        pem = pem.replace("\\n", "\n")
    return pem


def _repair_flattened_pem(pem: str) -> str:
    """Vercel / dashboards often strip or replace newlines; restore PEM line breaks."""
    pem = pem.replace("\r\n", "\n").replace("\r", "\n").strip()
    if pem.count("\n") >= 3:
        return pem
    m = re.match(
        r"(-----BEGIN [A-Z0-9 ]+-----)\s*(.+?)\s*(-----END [A-Z0-9 ]+-----)\s*$",
        pem,
        re.DOTALL,
    )
    if not m:
        return pem
    begin, body, end = m.group(1), m.group(2), m.group(3)
    body_clean = re.sub(r"\s+", "", body)
    wrapped = "\n".join(body_clean[i : i + 64] for i in range(0, len(body_clean), 64))
    return f"{begin}\n{wrapped}\n{end}\n"


def _load_pem_private_key_from_string(pem: str):
    pem = _repair_flattened_pem(_normalize_pem_from_env(pem))
    try:
        return serialization.load_pem_private_key(pem.encode("utf-8"), password=None)
    except ValueError as e:
        raise RuntimeError(
            "Could not parse PRIVATE_KEY_PEM. Use real newlines, or set "
            "PRIVATE_KEY_PEM_B64 to the base64 of the entire .pem file (see .env.example)."
        ) from e


def _load_pem_public_key_from_string(pem: str):
    pem = _repair_flattened_pem(_normalize_pem_from_env(pem))
    try:
        return serialization.load_pem_public_key(pem.encode("utf-8"))
    except ValueError as e:
        raise RuntimeError(
            "Could not parse PUBLIC_KEY_PEM. Use real newlines, or set "
            "PUBLIC_KEY_PEM_B64 to the base64 of the entire .pem file."
        ) from e


def load_private_key_auto():
    """Order: PRIVATE_KEY_PEM_B64, PRIVATE_KEY_PEM, PRIVATE_KEY_PATH."""
    b64 = os.getenv("PRIVATE_KEY_PEM_B64")
    if b64 and b64.strip():
        try:
            raw = base64.standard_b64decode(b64.strip())
        except (ValueError, binascii.Error) as e:
            raise RuntimeError("PRIVATE_KEY_PEM_B64 is not valid base64.") from e
        try:
            return serialization.load_pem_private_key(raw, password=None)
        except ValueError as e:
            raise RuntimeError(
                "PRIVATE_KEY_PEM_B64 decodes but is not a valid PEM private key."
            ) from e

    pem_env = os.getenv("PRIVATE_KEY_PEM")
    if pem_env and pem_env.strip():
        return _load_pem_private_key_from_string(pem_env)

    path = os.getenv("PRIVATE_KEY_PATH")
    if path:
        try:
            with open(path, "rb") as f:
                return serialization.load_pem_private_key(f.read(), password=None)
        except OSError as e:
            raise RuntimeError(
                f"Could not read PRIVATE_KEY_PATH {path!r}: {e}. "
                "On Vercel use PRIVATE_KEY_PEM or PRIVATE_KEY_PEM_B64 instead."
            ) from e
    raise RuntimeError(
        "Set PRIVATE_KEY_PEM_B64, PRIVATE_KEY_PEM, or PRIVATE_KEY_PATH for signing."
    )


def load_public_key_auto():
    """Order: PUBLIC_KEY_PEM_B64, PUBLIC_KEY_PEM, PUBLIC_KEY_PATH."""
    b64 = os.getenv("PUBLIC_KEY_PEM_B64")
    if b64 and b64.strip():
        try:
            raw = base64.standard_b64decode(b64.strip())
        except (ValueError, binascii.Error) as e:
            raise RuntimeError("PUBLIC_KEY_PEM_B64 is not valid base64.") from e
        try:
            return serialization.load_pem_public_key(raw)
        except ValueError as e:
            raise RuntimeError(
                "PUBLIC_KEY_PEM_B64 decodes but is not a valid PEM public key."
            ) from e

    pem_env = os.getenv("PUBLIC_KEY_PEM")
    if pem_env and pem_env.strip():
        return _load_pem_public_key_from_string(pem_env)

    path = os.getenv("PUBLIC_KEY_PATH")
    if path:
        try:
            with open(path, "rb") as f:
                return serialization.load_pem_public_key(f.read())
        except OSError as e:
            raise RuntimeError(
                f"Could not read PUBLIC_KEY_PATH {path!r}: {e}. "
                "On Vercel use PUBLIC_KEY_PEM or PUBLIC_KEY_PEM_B64 instead."
            ) from e
    raise RuntimeError(
        "Set PUBLIC_KEY_PEM_B64, PUBLIC_KEY_PEM, or PUBLIC_KEY_PATH for verification."
    )


def load_private_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def load_public_key(path: str):
    with open(path, "rb") as f:
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
    



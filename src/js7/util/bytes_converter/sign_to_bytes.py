from pathlib import Path
from typing import List, Optional, Tuple, Union
import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, ec
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.types import PublicKeyTypes

from cryptography.hazmat.backends import default_backend


def _verify_signature(
    *,
    data: bytes,
    signature: bytes,
    public_key: Union[rsa.RSAPublicKey, ec.EllipticCurvePublicKey],
    hash_alg: hashes.HashAlgorithm,
) -> bool:
    try:
        if isinstance(public_key, rsa.RSAPublicKey):
            public_key.verify(
                signature,
                data,
                padding.PKCS1v15(),
                hash_alg,
            )
        else:
            public_key.verify(
                signature,
                data,
                ec.ECDSA(hash_alg),
            )
        return True
    except InvalidSignature:
        return False

def sign_to_bytes(
    *,
    files: List[Tuple[str, bytes]],
    private_key_file: Path,
    public_key_file: Optional[Path],
    key_password: Optional[bytes],
    hash_alg: hashes.HashAlgorithm
) -> List[Tuple[str, bytes]]:
    
    if not private_key_file or not hash_alg:
        raise ValueError("'private_key_file' and 'hash_alg' is required")

    # ---- load private key ----
    with open(private_key_file, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=key_password,
            backend=default_backend(),
        )

    if not isinstance(private_key, (rsa.RSAPrivateKey, ec.EllipticCurvePrivateKey)):
        raise TypeError("Only RSA and ECDSA private keys are supported")

    # ---- load public key ----
    public_key: Optional[PublicKeyTypes] = None

    if public_key_file:
        with open(public_key_file, "rb") as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend(),
            )

        if not isinstance(public_key, (rsa.RSAPublicKey, ec.EllipticCurvePublicKey)):
            raise TypeError("Unsupported public key type.")

    # ---- sign ----
    result: List[Tuple[str, bytes]] = []

    for path, data in files:
        if isinstance(private_key, rsa.RSAPrivateKey):
            signature = private_key.sign(
                data,
                padding.PKCS1v15(),
                hash_alg,
            )
        else:
            signature = private_key.sign(
                data,
                ec.ECDSA(hash_alg),
            )

        signature_b64_bytes = base64.b64encode(signature)
        
        sig_path = f"{path}.sig"
        
        # ---- optional verification ----
        if public_key:
            if not _verify_signature(
                data=data,
                signature=signature,
                public_key=public_key,
                hash_alg=hash_alg,
            ):
                raise ValueError(f"Signature verification failed for '{sig_path}'")

        result.append((sig_path, signature_b64_bytes))

    return result

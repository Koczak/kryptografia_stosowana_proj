"""
Cryptographic identity module (Ed25519 + Base58).
"""

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import base58


class CryptoIdentity:
    """Ed25519-based cryptographic identity and digital signatures."""

    def __init__(self, private_key: ed25519.Ed25519PrivateKey) -> None:
        self._private_key: ed25519.Ed25519PrivateKey = private_key
        self._public_key: ed25519.Ed25519PublicKey = private_key.public_key()

    @classmethod
    def generate(cls) -> "CryptoIdentity":
        """Generate a new random Ed25519 keypair."""
        return cls(ed25519.Ed25519PrivateKey.generate())

    @classmethod
    def from_private_bytes(cls, raw_seed: bytes) -> "CryptoIdentity":
        """Restore identity from 32-byte private key seed."""
        return cls(ed25519.Ed25519PrivateKey.from_private_bytes(raw_seed))

    @property
    def private_bytes(self) -> bytes:
        """Raw 32-byte private key seed."""
        return self._private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )

    @property
    def public_bytes(self) -> bytes:
        """Raw 32-byte public key."""
        return self._public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )

    @property
    def public_key_hex(self) -> str:
        """Public key encoded as a hex string."""
        return self.public_bytes.hex()

    @property
    def address(self) -> str:
        """Base58-encoded wallet address."""
        return base58.b58encode(self.public_bytes).decode("utf-8")

    def sign(self, message: bytes) -> bytes:
        """Sign message bytes using the private key."""
        return self._private_key.sign(message)

    @staticmethod
    def verify(message: bytes, signature: bytes, public_key_bytes: bytes) -> bool:
        """Verify an Ed25519 signature against the public key."""
        try:
            pub_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
            pub_key.verify(signature, message)
            return True
        except (InvalidSignature, Exception):
            return False

"""
Secure keystore module using AES-256-GCM and PBKDF2-HMAC-SHA256.
"""

import os
import json
from typing import Dict, Any

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

from crypto import CryptoIdentity


class SecureWallet:
    """Encrypts and decrypts private keys using password-derived keys."""

    KDF_ITERATIONS: int = 100_000
    SALT_SIZE: int = 16
    NONCE_SIZE: int = 12

    @classmethod
    def _derive_symmetric_key(cls, password: str, salt: bytes) -> bytes:
        """Derive a 256-bit AES key from password and salt via PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=cls.KDF_ITERATIONS,
        )
        return kdf.derive(password.encode("utf-8"))

    @classmethod
    def create_wallet_data(cls, identity: CryptoIdentity, password: str) -> Dict[str, Any]:
        """Encrypt private key and return keystore dictionary."""
        salt = os.urandom(cls.SALT_SIZE)
        nonce = os.urandom(cls.NONCE_SIZE)
        aes_key = cls._derive_symmetric_key(password, salt)

        aesgcm = AESGCM(aes_key)
        ciphertext_with_tag = aesgcm.encrypt(nonce, identity.private_bytes, None)

        return {
            "version": 1,
            "crypto_scheme": "Ed25519",
            "address": identity.address,
            "public_key": identity.public_key_hex,
            "crypto": {
                "cipher": "aes-256-gcm",
                "ciphertext": ciphertext_with_tag.hex(),
                "nonce": nonce.hex(),
                "kdf": "pbkdf2-sha256",
                "kdf_params": {
                    "iterations": cls.KDF_ITERATIONS,
                    "salt": salt.hex(),
                },
            },
        }

    @classmethod
    def unlock_wallet_data(cls, data: Dict[str, Any], password: str) -> CryptoIdentity:
        """Decrypt private key using provided password."""
        crypto_meta = data["crypto"]
        salt = bytes.fromhex(crypto_meta["kdf_params"]["salt"])
        nonce = bytes.fromhex(crypto_meta["nonce"])
        ciphertext_with_tag = bytes.fromhex(crypto_meta["ciphertext"])

        aes_key = cls._derive_symmetric_key(password, salt)
        aesgcm = AESGCM(aes_key)

        try:
            raw_private = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
            return CryptoIdentity.from_private_bytes(raw_private)
        except InvalidTag:
            raise ValueError("Invalid password (authentication tag mismatch).")

    @classmethod
    def save_file(cls, filepath: str, wallet_data: Dict[str, Any]) -> None:
        """Save keystore dictionary to a JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(wallet_data, f, indent=2)

    @classmethod
    def load_file(cls, filepath: str) -> Dict[str, Any]:
        """Load keystore dictionary from a JSON file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File '{filepath}' not found.")
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

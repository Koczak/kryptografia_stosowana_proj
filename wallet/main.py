"""
Wallet CLI application.
"""

import os
import sys
import json
import urllib.request

from crypto import CryptoIdentity
from keystore import SecureWallet


def run_test() -> None:
    """Run self-tests for identity, encryption, and signatures."""
    print("Test 1: Generating Ed25519 identity and Base58 address...")
    id1 = CryptoIdentity.generate()
    assert len(id1.public_bytes) == 32 and len(id1.private_bytes) == 32
    print(f"  Address: {id1.address}")

    print("Test 2: Encrypting wallet (AES-256-GCM + PBKDF2)...")
    w_data = SecureWallet.create_wallet_data(id1, "Password123!")

    print("Test 3: Unlocking with incorrect password...")
    try:
        SecureWallet.unlock_wallet_data(w_data, "WRONG_PASSWORD")
        assert False, "Wallet should not unlock with incorrect password"
    except ValueError:
        print("  Access denied (invalid auth tag)")

    print("Test 4: Digital signature and verification...")
    unlocked = SecureWallet.unlock_wallet_data(w_data, "Password123!")
    msg = b"Sample transaction payload"
    sig = unlocked.sign(msg)
    assert CryptoIdentity.verify(msg, sig, unlocked.public_bytes) is True
    assert CryptoIdentity.verify(b"Tampered payload", sig, unlocked.public_bytes) is False
    print("  Signature verified successfully")

    print("\nAll tests passed.")


def run_wallet(filepath: str = "wallet.json", password: str = "password123") -> None:
    """Create a new wallet or unlock an existing keystore file."""
    if not os.path.exists(filepath):
        identity = CryptoIdentity.generate()
        data = SecureWallet.create_wallet_data(identity, password)
        SecureWallet.save_file(filepath, data)
        print(f"Created wallet {filepath} (password: '{password}')")
        print(f"Address:    {identity.address}")
        print(f"Public key: {identity.public_key_hex}")
    else:
        data = SecureWallet.load_file(filepath)
        try:
            identity = SecureWallet.unlock_wallet_data(data, password)
            print(f"Unlocked wallet {filepath}:")
            print(f"Address:     {identity.address}")
            print(f"Private key: {identity.private_bytes.hex()}")
        except ValueError as e:
            print(f"Error: {e}")


def run_status(port: str = "3001") -> None:
    """Query node status via HTTP RPC."""
    url = port if port.startswith("http") else f"http://127.0.0.1:{port}/status"
    try:
        with urllib.request.urlopen(url, timeout=3.0) as resp:
            data = json.loads(resp.read().decode())
            print(f"Node:            {data.get('node_id')}")
            print(f"Status:          {data.get('status')}")
            print(f"Connected peers: {data.get('connected_peers_count')}")
            print(f"Active peers:    {data.get('connected_peers')}")
            print(f"Known nodes:     {data.get('all_known_peers')}")
    except Exception as e:
        print(f"Connection error ({url}): {e}")


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "test":
        run_test()
    elif cmd == "status":
        port = sys.argv[2] if len(sys.argv) > 2 else "3001"
        run_status(port)
    elif cmd in ("create", "info", "open"):
        pwd = sys.argv[2] if len(sys.argv) > 2 else "password123"
        run_wallet("wallet.json", pwd)
    elif cmd == "help":
        print("Wallet Usage:")
        print("  python wallet/main.py test")
        print("  python wallet/main.py [password]")
        print("  python wallet/main.py status [3001]")
    else:
        run_wallet("wallet.json", cmd)


if __name__ == "__main__":
    main()

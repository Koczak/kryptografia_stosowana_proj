"""
P2P Node entrypoint.
Usage:
  python node/main.py [p2p_port] [rpc_port] [peer_port]

Examples:
  python node/main.py 6001 3001
  python node/main.py 6002 3002 6001
"""

import sys
import asyncio

from p2p import P2PNode


def main() -> None:
    p2p_port = int(sys.argv[1]) if len(sys.argv) > 1 else 6001
    rpc_port = int(sys.argv[2]) if len(sys.argv) > 2 else 3001
    peer_port = sys.argv[3] if len(sys.argv) > 3 else ""

    node = P2PNode(p2p_port=p2p_port, rpc_port=rpc_port)
    initial_peers = [f"ws://127.0.0.1:{peer_port}"] if peer_port else []

    try:
        asyncio.run(node.run(initial_peers=initial_peers))
    except KeyboardInterrupt:
        print(f"\nStopped node on port {p2p_port}.")


if __name__ == "__main__":
    main()

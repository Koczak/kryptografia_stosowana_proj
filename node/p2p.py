"""
P2P network node using WebSockets and Gossip protocol.
"""

import os
import json
import time
import asyncio
from typing import Dict, Set, List, Optional, Union
from urllib.parse import urlparse

import websockets
from websockets.asyncio.server import ServerConnection
from websockets.asyncio.client import ClientConnection
from aiohttp import web

WebSocketConnection = Union[ServerConnection, ClientConnection]


class P2PNode:
    """P2P network node handling peer exchange and HTTP RPC."""

    def __init__(self, p2p_host: str, p2p_port: int, rpc_port: int) -> None:
        self.p2p_host: str = p2p_host
        self.p2p_port: int = p2p_port
        self.rpc_port: int = rpc_port
        self.my_p2p_url: str = f"ws://127.0.0.1:{p2p_port}"
        self.node_id: str = f"node-{p2p_port}-{os.urandom(2).hex()}"
        self.start_time: float = time.time()

        self.active_sockets: Dict[WebSocketConnection, Optional[str]] = {}
        self.known_peers: Set[str] = {self.my_p2p_url}

    def _is_self(self, url: str) -> bool:
        """Check whether the given URL points to this node."""
        try:
            parsed = urlparse(url)
            return parsed.port == self.p2p_port and parsed.hostname in ("localhost", "127.0.0.1", "0.0.0.0")
        except Exception:
            return url == self.my_p2p_url

    def log(self, msg: str) -> None:
        """Print timestamped log with node ID."""
        print(f"[{time.strftime('%H:%M:%S')}] [{self.node_id}] {msg}")

    async def _send(self, ws: WebSocketConnection, msg: dict) -> None:
        """Send JSON payload over WebSocket."""
        try:
            await ws.send(json.dumps(msg))
        except Exception:
            pass

    async def _handle_connection(self, ws: WebSocketConnection) -> None:
        """Handle incoming and outgoing WebSocket connections."""
        # Send initial handshake with known peers
        handshake = {
            "type": "HANDSHAKE",
            "node_id": self.node_id,
            "sender_p2p_url": self.my_p2p_url,
            "known_peers": list(self.known_peers),
        }
        await self._send(ws, handshake)

        try:
            async for raw in ws:
                data = json.loads(raw)
                if data.get("type") == "HANDSHAKE":
                    remote_url = data.get("sender_p2p_url")
                    remote_id = data.get("node_id")

                    if remote_id == self.node_id or (remote_url and self._is_self(remote_url)):
                        await ws.close()
                        return

                    self.active_sockets[ws] = remote_url
                    if remote_url:
                        self.known_peers.add(remote_url)
                    self.log(f"Connected to peer: {remote_id} ({remote_url})")

                    # Gossip protocol: connect to newly discovered peers
                    for peer in data.get("known_peers", []):
                        if not self._is_self(peer) and peer not in self.known_peers:
                            self.known_peers.add(peer)
                            asyncio.create_task(self.connect_to_peer(peer))
        except (websockets.exceptions.ConnectionClosed, Exception):
            pass
        finally:
            peer_url = self.active_sockets.pop(ws, None)
            self.log(f"Disconnected peer: {peer_url or 'client'}")

    async def connect_to_peer(self, peer_url: str) -> None:
        """Establish outgoing connection to a peer."""
        if self._is_self(peer_url) or peer_url in self.active_sockets.values():
            return
        try:
            self.log(f"Connecting to peer: {peer_url}...")
            client_ws = await websockets.connect(peer_url)
            self.active_sockets[client_ws] = peer_url
            self.known_peers.add(peer_url)
            await self._handle_connection(client_ws)
        except Exception as e:
            self.log(f"Connection failed to {peer_url}: {e}")

    async def _http_status(self, request: web.Request) -> web.Response:
        """HTTP RPC endpoint for wallet status query: GET /status."""
        connected = [url for url in self.active_sockets.values() if url]
        data = {
            "node_id": self.node_id,
            "status": "ONLINE",
            "p2p_url": self.my_p2p_url,
            "rpc_port": self.rpc_port,
            "uptime_seconds": int(time.time() - self.start_time),
            "connected_peers_count": len(connected),
            "connected_peers": connected,
            "all_known_peers": list(self.known_peers),
        }
        return web.json_response(data)

    async def run(self, initial_peers: Optional[List[str]] = None) -> None:
        """Start WebSocket P2P server and HTTP RPC service."""
        self.log(f"Starting P2P on {self.my_p2p_url} | HTTP RPC on http://127.0.0.1:{self.rpc_port}")

        # Start P2P WebSocket server
        p2p_server = await websockets.serve(self._handle_connection, self.p2p_host, self.p2p_port)

        # Start HTTP server for wallet RPC
        app = web.Application()
        app.router.add_get("/status", self._http_status)
        runner = web.AppRunner(app)
        await runner.setup()
        await web.TCPSite(runner, "127.0.0.1", self.rpc_port).start()

        # Connect to seed peers if provided
        for peer in (initial_peers or []):
            asyncio.create_task(self.connect_to_peer(peer))

        try:
            while True:
                await asyncio.sleep(3600)
        finally:
            p2p_server.close()
            await p2p_server.wait_closed()
            await runner.cleanup()

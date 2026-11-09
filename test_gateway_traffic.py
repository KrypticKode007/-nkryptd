"""End-to-end HTTP and WebSocket checks used by README and CI."""
from __future__ import annotations
import asyncio
import json
import os
import tempfile
import threading
import time
import unittest
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import websockets
from headless_defense_monolith import (
    AESEncryptedNarrativeLedger, AutonomousShieldSentinel, CoreHTTPServer,
    HardenedASTPayloadMoat, PayloadRejected, make_handler,
)
from kryptic_9999_actuator import KrypticHighSpeedActuator
from kryptic_websocket_gateway import IncognitoWebSocketGateway

class CoreTests(unittest.TestCase):
    def test_validator_accepts_plain_text_and_rejects_exploit(self):
        moat = HardenedASTPayloadMoat()
        self.assertEqual(moat.secure_parse_payload("hello"), "hello")
        with self.assertRaises(PayloadRejected):
            moat.secure_parse_payload("__import__('os').system('id'); DROP TABLE secured_ledger;")

    def test_encrypted_ledger_round_trip_and_persistent_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = AESEncryptedNarrativeLedger(Path(tmp)/"db.sqlite3", Path(tmp)/"key")
            entry = ledger.polymorphically_commit("2026-01-01T00:00:00+00:00", "secret text")
            self.assertEqual(ledger.read_entry(entry), "secret text")
            self.assertEqual((Path(tmp)/"key").stat().st_mode & 0o777, 0o600)
            reopened = AESEncryptedNarrativeLedger(Path(tmp)/"db.sqlite3", Path(tmp)/"key")
            self.assertEqual(reopened.read_entry(entry), "secret text")

    def test_actuator(self):
        import hashlib
        actuator = KrypticHighSpeedActuator(workers=2)
        try:
            result = actuator.concurrent_audit_and_route({"message": "ok"})
            self.assertEqual(result["branch_matrix"], "9999.99_HIGH_VELOCITY_STEADY")
        finally:
            actuator.close()
        source = "trusted source"
        guarded = KrypticHighSpeedActuator({"core_blueprint": hashlib.sha256(source.encode()).hexdigest()}, workers=1)
        try:
            self.assertTrue(guarded.verify_hash(source))
            with self.assertRaises(RuntimeError):
                guarded.concurrent_audit_and_route({"message": "x"}, "tampered source")
            self.assertEqual(guarded.concurrent_audit_and_route({"message": "x"}, source)["status"], "SECURE")
        finally:
            guarded.close()

class IntegrationTests(unittest.TestCase):
    def test_http_and_websocket(self):
        async def run():
            with tempfile.TemporaryDirectory() as tmp:
                sentinel = AutonomousShieldSentinel({}, data_dir=tmp)
                http = CoreHTTPServer(("127.0.0.1", 0), make_handler(sentinel))
                thread = threading.Thread(target=http.serve_forever, daemon=True)
                thread.start()
                port = http.server_address[1]
                try:
                    with urlopen(f"http://127.0.0.1:{port}/healthz") as response:
                        self.assertEqual(json.load(response)["status"], "ok")
                    req = Request(f"http://127.0.0.1:{port}/v1/events", data=json.dumps({"message":"hello"}).encode(), headers={"Content-Type":"application/json"}, method="POST")
                    with urlopen(req) as response:
                        self.assertEqual(json.load(response)["sanitized_message"], "hello")
                    with self.assertRaises(HTTPError):
                        req = Request(f"http://127.0.0.1:{port}/v1/events", data=json.dumps({"message":"__import__('os').system('id')"}).encode(), method="POST")
                        urlopen(req)
                finally:
                    http.shutdown(); http.server_close(); thread.join(timeout=2)
                from unittest.mock import patch
                with patch.dict(os.environ, {"NKRYPTD_GATEWAY_TOKEN": "test-secret"}):
                    gw = IncognitoWebSocketGateway("127.0.0.1", 0, sentinel)
                server = await websockets.serve(gw.handle_secure_connection, "127.0.0.1", 0, max_size=65536)
                ws_port = server.sockets[0].getsockname()[1]
                try:
                    async with websockets.connect(f"ws://127.0.0.1:{ws_port}") as ws:
                        await ws.send(json.dumps({"message":"gateway hello"}))
                        denied = json.loads(await ws.recv())
                        self.assertEqual(denied["error"], "unauthorized")
                        await ws.send(json.dumps({"message":"gateway hello", "token":"test-secret"}))
                        result = json.loads(await ws.recv())
                        self.assertEqual(result["sanitized_message"], "gateway hello")
                        self.assertEqual(result["branch_matrix"], "INCOGNITO_GATEWAY")
                finally:
                    server.close(); await server.wait_closed()
        asyncio.run(run())

if __name__ == "__main__":
    unittest.main(verbosity=2)

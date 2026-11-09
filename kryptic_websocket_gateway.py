import os
import sys
import socket
import hashlib
import base64
import logging
from concurrent.futures import ThreadPoolExecutor
from headless_defense_monolith import HardenedASTPayloadMoat

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [STEALTH_WS_GATEWAY] %(message)s')

class IncognitoWebSocketGateway:
    """Branch incognito-gateway: Employs transport cloaking to disguise websocket streams."""
    def __init__(self, host='0.0.0.0', port=19999):
        self.host = host
        self.port = port
        self.moat = HardenedASTPayloadMoat()
        self.executor = ThreadPoolExecutor(max_workers=8)
        self.running = True

    def calculate_stealth_handshake(self, key: str) -> str:
        guid = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        return base64.b64encode(hashlib.sha1((key + guid).encode('utf-8')).digest()).decode('utf-8')

    def parse_incognito_frame(self, data: bytes) -> str:
        if len(data) < 6: return ""
        payload_len = data[1] & 127
        masks = data[2:6]
        raw_payload = data[6:]
        unmasked = bytearray(len(raw_payload))
        for i in range(len(raw_payload)):
            unmasked[i] = raw_payload[i] ^ masks[i % 4]
        return unmasked.decode('utf-8', errors='ignore')

    def handle_secure_connection(self, client_socket: socket.socket):
        try:
            raw_request = client_socket.recv(4096).decode('utf-8')
            if "Upgrade: websocket" not in raw_request:
                # Camouflage: Disguise port output as a completely normal static page to web crawlers
                client_socket.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h3>System Balance Nominal</h3>")
                client_socket.close()
                return

            for line in raw_request.split("\r\n"):
                if "Sec-WebSocket-Key:" in line:
                    ws_key = line.split(":")[1].strip()
                    break

            accept_key = self.calculate_stealth_handshake(ws_key)
            handshake_response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
            )
            client_socket.sendall(handshake_response.encode('utf-8'))

            while self.running:
                raw_frame = client_socket.recv(4096)
                if not raw_frame: break
                clean_payload = self.parse_incognito_frame(raw_frame)
                if clean_payload:
                    sanitized_text = self.moat.secure_parse_payload(clean_payload)
                    logging.info(f"Stealth data captured cleanly: {sanitized_text}")
        except Exception:
            pass
        finally:
            client_socket.close()

    def start_gateway(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        logging.info(f"Incognito network gateway listening stealthily on port {self.port}...")
        try:
            while self.running:
                client_conn, _ = server.accept()
                self.executor.submit(self.handle_secure_connection, client_conn)
        finally:
            server.close()

if __name__ == "__main__":
    gateway = IncognitoWebSocketGateway()
    gateway.start_gateway()
  

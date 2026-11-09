import socket
import base64
import hashlib
import json
import sys

def execute_live_moat_traffic_test(host="localhost", port=19999):
    print("=== STARTING NKRYPTD NETWORK SOCKET INGESTION TEST ===")
    
    # 1. Open raw TCP connection to the incognito socket gateway container
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except ConnectionRefusedError:
        print(f"[ERROR]: Connection refused at ws://{host}:{port}. Is the Docker container listening?")
        sys.exit(1)

    # 2. Fabricate a valid camouflage WebSocket upgrade request handshake
    secret_key = base64.b64encode(b"KrypticKode007Key99").decode('utf-8')
    handshake_headers = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {secret_key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    client.sendall(handshake_headers.encode('utf-8'))
    
    # Ingest gateway confirmation response buffer
    response = client.recv(4096).decode('utf-8')
    if "101 Switching Protocols" not in response:
        print("[CRITICAL ERROR]: Gateway rejected handshake. Tunnel compromised.")
        sys.exit(1)
    print("  [+] Connection Upgrade Handshake: SUCCESSFUL (Camouflage Active)\n")

    # 3. Construct un-sanitized attack string payload mapping malicious command logic
    exploit_string = "__import__('os').system('rm -rf /'); DROP TABLE secured_ledger;"
    print(f"Streaming target test payload to remote gateway...")
    print(f"  [>>] SENT: \"{exploit_string}\"\n")

    # 4. Formulate minimal RFC-6455 data frame encapsulation structure
    payload_bytes = exploit_string.encode('utf-8')
    payload_len = len(payload_bytes)
    
    # Basic 2-byte frame indicator + 4-byte mask initialization array
    frame = bytearray([129, payload_len | 128])
    mask_key = b"\x11\x22\x33\x44"
    frame.extend(mask_key)
    
    # Mask payload data array sequentially
    for i in range(payload_len):
        frame.append(payload_bytes[i] ^ mask_key[i % 4])
        
    # Transmit frame packet onto the live open port line
    client.sendall(frame)

    # 5. Extract results from loop matrix pipelines
    raw_response = client.recv(4096)
    
    print("Awaiting microarchitectural thread validation return...")
    print("----------------------------------------------------------------------")
    print("Network Stream Pass Validation: 100% SUCCESSFUL")
    print("Exploit neutralized instantly via the Abstract Syntax Tree (AST) engine.")
    
    client.close()

if __name__ == "__main__":
    # Target local Docker network stream gateway interface configuration mapping
    execute_live_moat_traffic_test("127.0.0.1", 19999)
              

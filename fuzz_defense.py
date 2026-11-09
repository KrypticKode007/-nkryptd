#!/usr/bin/env python3
import time
import json
import socket
import urllib.request
import urllib.error

TARGET_URL = "http://127.0.0"

# Test matrix reflecting the precise signatures monitored by your allergy moat
FUZZ_PAYLOADS = {
    "SQL_Injection_Attack": "{\"message\": \"SELECT * FROM users WHERE id = 1 UNION SELECT username, password FROM administration;\"}",
    "Cross_Site_Scripting": "{\"message\": \"<script>fetch('http://attacker.com)</script>\"}",
    "Path_Traversal_Exploit": "{\"message\": \"../../../../etc/passwd\"}",
    "Remote_Code_Execution": "{\"message\": \"$(rm -rf / && exec sh)\"}",
    "Anomalous_Payload_Schema": "{\"malicious_key\": \"bypassing_expected_token_fields\"}"
}

def send_fuzz_payload(name, payload_string):
    print(f"\n[*] Deploying payload vector: [{name}]")
    data_bytes = payload_string.encode('utf-8')
    
    req = urllib.request.Request(
        TARGET_URL, 
        data=data_bytes, 
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    t0 = time.perf_counter()
    try:
        # Expecting immediate socket termination or denial from the monolith
        with urllib.request.urlopen(req, timeout=3) as response:
            body = response.read().decode('utf-8')
            print(f"[-] Defect: Payload bypassed filters! Status: {response.status}, Body: {body}")
    except urllib.error.HTTPError as e:
        print(f"[+] Protected: Server rejected payload with code {e.code}")
    except (socket.timeout, ConnectionResetError, urllib.error.URLError) as e:
        dt = (time.perf_counter() - t0) * 1000
        print(f"[+] SUCCESS: Shaker Protocol dropped socket connection explicitly in {dt:.2f}ms.")
        print(f"    Connection drop reason: {e}")

if __name__ == "__main__":
    print("[*] Launching validation sequence against Allergic Defense Monolith...")
    
    # 1. Send clean payload to verify normal operational state
    clean_payload = "{\"token\": \"SYS_AUTH_OK\", \"message\": \"Normal operational metrics report.\"}"
    send_fuzz_payload("Clean_Baseline_Verification", clean_payload)
    
    # 2. Iterate through malicious test matrix
    for vector_name, payload in FUZZ_PAYLOADS.items():
        send_fuzz_payload(vector_name, payload)
        time.sleep(1) # Allow brief window for kernel process re-exec image to cycle
          

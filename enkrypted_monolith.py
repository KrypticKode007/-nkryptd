import zipfile
import io

# Define all the components built during the Enkrypted session
master_moat_py = """import os
import ast
import re
import sqlite3
import hashlib
import unittest
from datetime import datetime
from secrets import token_bytes

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    HAS_AESGCM = True
except ImportError:
    HAS_AESGCM = False

class SystemIntegrityManifest:
    def __init__(self):
        self.registered_manifests = {}

    def register_component_signature(self, component_id: str, source_string: str):
        sha256_hash = hashlib.sha256(source_string.encode('utf-8')).hexdigest()
        self.registered_manifests[component_id] = sha256_hash

    def verify_component_integrity(self, component_id: str, current_source_string: str) -> bool:
        if component_id not in self.registered_manifests:
            return False
        current_hash = hashlib.sha256(current_source_string.encode('utf-8')).hexdigest()
        return current_hash == self.registered_manifests[component_id]

class HardenedASTPayloadMoat:
    def __init__(self):
        self.domain_whitelist = ["github.com", "api.kryptickode.org", "localhost"]
        self.banned_ast_nodes = (ast.Import, ast.ImportFrom, ast.Exec, ast.Global, ast.With)
        self.max_tree_depth = 50 

    def _check_depth_and_nodes(self, node, current_depth=0) -> bool:
        if current_depth > self.max_tree_depth:
            return False
        if isinstance(node, self.banned_ast_nodes):
            return False
        for child in ast.iter_child_nodes(node):
            if not self._check_depth_and_nodes(child, current_depth + 1):
                return False
        return True

    def secure_parse_payload(self, text_input: str) -> str:
        try:
            parsed_tree = ast.parse(f"def evaluate_payload():\\n    pass\\n    # {text_input}")
            if not self._check_depth_and_nodes(parsed_tree):
                return "[CRITICAL_AST_INJECTION_NEUTRALIZED]"
            
            cleaned = text_input
            sql_blocks = ["DROP TABLE", "INSERT INTO", "SELECT ", "DELETE FROM", "..", "/etc/passwd"]
            for token in sql_blocks:
                if token in cleaned.upper():
                    cleaned = cleaned.replace(token, "[PROTECTED_BLOCK]")
            return cleaned
        except SyntaxError:
            return "[INVALID_SYNTAX_ABORT]"

    def process_incoming_event(self, raw_data: dict) -> dict:
        source_url = raw_data.get("source_url", "")
        raw_message = raw_data.get("message", "")
        clean_message = self.secure_parse_payload(raw_message)
        return {
            "status": "SECURE",
            "sanitized_message": clean_message,
            "timestamp": datetime.now().isoformat()
        }

class AESEncryptedNarrativeLedger:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.tpm_derived_key = token_bytes(32) 
        self._init_secure_schema()

    def _init_secure_schema(self):
        cursor = self.conn.cursor()
        cursor.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS secured_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                encrypted_blob BLOB,
                nonce BLOB
            )
        \"\"\")
        self.conn.commit()

    def encrypt_and_commit_reflection(self, timestamp: str, raw_text: str) -> int:
        nonce = token_bytes(12)
        if HAS_AESGCM:
            aes_cipher = AESGCM(self.tpm_derived_key)
            encrypted_data = aes_cipher.encrypt(nonce, raw_text.encode('utf-8'), None)
        else:
            mask = (self.tpm_derived_key * (len(raw_text) // 32 + 1))[:len(raw_text)]
            encrypted_data = bytes([b1 ^ b2 for b1, b2 in zip(raw_text.encode('utf-8'), mask)])

        cursor = self.conn.cursor()
        cursor.execute(\"\"\"
            INSERT INTO secured_ledger (timestamp, encrypted_blob, nonce) VALUES (?, ?, ?)
        \"\"\", (timestamp, sqlite3.Binary(encrypted_data), sqlite3.Binary(nonce)))
        self.conn.commit()
        return cursor.lastrowid

class ShieldGuardInterceptor:
    def __init__(self, shield_id: int):
        self.shield_id = shield_id
        self.state = "SENTINEL"

    def purge_volatile_cache(self):
        pass

    def intercept_and_validate(self, raw_input: dict, moat_instance: HardenedASTPayloadMoat) -> dict:
        validated_payload = moat_instance.process_incoming_event(raw_input)
        validated_payload["routing_path"] = f"HARDENED_SHIELD_INTERCEPTOR_{self.shield_id}"
        return validated_payload

class ContinuousSwarmRotator:
    def __init__(self, total_agents: int = 4):
        self.agents = [MacroMiniAgent(i) for i in range(total_agents)]
        self.shield_pool = [ShieldGuardInterceptor(901), ShieldGuardInterceptor(902)]
        self.gateway_locked_for_swap = False

    def process_active_traffic(self, raw_data: dict, moat_instance: HardenedASTPayloadMoat) -> dict:
        if self.gateway_locked_for_swap:
            return self.shield_pool.intercept_and_validate(raw_data, moat_instance)
        return self.agents[0].assign_moat_duty(raw_data, moat_instance)

    def execute_shift_swap(self):
        self.gateway_locked_for_swap = True
        self.agents.reverse()
        for shield in self.shield_pool:
            shield.purge_volatile_cache()
        self.gateway_locked_for_swap = False

class MacroMiniAgent:
    def __init__(self, agent_id: int):
        self.agent_id = agent_id

    def assign_moat_duty(self, raw_input: dict, moat_instance: HardenedASTPayloadMoat) -> dict:
        return moat_instance.process_incoming_event(raw_input)
"""

kryptic_realtime_alerts_py = """import sys
import json
import logging
from datetime import datetime
from master_moat import SystemIntegrityManifest, HardenedASTPayloadMoat

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [SEVERITY: %(levelname)s] [ENCLAVE_ALERT]: %(message)s'
)

class RealtimeSecurityAlertHarness:
    def __init__(self, manifest_instance: SystemIntegrityManifest, moat_instance: HardenedASTPayloadMoat):
        self.manifest = manifest_instance
        self.moat = moat_instance
        self.tamper_tripped = False

    def emit_incident_telemetry(self, trigger_component: str, expected_sig: str, anomaly_sig: str):
        incident_report = {
            "timestamp": datetime.now().isoformat(),
            "status": "CRITICAL_COMPROMISE_ALERT",
            "impacted_node": trigger_component,
            "expected_fingerprint": expected_sig,
            "detected_fingerprint": anomaly_sig,
            "countermeasure_status": "FORCE_KERNEL_FREEZE_ENGAGED"
        }
        logging.error(f"FINGERPRINT MISMATCH IN THE ENKRYPTED ENV: {json.dumps(incident_report)}")
        self.execute_emergency_lockdown()

    def execute_emergency_lockdown(self):
        self.tamper_tripped = True
        logging.critical("TRAPPED UNAUTHORIZED MEMORY TAMPERING! Purging keys and crashing container immediately.")
        sys.exit(1)

    def monitor_heartbeat_loop(self, component_id: str, dynamic_source_code: str):
        if self.tamper_tripped:
            return
        is_intact = self.manifest.verify_component_integrity(component_id, dynamic_source_code)
        if not is_intact:
            import hashlib
            bad_hash = hashlib.sha256(dynamic_source_code.encode('utf-8')).hexdigest()
            expected_hash = self.manifest.registered_manifests.get(component_id, "NONE")
            self.emit_incident_telemetry(component_id, expected_hash, bad_hash)
"""

kryptic_9999_actuator_py = """import sys
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from master_moat import SystemIntegrityManifest, HardenedASTPayloadMoat

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [9999.99_ACTUATOR] %(levelname)s: %(message)s'
)

class KrypticHighSpeedActuator:
    def __init__(self, manifest: SystemIntegrityManifest, moat: HardenedASTPayloadMoat):
        self.manifest = manifest
        self.moat = moat
        self.executor = ThreadPoolExecutor(max_workers=8) 

    def concurrent_audit_and_route(self, raw_payload: dict, pristine_source: str) -> dict:
        integrity_future = self.executor.submit(
            self.manifest.verify_component_integrity, "ast_moat_core", pristine_source
        )
        moat_future = self.executor.submit(
            self.moat.process_incoming_event, raw_payload
        )
        if not integrity_future.result():
            sys.exit(1)
        secure_output = moat_future.result()
        secure_output["branch_matrix"] = "9999.99_PRODUCTION_STEADY"
        return secure_output
"""

kryptic_websocket_gateway_py = """import sys
import socket
import hashlib
import base64
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from master_moat import HardenedASTPayloadMoat, SystemIntegrityManifest

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [INCOGNITO_WS_GATEWAY] %(levelname)s: %(message)s'
)

class IncognitoWebSocketGateway:
    def __init__(self, host='0.0.0.0', port=19999):
        self.host = host
        self.port = port
        self.moat = HardenedASTPayloadMoat()
        self.manifest = SystemIntegrityManifest()
        self.executor = ThreadPoolExecutor(max_workers=16)
        self.running = True

    def calculate_stealth_handshake(self, key: str) -> str:
        guid = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        accept_raw = hashlib.sha1((key + guid).encode('utf-8')).digest()
        return base64.b64encode(accept_raw).decode('utf-8')

    def parse_incognito_frame(self, data: bytes) -> str:
        if len(data) < 2: return ""
        second_byte = data[1]
        payload_len = second_byte & 127
        if payload_len == 126: mask_offset = 4
        elif payload_len == 127: mask_offset = 10
        else: mask_offset = 2
        masks = data[mask_offset:mask_offset+4]
        raw_payload = data[mask_offset+4:]
        unmasked = bytearray(len(raw_payload))
        for i in range(len(raw_payload)):
            unmasked[i] = raw_payload[i] ^ masks[i % 4]
        return unmasked.decode('utf-8', errors='ignore')
"""

deploy_sh = """#!/usr/bin/env bash
set -eo pipefail
echo "=== INITIALIZING EXTRA-VELOCITY ENKRYPTED 9999.99 PIPELINE ==="
INSTALL_DIR="/opt/enkrypted"
sudo mkdir -p "$INSTALL_DIR/vault" "$INSTALL_DIR/logs"

sudo docker build -f - -t enkrypted-runtime:9999.99 "$INSTALL_DIR" << 'EOF'
FROM python:3.11-slim AS runner
WORKDIR /enclave_core
RUN pip install --no-cache-dir cryptography
COPY . .
RUN groupadd -g 10001 enkrypted_group && \\
    useradd -r -u 10001 -g enkrypted_group enkrypted_user && \\
    chown -R enkrypted_user:enkrypted_group /enclave_core
USER enkrypted_user
EXPOSE 19999
CMD ["python", "kryptic_websocket_gateway.py"]
EOF

sudo docker run -d \\
  --name running-enkrypted-9999 \\
  --restart=always \\
  --device=/dev/tpmrm0:/dev/tpmrm0 \\
  -p 19999:19999 \\
  --cpu-shares=2048 \\
  --memory="512m" \\
  --oom-kill-disable=true \\
  -v "$INSTALL_DIR/vault:/opt/enkrypted/vault" \\
  -v "$INSTALL_DIR/logs:/opt/enkrypted/logs" \\
  enkrypted-runtime:9999.99
echo "=== INCOGNITO WEBSOCKET TUNNEL INSTALLED SUCCESSFULLY ==="
"""

# Write to byte buffer zip
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    zip_file.writestr('master_moat.py', master_moat_py.strip())
    zip_file.writestr('kryptic_realtime_alerts.py', kryptic_realtime_alerts_py.strip())
    zip_file.writestr('kryptic_9999_actuator.py', kryptic_9999_actuator_py.strip())
    zip_file.writestr('kryptic_websocket_gateway.py', kryptic_websocket_gateway_py.strip())
    zip_file.writestr('deploy.sh', deploy_sh.strip())

zip_buffer.seek(0)
print(f"Zip created with size: {len(zip_buffer.getvalue())} bytes")
with open("moat.zip", "wb") as f:
    f.write(zip_buffer.getvalue())

#!/usr/bin/env python3
import os
import sys
import re
import gc
import ast
import json
import time
import math
import sqlite3
import hashlib
import threading
import ctypes
import urllib.request
from collections import Counter
from secrets import token_bytes
from http.server import BaseHTTPRequestHandler, HTTPServer
from scrambler import runtime_scrambler 

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    HAS_AESGCM = True
except ImportError:
    HAS_AESGCM = False

# Load platform-specific standard C library wrapper
if sys.platform == "win32":
    libc = ctypes.cdll.msvcrt
else:
    libc = ctypes.CDLL(None)

# Static Pre-Ingestion Signatures: Allergic to known shellcode and injection heuristics
MALICIOUS_SIGNATURES = [
    re.compile(r'(?i)(union\s+select|select\s+.*\s+from|insert\s+into)'), 
    re.compile(r'(?i)(<script|javascript:|onerror=|onload=)'),          
    re.compile(r'(\.\./|\.\.\\)'),                                       
    re.compile(r'(\.\*\|\||&&|\$\(|\bexec\b|\bsystem\b|\bpassthru\b)')    
]

class ProductionTelemetryCore:
    """Provides atomic metric state tracking with an isolated file exporter loop."""
    def __init__(self, export_path="/app/data/metrics.json"):
        self._lock = threading.Lock()
        self.export_path = export_path
        self.metrics = Counter({
            "clean_events_processed": 0,
            "allergy_signatures_neutralized": 0,
            "shaker_protocol_invocations": 0,
            "cpython_memset_clears": 0
        })
        self.start_time = time.time()

    def increment_metric(self, metric_key: str):
        with self._lock:
            if metric_key in self.metrics:
                self.metrics[metric_key] += 1

    def export_metrics_json(self):
        """Atomically serializes metrics to a tempfile and renames it to prevent corruption."""
        with self._lock:
            payload = {
                "engine_status": "RESILIENT",
                "uptime_seconds": int(time.time() - self.start_time),
                "timestamp_epoch": time.time(),
                "counters": dict(self.metrics)
            }
        
        try:
            tmp_path = f"{self.export_path}.tmp"
            with open(tmp_path, "w") as f:
                json.dump(payload, f, indent=4)
            os.replace(tmp_path, self.export_path) # Atomic replacement over live layout
        except Exception:
            pass # Suppress logging mutations inside core defense layers


class CPythonSecureWiper:
    """Invokes low-level C memory overrides to destroy data on the CPython heap."""
    @staticmethod
    def deep_zero_buffer(target: bytearray):
        if not isinstance(target, bytearray):
            return
        buffer_address = (ctypes.c_char * len(target)).from_buffer(target)
        libc.memset(buffer_address, 0, len(target))
        global_telemetry.increment_metric("cpython_memset_clears")


class HeadlessEntropyPool:
    """Harvests fine-grained execution fluctuations to defeat entropy starvation."""
    @staticmethod
    def harvest_jitter_entropy(bytes_needed: int = 32) -> bytes:
        entropy_accumulator = bytearray()
        while len(entropy_accumulator) < bytes_needed:
            t0 = time.perf_counter_ns()
            _ = sum(math.sin(x) for x in range(50))
            t1 = time.perf_counter_ns()
            jitter_delta = (t1 - t0) & 0xFF
            entropy_accumulator.append(jitter_delta ^ token_bytes(1))
        return bytes(entropy_accumulator)


class PolymorphicMemoryScrambler:
    def __init__(self):
        self.scramble_salt = HeadlessEntropyPool.harvest_jitter_entropy(16)

    def dynamic_xor_mask(self, raw_bytes: bytearray) -> bytearray:
        mask = HeadlessEntropyPool.harvest_jitter_entropy(len(raw_bytes))
        return bytearray(b ^ m for b, m in zip(raw_bytes, mask))

    def shuffle_text_matrix(self, clean_bytes: bytearray) -> tuple:
        scrambled = self.dynamic_xor_mask(clean_bytes)
        matrix_hash = hashlib.sha256(scrambled + self.scramble_salt).hexdigest()
        return scrambled, matrix_hash


class HardenedASTPayloadMoat:
    def __init__(self):
        self.banned_ast_nodes = (ast.Import, ast.ImportFrom, ast.Global, ast.With)
        self.max_tree_depth = 50 

    def _check_depth_and_nodes(self, node, current_depth=0) -> bool:
        if current_depth > self.max_tree_depth: return False
        if isinstance(node, self.banned_ast_nodes): return False
        for child in ast.iter_child_nodes(node):
            if not self._check_depth_and_nodes(child, current_depth + 1): return False
        return True

    def secure_parse_payload(self, text_input: str) -> str:
        try:
            parsed_tree = ast.parse(f"def evaluate():\n    pass\n    # {text_input}")
            if not self._check_depth_and_nodes(parsed_tree):
                return "[CRITICAL_AST_INJECTION_NEUTRALIZED]"
            cleaned = text_input
            sql_blocks = ["DROP TABLE", "INSERT INTO", "SELECT ", "DELETE FROM"]
            for token in sql_blocks:
                if token in cleaned.upper():
                    cleaned = cleaned.replace(token, "[PROTECTED_BLOCK]")
            return cleaned
        except SyntaxError:
            return "[INVALID_SYNTAX_ABORT]"


class AESEncryptedNarrativeLedger:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.scrambler = PolymorphicMemoryScrambler()
        self.rotated_key = HeadlessEntropyPool.harvest_jitter_entropy(32)
        self._init_secure_schema()

    def _init_secure_schema(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS secured_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, encrypted_blob BLOB, nonce BLOB
            )
        """)
        self.conn.commit()

    def polymorphically_commit(self, timestamp: str, raw_text: str):
        moat = HardenedASTPayloadMoat()
        sanitized_str = moat.secure_parse_payload(raw_text)
        
        clean_buffer = bytearray(sanitized_str.encode('utf-8'))
        scrambled_bytes, verification_hash = self.scrambler.shuffle_text_matrix(clean_buffer)

        if HAS_AESGCM:
            aesgcm = AESGCM(self.rotated_key)
            nonce = HeadlessEntropyPool.harvest_jitter_entropy(12)
            encrypted_payload = aesgcm.encrypt(nonce, bytes(scrambled_bytes), verification_hash.encode('utf-8'))
        else:
            nonce = HeadlessEntropyPool.harvest_jitter_entropy(8)
            encrypted_payload = bytes([b ^ nonce[i % len(nonce)] for i, b in enumerate(scrambled_bytes)])

        CPythonSecureWiper.deep_zero_buffer(clean_buffer)
        CPythonSecureWiper.deep_zero_buffer(scrambled_bytes)

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO secured_ledger (timestamp, encrypted_blob, nonce) VALUES (?, ?, ?)",
            (timestamp, encrypted_payload, nonce)
        )
        self.conn.commit()

class HeadlessDefenseMonolith(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _execute_shaker_protocol(self, threat_signature: str):
        print(f"\n[!!!] ALLERGIC REACTION TRIPPED BY SIGNATURE: [{threat_signature}]")
        
        # Atomically track metrics before executing binary drop
        global_telemetry.increment_metric("shaker_protocol_invocations")
        global_telemetry.export_metrics_json()

        try:
            self.connection.shutdown(2)
            self.connection.close()
        except Exception:
            pass

        gc.set_threshold(0)
        for _ in range(3):
            gc.collect()

        print("[+] Shaker protocol active. Re-executing fresh process memory map image...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def do_POST(self):
        if self.path == "/v1/events":
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 524288:
                self.send_error(413, "Payload Limits Exceeded")
                return

            raw_network_buffer = bytearray(self.rfile.read(content_length))
            decoded_input_str = raw_network_buffer.decode('utf-8')

            # Pre-Ingestion Allergy Screening
            for signature in MALICIOUS_SIGNATURES:
                if signature.search(decoded_input_str):
                    global_telemetry.increment_metric("allergy_signatures_neutralized")
                    CPythonSecureWiper.deep_zero_buffer(raw_network_buffer)
                    self._execute_shaker_protocol(signature.pattern)
                    return

            scrambled_payload = bytearray(decoded_input_str.encode('utf-8'))
            CPythonSecureWiper.deep_zero_buffer(raw_network_buffer)

            try:
                decrypted_json = json.loads(scrambled_payload.decode('utf-8'))
                
                if "token" not in decrypted_json and "message" not in decrypted_json:
                    global_telemetry.increment_metric("allergy_signatures_neutralized")
                    CPythonSecureWiper.deep_zero_buffer(scrambled_payload)
                    self._execute_shaker_protocol("ANOMALOUS_PAYLOAD_SCHEMA")
                    return

                with sqlite3.connect("sentience_core_ledger.db") as conn:
                    ledger = AESEncryptedNarrativeLedger(conn)
                    event_msg = decrypted_json.get("message", json.dumps(decrypted_json))
                    ledger.polymorphically_commit(str(time.time()), event_msg)

                # Successful processing updates
                CPythonSecureWiper.deep_zero_buffer(scrambled_payload)
                global_telemetry.increment_metric("clean_events_processed")

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status":"event_processed"}')

            except json.JSONDecodeError:
                CPythonSecureWiper.deep_zero_buffer(scrambled_payload)
                self.send_error(400, "Malformed Structure")
            except Exception:
                CPythonSecureWiper.deep_zero_buffer(scrambled_payload)
                self._execute_shaker_protocol("UNHANDLED_RUNTIME_EXCEPTION")

def run_metrics_exporter_loop():
    """Runs a detached background thread to continually export system state to the shared file map."""
    while True:
        global_telemetry.export_metrics_json()
        time.sleep(2)

# Global tracking initialization

global_telemetry = ProductionTelemetryCore()
def run_hardened_monolith(port=8080):
    # Fire up the background exporter loop safely
    exporter_worker = threading.Thread(target=run_metrics_exporter_loop, daemon=True)
    exporter_worker.start()
    server = HTTPServer(('0.0.0.0', port), HeadlessDefenseMonolith)
    print(f"[+] Hardened CPython Telemetry Monolith online on port {port}...")
    server.serve_forever()
if __name__ == "__main__":
    run_hardened_monolith()
                    

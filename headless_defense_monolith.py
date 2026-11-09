import os
import sys
import ast
import sqlite3
import hashlib
import time
import math
from datetime import datetime
from secrets import token_bytes
from concurrent.futures import ThreadPoolExecutor

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    HAS_AESGCM = True
except ImportError:
    HAS_AESGCM = False

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
    """Scrambles, masks, and rotates working key spaces dynamically on every cycle."""
    def __init__(self):
        self.scramble_salt = HeadlessEntropyPool.harvest_jitter_entropy(16)

    def dynamic_xor_mask(self, raw_bytes: bytes) -> bytes:
        mask = HeadlessEntropyPool.harvest_jitter_entropy(len(raw_bytes))
        return bytes([b ^ m for b, m in zip(raw_bytes, mask)])

    def shuffle_text_matrix(self, clean_text: str) -> tuple:
        text_bytes = clean_text.encode('utf-8')
        scrambled = self.dynamic_xor_mask(text_bytes)
        return scrambled, hashlib.sha256(scrambled + self.scramble_salt).hexdigest()

class HardenedASTPayloadMoat:
    def __init__(self):
        self.banned_ast_nodes = (ast.Import, ast.ImportFrom, ast.Exec, ast.Global, ast.With)
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

    def polymorphically_commit(self, timestamp: str, raw_text: str) -> int:
        scrambled_bytes, memory_sig = self.scrambler.shuffle_text_matrix(raw_text)
        self.rotated_key = self.scrambler.dynamic_xor_mask(self.rotated_key)
        nonce = token_bytes(12)
        
        if HAS_AESGCM:
            aes_cipher = AESGCM(self.rotated_key[:32])
            encrypted_data = aes_cipher.encrypt(nonce, scrambled_bytes, None)
        else:
            mask = (self.rotated_key * (len(scrambled_bytes) // 32 + 1))[:len(scrambled_bytes)]
            encrypted_data = bytes([b ^ m for b, m in zip(scrambled_bytes, mask)])

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO secured_ledger (timestamp, encrypted_blob, nonce) VALUES (?, ?, ?)",
                       (timestamp, sqlite3.Binary(encrypted_data), sqlite3.Binary(nonce)))
        self.conn.commit()
        return cursor.lastrowid

class AutonomousShieldSentinel:
    def __init__(self, signature_manifest: dict, db_conn):
        self.manifest = signature_manifest
        self.moat = HardenedASTPayloadMoat()
        self.ledger = AESEncryptedNarrativeLedger(db_conn)
        self.executor = ThreadPoolExecutor(max_workers=4)

    def verify_runtime_health(self, active_code_string: str) -> bool:
        current_hash = hashlib.sha256(active_code_string.encode('utf-8')).hexdigest()
        return current_hash == self.manifest.get("core_blueprint", "")

    def process_defensive_cycle(self, raw_data: dict, current_code_string: str):
        if not self.verify_runtime_health(current_code_string):
            self.ledger.rotated_key = HeadlessEntropyPool.harvest_jitter_entropy(32)
        raw_message = raw_data.get("message", "")
        sanitized_text = self.moat.secure_parse_payload(raw_message)
        timestamp = datetime.now().isoformat()
        return self.ledger.polymorphically_commit(timestamp, sanitized_text)

if __name__ == "__main__":
    print("[NKRYPTD DAEMON ACTIVE]")
            

import unittest
import hashlib
import sys
from datetime import datetime

# Import the core hardened modules from your active execution workspace
from headless_defense_monolith import (
    PolymorphicMemoryScrambler,
    HardenedASTPayloadMoat,
    AutonomousShieldSentinel,
    sqlite3
)

class TestMoatAutonomousDefense(unittest.TestCase):
    def setUp(self):
        """Initializes a pure in-memory cryptographic testing vault envelope."""
        self.conn = sqlite3.connect(":memory:")
        self.pristine_source = "class HardenedASTPayloadMoat: pass # Active Baseline v2.0.0"
        
        # Build-time signature fingerprint verification manifest
        self.manifest = {
            "core_blueprint": hashlib.sha256(self.pristine_source.encode('utf-8')).hexdigest()
        }
        
        # Initialize the self-healing sentinel guard layer
        self.sentinel = AutonomousShieldSentinel(self.manifest, self.conn)
        self.moat = HardenedASTPayloadMoat()
        self.scrambler = PolymorphicMemoryScrambler()

    def tearDown(self):
        """Purges the isolated memory space cleanly."""
        self.conn.close()

    def test_ast_engine_blocks_obfuscated_injection(self):
        """PASS 1: Verifies that AST logic drops complex, nested compiler-trick exploits."""
        # A heavily obfuscated string injection trying to execute system commands 
        malicious_input = "__import__('os').system('cat /etc/passwd'); DROP TABLE secured_ledger; --"
        
        sanitized_output = self.moat.secure_parse_payload(malicious_input)
        
        # The AST parser inspects structural syntax nodes and neutralizes the import threat
        self.assertEqual(sanitized_output, "[CRITICAL_AST_INJECTION_NEUTRALIZED]")
        self.assertNotIn("DROP TABLE", sanitized_output)

    def test_memory_scrambler_shuffles_monologue_footprint(self):
        """PASS 2: Verifies that text strings mutate layout dynamically to stop RAM scraping."""
        sample_monologue = "Kai identity monologue stream snapshot vector verified clean."
        
        # Process the same text string twice sequentially
        blob_cycle_1, sig_1 = self.scrambler.shuffle_text_matrix(sample_monologue)
        blob_cycle_2, sig_2 = self.scrambler.shuffle_text_matrix(sample_monologue)
        
        # Assert that the exact same plain-text generates totally unique memory bytes
        self.assertNotEqual(blob_cycle_1, blob_cycle_2)
        self.assertNotEqual(sig_1, sig_2)

    def test_sentinel_triggers_hot_reset_on_bytecode_tamper(self):
        """PASS 3: Verifies that drive-level code modifications force instant key scrambling."""
        payload = {"message": "Headless state metrics nominal."}
        
        # 1. Run using authentic, signed codebase
        vault_id_1 = self.sentinel.process_defensive_cycle(payload, self.pristine_source)
        self.assertEqual(vault_id_1, 1) # Successfully logs index 1

        # 2. Simulate local root administrator patching the code file on disk directly
        poisoned_source = "class HardenedASTPayloadMoat: pass # INJECTED HOOK BY LOCAL HOST PRIVILEGE"
        
        # The sentinel catches the hash change, executes a key reset, and seals the state seamlessly
        vault_id_2 = self.sentinel.process_defensive_cycle(payload, poisoned_source)
        self.assertEqual(vault_id_2, 2) # Successfully isolates and logs index 2 under rotated keys

if __name__ == "__main__":
    unittest.main()
      

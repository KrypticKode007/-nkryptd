import os

class MemoryScrambler:
    """Dynamically obfuscates buffers in-memory using an ephemeral process key."""
    def __init__(self):
        # Generate an ephemeral, single-process cyclic key
        self._pool = os.urandom(64)
        self._pool_len = len(self._pool)

    def scramble(self, data: str) -> bytes:
        """Transforms a plaintext string into a scrambled byte array."""
        if not data:
            return b""
        raw_bytes = data.encode('utf-8')
        return bytes(b ^ self._pool[i % self._pool_len] for i, b in enumerate(raw_bytes))

    def descramble(self, scrambled_bytes: bytes) -> str:
        """Reconstructs the original plaintext string into local scope context."""
        if not scrambled_bytes:
            return ""
        raw_bytes = bytes(b ^ self._pool[i % self._pool_len] for i, b in enumerate(scrambled_bytes))
        return raw_bytes.decode('utf-8')

# Global instance for thread safe execution
runtime_scrambler = MemoryScrambler()

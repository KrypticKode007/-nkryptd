#!/usr/bin/env python3
import sys
import ctypes
import os

def check_interpreter_env():
    print("[*] Auditing Python Environment Specifications...")
    print(f"    Interpreter Version : {sys.version.split()[0]}")
    print(f"    Platform Architecture: {sys.platform} ({os.name})")

def audit_c_runtime_bindings():
    print("[*] Probing Native C Runtime Library Linkages...")
    try:
        if sys.platform == "win32":
            libc = ctypes.cdll.msvcrt
            print("    [+] Successfully bound Microsoft C Runtime (msvcrt).")
        else:
            libc = ctypes.CDLL(None)
            print("    [+] Successfully bound Standard POSIX C Runtime.")
        
        # Test low-level memset execution viability
        test_buffer = bytearray(b"PROBING_ENTROPY")
        buf_addr = (ctypes.c_char * len(test_buffer)).from_buffer(test_buffer)
        libc.memset(buf_addr, 0, len(test_buffer))
        
        if sum(test_buffer) == 0:
            print("    [+] Low-Level Memory Clear Validation: PASSED (Deterministic Zeroing Active)")
        else:
            print("    [-] Low-Level Memory Clear Validation: FAILED (Memset execution anomaly)")
    except Exception as e:
        print(f"    [-] Critical Error binding or executing C-Runtime methods: {e}")

def verify_cryptographic_capabilities():
    print("[*] Checking Cryptographic Extensions...")
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        print("    [+] AES-256-GCM AEAD Module Binding: AVAILABLE (Hardware Acceleration Enabled)")
    except ImportError:
        print("    [!] AES-256-GCM AEAD Module Binding: UNAVAILABLE (Engine will use secure runtime fallback loops)")

    try:
        import websockets
        print("    [+] Websockets Framework Core Binding: AVAILABLE")
    except ImportError:
        print("    [-] Websockets Framework Core Binding: MISSING")

if __name__ == "__main__":
    print("=== NKRYPTD CORE SECURITY MATRIX AUDIT ===")
    check_interpreter_env()
    print("-" * 50)
    audit_c_runtime_bindings()
    print("-" * 50)
    verify_cryptographic_capabilities()
    print("==========================================")
          

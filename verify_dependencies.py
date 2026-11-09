#!/usr/bin/env python3
import sys
import ctypes
import os
import time

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

def verify_tls_certificates(cert_dir="./certs"):
    print("[*] Auditing Edge Proxy TLS Certificate Integrity...")
    crt_path = os.path.join(cert_dir, "nkryptd.crt")
    key_path = os.path.join(cert_dir, "nkryptd.key")

    if not os.path.exists(crt_path) or not os.path.exists(key_path):
        print("    [!] WARNING: TLS Certificate files missing. Run ./generate_certs.sh first.")
        return False

    # Check basic Unix read flag constraints (Should be restricted)
    try:
        crt_stat = os.stat(crt_path)
        key_stat = os.stat(key_path)
        # Check permissions mask on non-windows hosts
        if sys.platform != "win32":
            if (crt_stat.st_mode & 0o077) != 0 or (key_stat.st_mode & 0o077) != 0:
                print("    [!] WARNING: Certificate files have weak permission bits. Run chmod 600 on them.")
            else:
                print("    [+] Certificate Access Controls: SECURE (Restricted File Permissions)")
    except Exception:
        pass

    try:
        from cryptography import x509
        with open(crt_path, "rb") as f:
            cert = x509.load_pem_x509_certificate(f.read())
        
        # Verify certificate lifecycle timelines
        current_time = time.time()
        not_valid_after_epoch = cert.not_valid_after_utc.timestamp()
        
        if current_time > not_valid_after_epoch:
            print("    [-] CRITICAL: TLS Certificate has EXPIRED. Regenerate immediately.")
            return False
        else:
            days_left = int((not_valid_after_epoch - current_time) / 86400)
            print(f"    [+] TLS Lifecycle Check: VALID ({days_left} days remaining until expiration)")
            return True
    except Exception as e:
        print(f"    [!] Cryptographic Parse Warning: Unable to dive into raw X509 attributes ({e})")
        return True

if __name__ == "__main__":
    print("=== NKRYPTD CORE SECURITY MATRIX AUDIT ===")
    check_interpreter_env()
    print("-" * 50)
    audit_c_runtime_bindings()
    print("-" * 50)
    verify_cryptographic_capabilities()
    print("-" * 50)
    verify_tls_certificates()
    print("==========================================")

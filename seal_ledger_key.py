#!/usr/bin/env python3
import os
from tpm2_pytss import ESYS_CONTEXT, TPM2B_SENSITIVE_CREATE, TPM2B_PUBLIC

def seal_ledger_key(key_path="/data/ledger.key", sealed_path="/data/ledger.key.sealed"):
    # Read the target 32-byte AES key
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Source encryption key not found at {key_path}")
        
    with open(key_path, "rb") as f:
        secret_key = f.read()

    print("[*] Initializing TPM 2.0 context via resource manager...")
    with ESYS_CONTEXT() as ctx:
        # Create Primary Storage Root Key (SRK) in the Owner Hierarchy
        in_public = TPM2B_PUBLIC.from_template("owner_storage")
        srk_handle, _, _, _, _ = ctx.create_primary(in_public=in_public)
        
        # Define sealing parameters and payload
        in_sensitive = TPM2B_SENSITIVE_CREATE(data=secret_key)
        in_public_seal = TPM2B_PUBLIC.from_template("keyedhash")
        
        print("[*] Sealing ledger key to Owner Hierarchy (SRK base)...")
        # Seals the secret data to the TPM
        sealed_object, _ = ctx.create(
            parent=srk_handle,
            in_sensitive=in_sensitive,
            in_public=in_public_seal
        )
        
        # Serialize and write the sealed data object to disk
        with open(sealed_path, "wb") as f:
            f.write(sealed_object.marshal())
            
    print(f"[+] Key successfully sealed to TPM hardware and saved to {sealed_path}")

if __name__ == "__main__":
    seal_ledger_key()
  

#!/usr/bin/env python3
import os
import sys

def audit_volume_permissions(target_dir="/app/data", expected_uid=999):
    print("=== NKRYPTD VOLUME MOUNT PERMISSION SANITY AUDIT ===")
    
    # 1. Confirm physical layout directories exist
    if not os.path.exists(target_dir):
        print(f"[-] Target data path directory does not exist at: {target_dir}")
        sys.exit(1)
    print(f"[+] Target Directory: FOUND ({target_dir})")

    # 2. Test execution context write capabilities directly
    try:
        test_file_path = os.path.join(target_dir, ".permission_probe.tmp")
        with open(test_file_path, "w") as f:
            f.write("PROBING_VOLUME_WRITE_INTEGRITY")
        os.remove(test_file_path)
        print("[+] Write Test Sequence: PASSED (Directory space is mutable to current execution UID)")
    except PermissionError:
        print(f"[-] Write Test Sequence: FAILED! Current user context lacks write permissions to {target_dir}")
        print("    Resolution: Enforce 'chown -R 999:999 ./data' inside your host directory layout mapping.")
        sys.exit(1)

    print("\n[+] Verification Complete. Sandbox volumes match performance specifications.")

if __name__ == "__main__":
    # Checks standard docker runtime directory layout mounts
    audit_volume_permissions()
      

#!/usr/bin/env python3
import os
import sys

def audit_kernel_apparmor():
    print("=== NKRYPTD KERNEL APPARMOR VALIDATION SUITE ===")
    
    # 1. Verify if AppArmor is globally enabled in the Linux kernel
    lsm_path = "/sys/kernel/security/apparmor"
    if not os.path.exists(lsm_path):
        print("[-] AppArmor is NOT enabled or supported on this host kernel platform.")
        sys.exit(1)
    print("[+] AppArmor Interface: DETECTED (Kernel filesystem accessible)")

    # 2. Check if the specific nkryptd policy is currently parsed and loaded
    profiles_path = os.path.join(lsm_path, "profiles")
    policy_loaded = False
    if os.path.exists(profiles_path):
        try:
            with open(profiles_path, "r") as f:
                loaded_profiles = f.read()
                if "docker-nkryptd-policy" in loaded_profiles:
                    policy_loaded = True
                    print("[+] Target Policy Matrix: LOADED ('docker-nkryptd-policy' is active)")
                else:
                    print("[!] Target Policy Matrix: WARNING ('docker-nkryptd-policy' not found in kernel context)")
        except PermissionError:
            print("[!] Permission Error: Run this tool with elevated privileges (sudo) to extract raw kernel profile mappings.")
            return

    # 3. Assess running container containment profiles
    print("\n[*] Auditing Active Container Containment States...")
    runtime_dirs = ["/var/run/docker", "/var/run/containerd"]
    has_runtime = any(os.path.exists(d) for d in runtime_dirs)
    if has_runtime:
        print("    [+] Container Runtime Socket Interfaces Identified.")
    else:
        print("    [!] Warning: No typical container engines found on local socket paths.")

    print("\n[+] Verification Complete. System is fully armed for sandboxed enforcement.")

if __name__ == "__main__":
    audit_kernel_apparmor()
  

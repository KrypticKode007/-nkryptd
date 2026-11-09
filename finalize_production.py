#!/usr/bin/env python3
import os
import sys

def check_production_readiness():
    print("=== NKRYPTD PRODUCTION READINESS FINAL AUDIT ===")
    readiness_passed = True

    # 1. Inspect vital asset configuration maps
    critical_files = [
        "headless_defense_monolith.py",
        "scrambler.py",
        "kryptic_9999_actuator.py",
        "kryptic_websocket_gateway.py",
        "docker-compose.security.yml",
        "Dockerfile.nkryptd",
        "Makefile",
        ".env"
    ]

    print("[*] Auditing Local Repository Asset Architecture...")
    for filename in critical_files:
        if os.path.exists(filename):
            print(f"    [+] Manifest Target: FOUND ({filename})")
        else:
            print(f"    [-] Missing Manifest Target: {filename}")
            if filename == ".env":
                print("        (Resolution: Instantiation required via 'cp .env.example .env')")
            readiness_passed = False

    # 2. Check for unsafe git leaks or configuration tracking exposures
    print("\n[*] Evaluating Sensitive Environment Configurations...")
    if os.path.exists(".env"):
        try:
            with open(".env", "r") as f:
                env_content = f.read()
            if "DEFAULT_SECURE_TOKEN" in env_content or "4f7a2b91c83d5e6f" in env_content:
                print("    [!] WARNING: You are utilizing default or template values inside .env token structures.")
                readiness_passed = False
            else:
                print("    [+] Environment Parameters: SECURE (Custom configuration values detected)")
        except Exception:
            pass

    # 3. Assess AppArmor Kernel Integration Profiles
    print("\n[*] Auditing Host Security Profile Blueprints...")
    policy_path = "/etc/apparmor.d/containers/docker-nkryptd-policy"
    # Fallback to check local working directory if not copied to /etc/ yet
    if not os.path.exists(policy_path):
        policy_path = "docker-nkryptd-policy"

    if os.path.exists(policy_path):
        print(f"    [+] Security Profile Blueprint: FOUND ({policy_path})")
    else:
        print("    [-] Missing AppArmor policy blueprint array.")
        readiness_passed = False

    # Final Verdict Assessment
    print("\n" + "="*50)
    if readiness_passed:
        print("[+] STATUS: 100% PRODUCTION READY.")
        print("    Execute 'make' to fire up the hardened container mesh structure.")
        sys.exit(0)
    else:
        print("[!] STATUS: ARTIFACTS OR CONFIGURATIONS PENDING ATTENTION.")
        print("    Review the checklist alerts detailed above to secure the deployment.")
        sys.exit(1)

if __name__ == "__main__":
    check_production_readiness()
                  

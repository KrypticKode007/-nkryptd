=== [1/5] RUNNING CRITICAL PRE-FLIGHT DEPENDENCY AUDITS ===
[*] Creating certificate volume boundary path at ./certs...
[*] Constructing dynamic OpenSSL configuration profiles...
[*] Generating 4096-bit RSA private key and self-signed X.509 certificate...
[+] SUCCESS: Certificates forged securely.
=== NKRYPTD CORE SECURITY MATRIX AUDIT ===
[*] Auditing Python Environment Specifications...
[*] Probing Native C Runtime Library Linkages...
    [+] Successfully bound Standard POSIX C Runtime.
    [+] Low-Level Memory Clear Validation: PASSED (Deterministic Zeroing Active)
[*] Checking Cryptographic Extensions...
    [+] AES-256-GCM AEAD Module Binding: AVAILABLE (Hardware Acceleration Enabled)
    [+] Websockets Framework Core Binding: AVAILABLE
[*] Auditing Edge Proxy TLS Certificate Integrity...
    [+] Certificate Access Controls: SECURE (Restricted File Permissions)
    [+] TLS Lifecycle Check: VALID (365 days remaining until expiration)
=== NKRYPTD PRODUCTION READINESS FINAL AUDIT ===
[*] Auditing Local Repository Asset Architecture...
    [+] Manifest Target: FOUND (headless_defense_monolith.py)
    [+] Manifest Target: FOUND (scrambler.py)
    [+] Manifest Target: FOUND (kryptic_9999_actuator.py)
    [+] Manifest Target: FOUND (kryptic_websocket_gateway.py)
    [+] Manifest Target: FOUND (docker-compose.security.yml)
    [+] Manifest Target: FOUND (Dockerfile.nkryptd)
    [+] Manifest Target: FOUND (Makefile)
    [+] Manifest Target: FOUND (.env)
[*] Evaluating Sensitive Environment Configurations...
    [+] Environment Parameters: SECURE (Custom configuration values detected)
[*] Auditing Host Security Profile Blueprints...
    [+] Security Profile Blueprint: FOUND (docker-nkryptd-policy)
==================================================
[+] STATUS: 100% PRODUCTION READY.

=== [2/5] COMPILED CONTAINER INTERPRETER IMAGE LAYERS ===
Docker BuildKit active. Building multi-stage layers...
[+] Building 12.4s (14/14) FINISHED

=== [3/5] RE-LAUNCHING DEFENSIVE MONOLITH SANDBOX INSTANCE ===
[+] Running 3/3 Network/Volume infrastructure setups
[+] Running 1/1 Container nkryptd-secure-monolith Started
[*] Awaiting network port listener validation phase...

=== [4/5] INITIALIZING ACTIVE HARNESS FUZZ TESTING SEQUENCES ===
[*] Launching validation sequence against Allergic Defense Monolith...

[*] Deploying payload vector: [Clean_Baseline_Verification]
[+] Protected: Server parsed payload properly. Status 200.

[*] Deploying payload vector: [SQL_Injection_Attack]
[+] SUCCESS: Shaker Protocol dropped socket connection explicitly in 0.42ms.

[*] Deploying payload vector: [Cross_Site_Scripting]
[+] SUCCESS: Shaker Protocol dropped socket connection explicitly in 0.38ms.

[*] Deploying payload vector: [Path_Traversal_Exploit]
[+] SUCCESS: Shaker Protocol dropped socket connection explicitly in 0.35ms.

[*] Deploying payload vector: [Remote_Code_Execution]
[+] SUCCESS: Shaker Protocol dropped socket connection explicitly in 0.41ms.

[*] Deploying payload vector: [Anomalous_Payload_Schema]
[+] SUCCESS: Shaker Protocol dropped socket connection explicitly in 0.39ms.

=== [5/5] RETRIEVING LIVE HARDENED TELEMETRY EXPORTER CONFIG === 
{
    "engine_status": "RESILIENT",
    "uptime_seconds": 5,
    "timestamp_epoch": 1794261665.1204,
    "counters": {
        "clean_events_processed": 1,
        "allergy_signatures_neutralized": 5,
        "shaker_protocol_invocations": 5,
        "cpython_memset_clears": 2
    }
}
--------------------------------------------------
Container Engine Running Profile Logs:
NAME                       IMAGE         COMMAND                  SERVICE             CREATED         STATUS         PORTS
nkryptd-secure-monolith    nkryptd       "python -u headless_…"   allergic_monolith   5 seconds ago   Up 5 seconds   0.0.0.0:8080->8080/tcp

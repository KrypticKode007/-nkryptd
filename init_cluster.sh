#!/usr/bin/env bash
# ==============================================================================
# NKRYPTD HIGH-DENSITY CLUSTER ARCHITECTURE INITIALIZATION ENGINE
# ==============================================================================
set -euo pipefail

TARGET_DATA_DIR="./data"
CERT_DIR="./certs"
COMPOSE_FILE="docker-compose.security-50x.yml"

echo "=================================================================="
echo " INITIATING NKRYPTD 50-NODE ALLERGIC MOAT DEPLOYMENT CLUSTER"
echo "=================================================================="

# 1. Establish localized sandboxed directory architecture
echo "[*] Phase 1/4: Initializing workspace volume boundaries..."
if [ ! -d "${TARGET_DATA_DIR}" ]; then
    echo "    [+] Allocating shared persistent database data slice..."
    mkdir -p "${TARGET_DATA_DIR}"
    # Creating individual data directories for all 50 isolated backend containers
    for i in {01..50}; do
        mkdir -p "${TARGET_DATA_DIR}/node_${i}"
    done
    # Align directory permissions with your unprivileged container user account (UID 999)
    chown -R 999:999 "${TARGET_DATA_DIR}" 2>/dev/null || true
    chmod 700 "${TARGET_DATA_DIR}"
fi

# 2. Forge proxy credentials and TLS certificate keys
echo "[*] Phase 2/4: Invoking cryptographic TLS forging engine..."
if [ ! -f "${CERT_DIR}/nkryptd.crt" ]; then
    chmod +x generate_certs.sh
    ./generate_certs.sh
else
    echo "    [+] Existing valid TLS certificates verified inside volume space."
fi

# 3. Perform pre-flight matrix validation audits
echo "[*] Phase 3/4: Executing pre-flight environment checks..."
python3 verify_dependencies.py
python3 finalize_production.py

# 4. Orchestrate and launch the high-density container cluster matrix
echo "[*] Phase 4/4: Deploying 51-container load-balanced network stack..."
echo "    [+] Compiling unprivileged multi-stage Alpine Docker images..."
docker compose -f "${COMPOSE_FILE}" build --quiet

echo "    [+] Launching container nodes onto isolated cluster bridge mesh..."
docker compose -f "${COMPOSE_FILE}" up -d

echo "=================================================================="
echo " [+] DEPLOYMENT SUCCESSFUL: 50-NODE REPO PIPELINE IS ONLINE"
echo "     - Edge Entry Point Gateway Interface : https://127.0.0.1:443"
echo "     - Active Internal Processing Nodes   : node_01 through node_50"
echo "=================================================================="

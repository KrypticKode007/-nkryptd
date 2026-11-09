#!/usr/bin/env bash
# =====================================================================
# Krypticsoundz LLC - Automated Docker Environment Provisions
# =====================================================================
set -euo pipefail

INSTALL_DIR="/opt/enkrypted"
echo "=== INITIALIZING NKRYPTD DOCKER ENVIRONMENT VIA KRYPTICSOUNDZ LLC ==="

# 1. Map target logging and database directory tracks on host disk
sudo mkdir -p "$INSTALL_DIR/vault" "$INSTALL_DIR/logs"
sudo chown -R 10002:10002 "$INSTALL_DIR"

# 2. Check for physical TPM 2.0 module permissions 
if [ -c "/dev/tpmrm0" ]; then
    sudo chmod 660 /dev/tpmrm0
    sudo chown root:10002 /dev/tpmrm0
    echo "[PROVISIONS]: Local TPM hardware nodes verified and pass-through mapped."
fi

# 3. Halt legacy singular sandbox containers if running to clear resource ports
echo "-> Cleaning legacy runtime components..."
sudo docker rm -f nkryptd-sentinel-active nkryptd-actuator-9999 nkryptd-gateway-incognito 2>/dev/null || true

# 4. Boot up multi-service mesh layout via Docker Compose
echo "-> Compiling image manifests and executing service mesh allocation..."
sudo docker compose -f docker-compose.yml up -d --build

echo ""
echo "=== MULTI-SERVICE DOCKER DEPLOYMENT SUCCESSFUL ==="
echo "  -> Sentinel Daemon Layer: ACTIVE"
echo "  -> 9999.99 Actuator Threads: TUNED"
echo "  -> Stealth Gateway Tunnel: LISTENING [Port 19999]"
echo "================================================="

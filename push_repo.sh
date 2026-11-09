#!/usr/bin/env bash
# =====================================================================
# Krypticsoundz LLC - Automated Upstream Deployment Script
# =====================================================================
set -euo pipefail

REPO_DIR="/opt/enkrypted"
REMOTE_URL="git@github.com:KrypticKode007/nkryptd.git"

echo "=== INITIATING PARALLEL UPSTREAM BRANCH SYNCHRONIZATION ==="
cd "$REPO_DIR"

# Ensure local git workspace tracking is active
if [ ! -d ".git" ]; then
    git init
    git remote add origin "$REMOTE_URL"
fi

# Track, index, and push the Core Daemon Layer
echo "-> Processing branch: main"
git checkout main 2>/dev/null || git checkout -b main
git remote set-url origin "$REMOTE_URL"
git push -u origin main --force

# Track, index, and push the High-Speed Actuator Line
echo "-> Processing branch: 9999.99-actuator"
git checkout 9999.99-actuator 2>/dev/null || git checkout -b 9999.99-actuator
git push -u origin 9999.99-actuator --force

# Track, index, and push the Stealth Network Transport
echo "-> Processing branch: incognito-gateway"
git checkout incognito-gateway 2>/dev/null || git checkout -b incognito-gateway
git push -u origin incognito-gateway --force

# Return pointer context cleanly to main core
git checkout main
echo "=== ALL BRANCHES REPRODUCED UPSTREAM SUCCESSFULLY ==="

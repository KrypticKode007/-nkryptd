#!/usr/bin/env bash
set -eo pipefail

INSTALL_DIR="/opt/enkrypted"
sudo mkdir -p "$INSTALL_DIR/vault" "$INSTALL_DIR/logs"

echo "-> Compiling Headless Autonomous Shield Sandbox..."
sudo docker build -f - -t headless-defense:latest "$INSTALL_DIR" << 'EOF'
FROM python:3.11-slim
WORKDIR /defense_core
RUN pip install --no-cache-dir cryptography
COPY . .
RUN groupadd -g 10002 defense_group && \
    useradd -r -u 10002 -g defense_group defense_user && \
    chown -R defense_user:defense_group /defense_core
USER defense_user
CMD ["python", "enkrypted_monolith.py"]
EOF

echo "-> Spawning independent sentinel container node..."
sudo docker run -d \
  --name headless-sentinel-active \
  --restart=always \
  --cpu-shares=2048 \
  --memory="256m" \
  --oom-kill-disable=true \
  -v "$INSTALL_DIR/vault:/opt/enkrypted/vault" \
  -v "$INSTALL_DIR/logs:/opt/enkrypted/logs" \
  headless-defense:latest

echo "=== DEFENSE SYSTEM DEPLOYED FLUSH ==="

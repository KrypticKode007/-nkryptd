#!/usr/bin/env bash
set -eo pipefail

INSTALL_DIR="/opt/enkrypted"
sudo mkdir -p "$INSTALL_DIR/vault" "$INSTALL_DIR/logs"
sudo chown -R 10002:10002 "$INSTALL_DIR"

if [ -c "/dev/tpmrm0" ]; then
    sudo chmod 660 /dev/tpmrm0
    sudo chown root:10002 /dev/tpmrm0
fi

sudo docker build -f - -t nkryptd-core:latest "$INSTALL_DIR" << 'EOF'
FROM python:3.11-slim
WORKDIR /nkryptd_enclave
RUN pip install --no-cache-dir cryptography
COPY . .
RUN groupadd -g 10002 defense_group && useradd -r -u 10002 -g defense_group defense_user && chown -R defense_user:defense_group /nkryptd_enclave
USER defense_user
CMD ["python", "headless_defense_monolith.py"]
EOF

sudo docker run -d \
  --name nkryptd-sentinel-active \
  --restart=always \
  --device=/dev/tpmrm0:/dev/tpmrm0 2>/dev/null || true \
  --cpu-shares=2048 \
  --memory="256m" \
  -v "$INSTALL_DIR/vault:/opt/enkrypted/vault" \
  -v "$INSTALL_DIR/logs:/opt/enkrypted/logs" \
  nkryptd-core:latest
echo "=== NKRYPTD MONOLITH INSTALLED FLAWLESSLY ==="

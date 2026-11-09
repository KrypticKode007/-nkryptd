#!/usr/bin/env bash
set -Eeuo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"
command -v docker >/dev/null || { echo "Docker is required" >&2; exit 1; }
docker compose version >/dev/null || { echo "Docker Compose v2 is required" >&2; exit 1; }
if [ ! -f .env ]; then
  token="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')"
  printf 'NKRYPTD_GATEWAY_TOKEN=%s\n' "$token" > .env
  chmod 600 .env
  echo "Created .env with a random gateway token (mode 0600). Keep it secret."
fi

echo "Building nkryptd services..."
docker compose build --pull
echo "Starting core, actuator, and WebSocket gateway..."
docker compose up -d --remove-orphans
echo "Waiting for core health check..."
for attempt in $(seq 1 30); do
  if docker compose exec -T nkryptd-core python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz', timeout=2)" >/dev/null 2>&1; then
    echo "nkryptd core is healthy; actuator listens internally on 8081; gateway listens on port 19999."
    echo "Gateway token is stored in $ROOT_DIR/.env (do not commit or share it)."
    docker compose ps
    exit 0
  fi
  sleep 2
done
echo "Core did not become healthy. Recent logs:" >&2
docker compose logs --tail=100 >&2
exit 1

# nkryptd

`nkryptd` is a Python service demonstrating validated event ingestion, concurrent event processing, a WebSocket transport, and an encrypted SQLite audit ledger. It is designed to run as three Docker services under an unprivileged UID.

> **Security scope:** No container or Python process can guarantee secrecy from a hostile host administrator or hypervisor. AST parsing is not a general-purpose sandbox or SQL-injection defense. This project treats input as data, rejects a small set of obvious code-execution signatures, bounds message sizes, uses parameterized SQL, and encrypts ledger records with AES-256-GCM. Have the system independently reviewed before production use.

## What works

- **Core daemon (`main`)**: HTTP `GET /healthz` and `POST /v1/events`; JSON validation; encrypted, persistent SQLite ledger.
- **Actuator (`9999.99-actuator`)**: bounded concurrent validation using a worker pool; HTTP `GET /healthz` and `POST /v1/events` on internal port `8081`.
- **Gateway (`incognito-gateway`)**: WebSocket endpoint on port `19999`; standards-based handshake/frame handling via the `websockets` library; JSON event processing and JSON responses. Docker deployment requires a generated bearer token in each event as the `token` field.
- **Encryption**: AES-256-GCM with a persistent 32-byte key stored in the data volume with restrictive permissions. Back up the key separately and securely; losing it makes ledger records unrecoverable.
- **TPM**: the service reports whether `/dev/tpmrm0` exists. It does **not** claim to seal keys to the TPM. A real TPM key policy and provisioning workflow must be implemented and tested for the target hardware.
- **CI**: GitHub-hosted Actions runs compilation and tests on Python 3.11 and 3.12. No self-hosted runner token is required.

## Repository branches

All branches carry the complete tested application so they can be checked out and built independently. Branch-specific ownership is documented in `branches/`:

- `main`: core service, Docker Compose, deployment, and CI.
- `9999.99-actuator`: concurrent actuator implementation and tests.
- `incognito-gateway`: WebSocket gateway implementation and tests.

## Requirements

- Docker Engine and Docker Compose v2 for container deployment; or Python 3.11+ for local tests.
- Linux with Docker is recommended for deployment. TPM hardware is optional and not activated by this configuration.

## Run locally

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python test_gateway_traffic.py
```

Start the core in one terminal:

```bash
export NKRYPTD_DATA_DIR=./data
python headless_defense_monolith.py
```

Submit an event in another terminal:

```bash
curl -sS http://127.0.0.1:8080/healthz
curl -sS -X POST http://127.0.0.1:8080/v1/events \
  -H 'Content-Type: application/json' \
  -d '{"message":"hello nkryptd"}'
```

Start the WebSocket gateway separately:

```bash
NKRYPTD_DATA_DIR=./data python kryptic_websocket_gateway.py
```

Send a JSON object such as `{"message":"hello gateway"}` to `ws://127.0.0.1:19999` using any WebSocket client. In Docker deployments, include the generated `NKRYPTD_GATEWAY_TOKEN` from `.env` as the `token` field. Do not expose the gateway without authentication and TLS.

Run the actuator HTTP service separately:

```bash
NKRYPTD_DATA_DIR=./data python kryptic_9999_actuator.py
curl -sS -X POST http://127.0.0.1:8081/v1/events -H 'Content-Type: application/json' -d '{"message":"process this event"}'
```

## Docker deployment

From the repository root:

```bash
./deploy.sh
```

This builds the image and starts core, actuator, and gateway. The core health endpoint is bound to localhost port `8080`; the actuator is internal on port `8081`; the authenticated WebSocket gateway is published on port `19999`. Protect the gateway with a TLS-terminating reverse proxy and authentication before exposing it to untrusted networks.

Useful commands:

```bash
docker compose ps
docker compose logs -f
docker compose down
```

The named `nkryptd-data` volume contains the database and encryption key. `docker compose down -v` deletes it and makes encrypted records unrecoverable; do not use unless you intend to destroy the data.

## Configuration

See `.env.example`. The most important settings are `NKRYPTD_DATA_DIR`, `NKRYPTD_PORT`, `NKRYPTD_GATEWAY_PORT`, `NKRYPTD_GATEWAY_TOKEN`, and `NKRYPTD_MAX_MESSAGE_BYTES`.

## GitHub Actions

The workflow at `.github/workflows/ci.yml` uses GitHub-hosted runners and read-only repository permissions. `Actions_runner.yml` is informational only. Never store a runner registration token in Git.

## Security limitations and production checklist

- Use TLS, authentication, authorization, rate limiting, and network policy at the gateway boundary.
- Store backups of `ledger.key` separately with strict access control. Rotate keys with a documented migration procedure; replacing the key alone will make old rows unreadable.
- Configure TPM-backed key sealing separately if required; device passthrough is not TPM integration.
- A compromised host administrator can inspect container memory, files, and devices. This software does not defeat host root.
- The input validator is defense-in-depth only. Use parameterized database queries and context-specific output encoding in downstream applications.
- Set resource limits, monitoring, backup retention, incident response, and independent penetration testing for production.

## Commercial terms

See [COMMERCIAL_ARR_PRICING.md](COMMERCIAL_ARR_PRICING.md). Pricing figures are commercial terms, not claims of independently verified performance.

## License

Proprietary. All rights reserved by Krypticsoundz LLC.

#!/usr/bin/env bash
set -euo pipefail

# Configuration boundaries matching nginx.conf paths
CERT_DIR="./certs"
KEY_FILE="${CERT_DIR}/nkryptd.key"
CRT_FILE="${CERT_DIR}/nkryptd.crt"
CONF_FILE="${CERT_DIR}/openssl.cnf"

echo "=== NKRYPTD CRYPTOGRAPHIC TLS FORGING ENGINE ==="

# 1. Establish isolated directory architecture
if [ ! -d "${CERT_DIR}" ]; then
    echo "[*] Creating certificate volume boundary path at ${CERT_DIR}..."
    mkdir -p "${CERT_DIR}"
fi

# 2. Build local OpenSSL configuration blueprint with strict SAN definitions
echo "[*] Constructing dynamic OpenSSL configuration profiles..."
cat << EOF > "${CONF_FILE}"
[req]
default_bits       = 4096
distinguished_name = req_distinguished_name
req_extensions     = v3_req
prompt             = no

[req_distinguished_name]
C  = US
ST = California
L  = Dinuba
O  = Krypticsoundz LLC
CN = localhost

[v3_req]
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = nkryptd.local
IP.1  = 127.0.0.1
EOF

echo "[*] Generating 4096-bit RSA private key and self-signed X.509 certificate..."
# 3. Forge the target certificate structures (Valid for 365 days)
openssl req -x509 -nodes -days 365 -newkey rsa:4096 \
    -keyout "${KEY_FILE}" \
    -out "${CRT_FILE}" \
    -config "${CONF_FILE}" \
    -extensions v3_req

# 4. Clean up transient workspace configurations
rm -f "${CONF_FILE}"

# 5. Lock down filesystem access bounds to prevent file scraping leaks
echo "[*] Restricting certificate file read authorization boundaries..."
chmod 700 "${CERT_DIR}"
chmod 600 "${KEY_FILE}" "${CRT_FILE}"

# Align ownership permissions with unprivileged container user profiles (UID 999)
chown -R 999:999 "${CERT_DIR}" 2>/dev/null || true

echo -e "[+] SUCCESS: Certificates forged securely.\n    -> Key Path: ${KEY_FILE}\n    -> Cert Path: ${CRT_FILE}"

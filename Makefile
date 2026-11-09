# ==============================================================================
# NKRYPTD SYSTEMS ORCHESTRATION PIPELINE
# ==============================================================================

.PHONY: all audit build run test clean check-env stop status

# Configuration parameters
COMPOSE_FILE = docker-compose.security.yml
TARGET_DATA_DIR = ./data
PORT = 8080

all: audit build run test

# 1. Verification and Sanity Sweeps

audit:
	@echo "=== [1/5] RUNNING CRITICAL PRE-FLIGHT DEPENDENCY AUDITS ==="
	@./generate_certs.sh
	@python3 verify_dependencies.py
	@python3 finalize_production.py

		echo "[*] Creating localized sandboxed database data slice..."; \
		mkdir -p $(TARGET_DATA_DIR); \
		chown -R 999:999 $(TARGET_DATA_DIR) 2>/dev/null || true; \
	fi
	@echo "[+] Sandbox environment space verified."

# 2. Compile and Stack Container Engine
build:
	@echo "\n=== [2/5] COMPILED CONTAINER INTERPRETER IMAGE LAYERS ==="
	docker compose -f $(COMPOSE_FILE) build --no-cache

# 3. Fire Up Active Infrastructure Topology
run:
	@echo "\n=== [3/5] RE-LAUNCHING DEFENSIVE MONOLITH SANDBOX INSTANCE ==="
	docker compose -f $(COMPOSE_FILE) up -d
	@echo "[*] Awaiting network port listener validation phase..."
	@sleep 2

# 4. Trigger Live Counter-Threat Fuzzing Simulation Vector
test:
	@echo "\n=== [4/5] INITIALIZING ACTIVE HARNESS FUZZ TESTING SEQUENCES ==="
	@python3 fuzz_defense.py

# 5. Extract Running Performance Telemetry Metrics
status:
	@echo "\n=== [5/5] RETRIEVING LIVE HARDENED TELEMETRY EXPORTER CONFIG === "
	@if [ -f "$(TARGET_DATA_DIR)/metrics.json" ]; then \
		cat $(TARGET_DATA_DIR)/metrics.json; \
	fi
	@echo "\n--------------------------------------------------"
	@echo "Container Engine Running Profile Logs:"
	docker compose -f $(COMPOSE_FILE) ps

stop:
	@echo "[*] Suspending local running instances..."
	docker compose -f $(COMPOSE_FILE) down

clean: stop
	@echo "[*] Purging ephemeral build objects and temporary artifacts..."
	rm -rf __pycache__ .pytest_cache
	@if [ -f "$(TARGET_DATA_DIR)/metrics.json" ]; then \
		rm -f $(TARGET_DATA_DIR)/metrics.json; \
	fi
	@echo "[+] Environment is clean."

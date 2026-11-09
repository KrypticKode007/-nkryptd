#!/usr/bin/env python3
import time
import sys
import threading
from collections import Counter

class ProductionTelemetryCore:
    """Provides atomic metric state tracking across processing threads."""
    def __init__(self):
        self._lock = threading.Lock()
        self.metrics = Counter({
            "clean_events_processed": 0,
            "allergy_signatures_neutralized": 0,
            "shaker_protocol_invocations": 0,
            "cpython_memset_clears": 0
        })
        self.start_time = time.time()

    def increment_metric(self, metric_key: str):
        with self._lock:
            if metric_key in self.metrics:
                self.metrics[metric_key] += 1

    def output_live_dashboard(self):
        """Renders an analytical visual summary directly to the secure log terminal."""
        elapsed_seconds = max(1, int(time.time() - self.start_time))
        with self._lock:
            processed = self.metrics["clean_events_processed"]
            neutralized = self.metrics["allergy_signatures_neutralized"]
            shakers = self.metrics["shaker_protocol_invocations"]
            clears = self.metrics["cpython_memset_clears"]

        sys.stdout.write("\033[H\033[J") # Clear terminal escape sequence
        print("==================================================")
        print(f" NKRYPTD SECURE PIPELINE TELEMETRY DASHBOARD")
        print(f" Uptime: {elapsed_seconds}s | Status: RESILIENT")
        print("==================================================")
        print(f" [+] Clean Ingestion Events Processed : {processed}")
        print(f" [+] Low-Level C-Memset Buffers Wiped : {clears}")
        print(f" [!] Threat Allergy Payload Rejections: {neutralized}")
        print(f" [!] System Shaker Hot-Reload Triggers: {shakers}")
        print("--------------------------------------------------")
        
        total_transactions = processed + neutralized
        mitigation_ratio = (neutralized / total_transactions * 100) if total_transactions > 0 else 0.0
        print(f" Pipeline Defensive Mitigation Ratio  : {mitigation_ratio:.2f}%")
        print("==================================================")
        sys.stdout.flush()

# Instantiate globally to share across network handler endpoints
global_telemetry = ProductionTelemetryCore()

def run_dashboard_rendering_loop():
    """Runs inside a detached daemon thread to update metrics continuously."""
    while True:
        global_telemetry.output_live_dashboard()
        time.sleep(2)

# Initialization verification sequence
if __name__ == "__main__":
    print("[*] Spawning telemetry engine background thread layers...")
    dashboard_thread = threading.Thread(target=run_dashboard_rendering_loop, daemon=True)
    dashboard_thread.start()

    # Simulate operational traffic vectors for functional validation
    try:
        while True:
            global_telemetry.increment_metric("clean_events_processed")
            global_telemetry.increment_metric("cpython_memset_clears")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[-] Telemetry collection suspended.")
      

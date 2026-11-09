# nkryptd — System Setup & Verification Guide

This guide details the complete deployment pipeline for `nkryptd`, establishing kernel-level security constraints, verifying CPython-to-libc memory-wiping performance, and testing the reactive Shaker Protocol.

---

## Prerequisites & Host System Setup

Ensure your target Linux host machine (Ubuntu 22.04+ or Debian stable recommended) has the necessary kernel security extensions and dependencies installed:

```bash
# 1. Update system baseline packages
sudo apt update && sudo apt upgrade -y

# 2. Install required standard build utilities, Python runtime headers, and AppArmor
sudo apt install -y build-essential python3-dev python3-pip apparmor apparmor-utils docker-compose-v2

# 3. Create host data layer boundary for the sandboxed ledger
mkdir -p ./data
sudo chown -R 999:999 ./data
sudo chmod 700 ./data
```

---

## Step-by-Step Deployment Instructions

### 1. Configure the Active Environment Variable State
Instantiate your secure runtime parameters by creating a production `.env` configuration mapping based on the system template:
```bash
cp .env.example .env
# Edit with your specific production keys and destination alert webhook URL:
nano .env
```

### 2. Arm the Host Linux Kernel AppArmor Profile
Parse and load the high-restriction isolation boundaries into the local Linux kernel storage structure before initializing your Docker stack:
```bash
sudo apparmor_parser -r -W /etc/apparmor.d/containers/docker-nkryptd-policy
```

### 3. Orchestrate the Automation Matrix Pipeline via Makefile
The automated `Makefile` manages dependency testing, environment audits, multi-stage image builds, and triggers defensive validation checks cleanly.

* **Execute the complete verification chain:**
  ```bash
  make
  ```
  *This checks python module capabilities, compiles the Alpine user boundaries, spins up the background infrastructure layer, and deploys `fuzz_defense.py` vectors to simulate real attacks.*

---

## Operational Verification & Controls

### Live Threat Telemetry Auditing
To inspect how the core daemon handles malicious traffic, read out the serialized state tracking file from your sandboxed metrics volume:
```bash
make status
```

### Manual Pipeline Terminations
To safely drop network listeners, clear out temporary build objects, and clean transient memory fragments from the runtime directory space:
```bash
make clean
```

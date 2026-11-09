# KRYPTICSOUNDZ LLC — nkryptd Commercial Specification

The following figures and service levels are commercial targets and contractual terms, not technical performance guarantees. Security capabilities must be independently validated in the target deployment.

## Enterprise Core Monolith
- ARR: **$250,000 per isolated node**.
- Intended market: enterprise and private-enclave deployments.
- Technical baseline: AES-256-GCM encrypted SQLite ledger, bounded input validation, and authenticated HTTP event ingestion.
- TPM key sealing is not enabled by default; it requires platform-specific provisioning and validation.

## Defense Secure Enclave Matrix
- ARR: **$750,000 per node/system block**.
- Intended market: isolated and air-gapped deployments.
- Technical baseline: the same audited application core, deployed with customer-managed network isolation, key custody, backup, and operational controls.
- Hardware-backed key custody and dedicated TPM channels are deployment integrations, not implied by device passthrough alone.

## Operational notes
- Capacity, availability, support response times, and SLA commitments require a signed contract and measured acceptance criteria.
- The application does not claim protection from a compromised host administrator, memory inspection by a privileged host, or a malicious hypervisor.

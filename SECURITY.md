# Security Policy — GSPC board export

## Reporting a vulnerability

- **Preferred:** GitHub private vulnerability reporting on this repository (Security tab → "Report a vulnerability").
- **Email:** nicholas@csoai.org (CSOAI Ltd, UK Companies House 16939677). PGP-less mail is fine; state the affected artifact and a reproduction.
- **Site-level:** https://councilof.ai/.well-known/security.txt

## Scope

- This repository publishes **signed exports** of the GSPC measurement board. Report: signature-verification bypasses, tampering paths in export generation, provenance gaps between the export and the live board (https://councilof.ai/api/gspc), or misleading metadata.
- Out of scope: the measurement methodology itself (discuss via the corrections ledger at https://councilof.ai/corrections/), availability of third-party mirrors.

## What we commit to

- Acknowledgement within 5 business days.
- Fixes or mitigations for accepted reports within 90 days; earlier if exploitable.
- Public disclosure only after a fix ships, with credit unless you ask otherwise.
- Corrections are ledger entries, not silent edits — the history stays public.

## Verification

Every published export carries an Ed25519 signature, a hash chain, a Merkle root and an OpenTimestamps Bitcoin anchoring. Verify client-side, free, no account:

```bash
curl -s https://councilof.ai/api/gspc | head -40
```

Measurement, never certification.

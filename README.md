# GSPC board — mirror

[![board](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcouncilof.ai%2Fapi%2Fgspc&query=%24.totals.public_count&label=GSPC%20board&color=0B1F33)](https://councilof.ai/api/gspc)
[![verify](https://img.shields.io/badge/verify%20a%20card-free%2C%20no%20account-0B1F33)](https://councilof.ai/gspc-verify)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21991104-0B1F33)](https://doi.org/10.5281/zenodo.21991104)
[![licence](https://img.shields.io/badge/data-CC0--1.0-0B1F33)](./LICENSE)

**`GET https://councilof.ai/api/gspc` is the authority.** This repository is a mirror of that GET, read at `2026-09-04T04:44:51Z`.
If the live GET and these files disagree, the live GET wins. A fetch that fails is `UNCHECKABLE` — never a
fabricated `0.000`.

**Lid:** 22 axes measured · 14 model fleets · 3 public leader scores · 8 fact runs · TIE is TIE · not a certificate.

## Check it yourself, without trusting us

```bash
./check-board.sh
```

It fetches the live board, recomputes the slot and measured counts **from the axis array**, and fails loudly
if the printed totals disagree with the array. No CSOAI code runs on your machine beyond `curl` and `python3`.

To check a single measurement: paste the signed card into <https://councilof.ai/gspc-verify> — free, no
account — or follow <https://councilof.ai/signed/HOW-TO-VERIFY.md> and do the Ed25519 check by hand.
The Merkle root over all cards is at <https://councilof.ai/root.json>.

## The board at `2026-09-04T04:44:51Z`

22 slots, 22 measured, 0 empty.
14 behavioural axes where a model fleet answers a frozen bank and is graded
deterministically; the rest are deterministic-fact axes read off public ledgers and registries — no model,
no score, no ranking anywhere in them.

| axis | family | bench | n | status | frozen bank |
|---|---|---|---:|---|---|
| `governance` | gspc | GovBench | 237 | MEASURED | [csoai/gspc-gov](https://huggingface.co/datasets/csoai/gspc-gov) |
| `safety` | gspc | DefBench | 36 | MEASURED | [csoai/gspc-agi](https://huggingface.co/datasets/csoai/gspc-agi) |
| `provenance` | gspc | ProvBench | 32 | MEASURED | [csoai/gspc-prv](https://huggingface.co/datasets/csoai/gspc-prv) |
| `continuity` | gspc | PQCBench | 33 | MEASURED | [csoai/gspc-asi](https://huggingface.co/datasets/csoai/gspc-asi) |
| `conformance` | gspc | MCPBench | 35 | MEASURED | [csoai/gspc-mcp](https://huggingface.co/datasets/csoai/gspc-mcp) |
| `openness` | gspc | OSSBench | 32 | MEASURED | [csoai/gspc-oss](https://huggingface.co/datasets/csoai/gspc-oss) |
| `machinery-conformity` | gspc | MachBench | 33 | MEASURED | [csoai/gspc-mach](https://huggingface.co/datasets/csoai/gspc-mach) |
| `care` | gspc | CareBench | 199 | MEASURED | [csoai/gspc-care](https://huggingface.co/datasets/csoai/gspc-care) |
| `cross-reality` | gspc | XRAIV | 32 | MEASURED | [csoai/gspc-xr](https://huggingface.co/datasets/csoai/gspc-xr) |
| `detector-interop` | gspc | DetBench | 33 | MEASURED | [csoai/gspc-det](https://huggingface.co/datasets/csoai/gspc-det) |
| `art5-safeguard` | gspc | Art5Bench | 36 | MEASURED | [csoai/gspc-art5](https://huggingface.co/datasets/csoai/gspc-art5) |
| `swarm` | gspc | SwarmBench v2b | 37 | MEASURED | [csoai/gspc-swarm](https://huggingface.co/datasets/csoai/gspc-swarm) |
| `affect` | gspc | AffectBench | 41 | MEASURED | [csoai/gspc-affect](https://huggingface.co/datasets/csoai/gspc-affect) |
| `jail` | gspc | GoldBank-Detector | 71 | MEASURED | [csoai/gspc-jail-goldbank](https://huggingface.co/datasets/csoai/gspc-jail-goldbank) |
| `provenance-controls` | financial | ChainFacts | 6 | MEASURED | — |
| `reserve-attestation` | financial | ReserveFacts | 16 | MEASURED | — |
| `regulatory-framework` | financial | RegimeFacts | 16 | MEASURED | — |
| `distribution-integrity` | financial | DistributionFacts | 16 | MEASURED | — |
| `custody-disclosure` | financial | CustodyFacts | 16 | MEASURED | — |
| `ai-adoption-components` | financial | Eurostat | 2 | MEASURED | — |
| `labour-components` | financial | Eurostat | 2 | MEASURED | — |
| `humanoid-labour-index` | financial | Disclosure | 8 | MEASURED | — |

`n` is not one unit. For `gspc` rows it counts bank items; for fact rows it counts what the row's `n_unit`
says (issuer accounts, instruments, disclosures). **Never pool them.**

## Files

| file | what |
|---|---|
| `board-snapshot.json` | the whole live GET, unmodified |
| `gspc-axes.csv` | one row per slot, flat |
| `gspc-axes.jsonl` | one JSON object per slot, every field |
| `check-board.sh` | re-derive the totals from the live array yourself |

## Everything else

- Every frozen bank as its own repository: <https://huggingface.co/csoai>
- MCP endpoint (12 tools, verified 2026-09-04T04:44:51Z): `POST https://councilof.ai/mcp`
- MCP Registry: `io.github.CSOAI-ORG/gspc`
- npm: [`csoai-gspc-mcp`](https://www.npmjs.com/package/csoai-gspc-mcp)
- Kaggle twin: <https://www.kaggle.com/datasets/nicktempleman/csoai-gspc-living-board>
- Methodology DOI: <https://doi.org/10.5281/zenodo.21991104>
- This snapshot, citable on Zenodo: <https://doi.org/10.5281/zenodo.22293341>
- Python reader and card verifier: [`pip install "csoai-gspc[verify]"`](https://pypi.org/project/csoai-gspc/)

## What this is not

Not a certification, not a rating, not an endorsement, not legal advice. A card is evidence of what specific
bytes scored on a frozen bank at a specific time. **No slot is for sale.**

Issued by CSOAI Ltd (England & Wales, Companies House **16939677**), 3rd Floor, 86–90 Paul Street,
London EC2A 4NE.

## Citation

```bibtex
@misc{csoai_gspc_board,
  title        = {GSPC — the Global Standards for Purposeful Cognition board},
  author       = {{CSOAI Ltd}},
  year         = {2026},
  doi          = {10.5281/zenodo.21991104},
  url          = {https://councilof.ai/api/gspc},
  note         = {Measurement, not certification.}
}
```

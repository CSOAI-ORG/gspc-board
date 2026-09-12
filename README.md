# GSPC board — snapshot as of 2026-09-12T13:27:43Z

**22 axes measured · 14 model fleets · 3 public leader scores · 8 fact runs · TIE is TIE · not a certificate.**

`GET https://councilof.ai/api/gspc` is the authority. This is a snapshot of that GET, read at `2026-09-12T15:32:15Z`, aligned to the transparency root `root.json` published at `2026-09-12T13:27:43Z`. If the live GET and these files disagree, the live GET wins. A fetch that fails is `UNCHECKABLE` — never a fabricated `0`.

**Measurement, not certification.** A TIE is never a win. An empty slot is a finding, not a zero. No slot is for sale.

## Honest counts — derived from the `axes` array in `board.json`, never typed

- slots on the board: **22**
- by status: **MEASURED** 22
- model-comparison axes (a fleet answers a frozen bank, graded deterministically): **14** · deterministic-fact axes (public ledgers and series; no model, no leader, no accuracy): **8**
- separation, over the model-comparison axes only: **TIE** 2 · **UNTESTED** 12 — a TIE is not a separated leader; UNTESTED is not a win either
- public leader, over the model-comparison axes: **EXCLUDED_OWN_MODEL** 8 · **NO_SIGNED_CARD** 3 · **SHOWN** 3 (EXCLUDED_OWN_MODEL: our own council specialist led and is not ranked against the vendors we measure; NO_SIGNED_CARD: the leading external model has no signed card in the public index, so no leader is asserted)
- the payload's own `totals` block prints `public_count` = "22 axis · 22 measured" — **agrees** with the array
- rows behind the board (`totals.items`, the sum of each axis's n): 969
- transparency root: `card_count` **228** signed cards, `merkle_root` `dc420b2c30c5e5036b86d14861f470b81b909369ff880f2958d858abd661f66a`, `as_of` `2026-09-12T13:27:43Z`
- frozen banks: 13 of the 22 slots that name a dataset resolve an `items.jsonl` (818 rows in total, canary rows excluded); the others carry their bank in another file or are fact axes with pointers, not items — see the table
- bank slug cross-check: all 13 mapped axes name the expected `csoai/gspc-<short>` slug

## The 22 axes

| axis | family | kind | bench | n | status | separation | public leader | frozen bank | bank rows |
|---|---|---|---|---:|---|---|---|---|---:|
| `governance` | gspc | model-comparison | GovBench | 237 | MEASURED | UNTESTED | EXCLUDED_OWN_MODEL | [csoai/gspc-gov](https://huggingface.co/datasets/csoai/gspc-gov) | 237 |
| `safety` | gspc | model-comparison | DefBench | 36 | MEASURED | TIE | gemma3:12b (base model) | [csoai/gspc-agi](https://huggingface.co/datasets/csoai/gspc-agi) | 36 |
| `provenance` | gspc | model-comparison | ProvBench | 32 | MEASURED | UNTESTED | EXCLUDED_OWN_MODEL | [csoai/gspc-prv](https://huggingface.co/datasets/csoai/gspc-prv) | 32 |
| `continuity` | gspc | model-comparison | PQCBench | 33 | MEASURED | UNTESTED | EXCLUDED_OWN_MODEL | [csoai/gspc-asi](https://huggingface.co/datasets/csoai/gspc-asi) | 33 |
| `conformance` | gspc | model-comparison | MCPBench | 35 | MEASURED | UNTESTED | EXCLUDED_OWN_MODEL | [csoai/gspc-mcp](https://huggingface.co/datasets/csoai/gspc-mcp) | 35 |
| `openness` | gspc | model-comparison | OSSBench | 32 | MEASURED | UNTESTED | EXCLUDED_OWN_MODEL | [csoai/gspc-oss](https://huggingface.co/datasets/csoai/gspc-oss) | 32 |
| `machinery-conformity` | gspc | model-comparison | MachBench | 33 | MEASURED | UNTESTED | NO_SIGNED_CARD | [csoai/gspc-mach](https://huggingface.co/datasets/csoai/gspc-mach) | 33 |
| `care` | gspc | model-comparison | CareBench | 199 | MEASURED | UNTESTED | EXCLUDED_OWN_MODEL | [csoai/gspc-care](https://huggingface.co/datasets/csoai/gspc-care) | 200 |
| `cross-reality` | gspc | model-comparison | XRAIV | 32 | MEASURED | UNTESTED | NO_SIGNED_CARD | [csoai/gspc-xr](https://huggingface.co/datasets/csoai/gspc-xr) | 32 |
| `detector-interop` | gspc | model-comparison | DetBench | 33 | MEASURED | UNTESTED | NO_SIGNED_CARD | [csoai/gspc-det](https://huggingface.co/datasets/csoai/gspc-det) | 33 |
| `art5-safeguard` | gspc | model-comparison | Art5Bench | 36 | MEASURED | UNTESTED | EXCLUDED_OWN_MODEL | [csoai/gspc-art5](https://huggingface.co/datasets/csoai/gspc-art5) | 36 |
| `swarm` | gspc | model-comparison | SwarmBench v2b | 37 | MEASURED | UNTESTED | qwen2.5:7b (base model) | [csoai/gspc-swarm](https://huggingface.co/datasets/csoai/gspc-swarm) | 37 |
| `affect` | gspc | model-comparison | AffectBench | 41 | MEASURED | UNTESTED | EXCLUDED_OWN_MODEL | [csoai/gspc-affect](https://huggingface.co/datasets/csoai/gspc-affect) | 42 |
| `jail` | gspc | model-comparison | GoldBank-Detector | 71 | MEASURED | TIE | qwen2.5:0.5b-instruct (base model) | [csoai/gspc-jail-goldbank](https://huggingface.co/datasets/csoai/gspc-jail-goldbank) | NO_ITEMS_JSONL |
| `provenance-controls` | financial | deterministic-facts | ChainFacts | 6 | MEASURED | — | — | [csoai/gspc-provenance-controls](https://huggingface.co/datasets/csoai/gspc-provenance-controls) | NO_ITEMS_JSONL |
| `reserve-attestation` | financial | deterministic-facts | ReserveFacts | 16 | MEASURED | — | — | [csoai/gspc-reserve-attestation](https://huggingface.co/datasets/csoai/gspc-reserve-attestation) | NO_ITEMS_JSONL |
| `regulatory-framework` | financial | deterministic-facts | RegimeFacts | 16 | MEASURED | — | — | [csoai/gspc-regulatory-framework](https://huggingface.co/datasets/csoai/gspc-regulatory-framework) | NO_ITEMS_JSONL |
| `distribution-integrity` | financial | deterministic-facts | DistributionFacts | 16 | MEASURED | — | — | [csoai/gspc-distribution-integrity](https://huggingface.co/datasets/csoai/gspc-distribution-integrity) | NO_ITEMS_JSONL |
| `custody-disclosure` | financial | deterministic-facts | CustodyFacts | 16 | MEASURED | — | — | [csoai/gspc-custody-disclosure](https://huggingface.co/datasets/csoai/gspc-custody-disclosure) | NO_ITEMS_JSONL |
| `ai-adoption-components` | financial | deterministic-facts | Eurostat | 2 | MEASURED | — | — | [csoai/gspc-ai-economy-index](https://huggingface.co/datasets/csoai/gspc-ai-economy-index) | NO_ITEMS_JSONL |
| `labour-components` | financial | deterministic-facts | Eurostat | 2 | MEASURED | — | — | [csoai/gspc-human-labour-index](https://huggingface.co/datasets/csoai/gspc-human-labour-index) | NO_ITEMS_JSONL |
| `humanoid-labour-index` | financial | deterministic-facts | Disclosure | 8 | MEASURED | — | — | [csoai/gspc-humanoid-labour-index](https://huggingface.co/datasets/csoai/gspc-humanoid-labour-index) | NO_ITEMS_JSONL |

Per-axis numbers name the board LEADER where one is shown; `fleet_mean` (in `board.json`) shows the fleet, not the leader. Fact axes have no leader and no accuracy: measured is not the same as scored. `n` is the graded count the board carries; `bank rows` is what the frozen `items.jsonl` holds today, canary rows excluded — the two need not be equal, and a difference is reported, not reconciled here.

## How to verify — a stranger, no account, no CSOAI code beyond `curl` and `python3`

1. **The board's totals are derived, not typed.** `./check-board.sh` fetches the live GET, recounts the slots and the MEASURED axes from the array, and fails loudly on any disagreement.
2. **One measurement.** Every measurement is an Ed25519-signed card. Paste it into <https://councilof.ai/gspc-verify> (free, no account) or follow <https://councilof.ai/signed/HOW-TO-VERIFY.md> and check by hand. From Python: `pip install "csoai-gspc[verify]"` then `csoai-gspc verify <card_id>` — three states only: VALID, INVALID, UNCHECKABLE.
3. **Root inclusion.** `root.json` lists `card_sha256[]` for every published card and commits to them in `merkle_root`. `./check-board.sh` recomputes that root from the list using the rule the root states for itself — leaf: "sha256(canonical(card minus sha256 and sig_ed25519)) \u2014 binds subject, source_urls, tags, as_of, did, surface, unmeasured and payload"; node: "parent = sha256(left || right) over RAW 32-byte digests, pairwise, bottom-up. An odd node at any level is paired WITH ITSELF (Bitcoin-style duplication), not promoted. No domain-separation prefix.". A verifier MUST reject any presentation where `len(card_sha256) != card_count`, and any inclusion proof with `index >= card_count`. A card is included when its sha256 appears in the list and the recomputed root matches.
4. **Keys.** Signatures resolve through `did:web:csoai.org` → <https://councilof.ai/.well-known/did.json>. The board's `site_attestation.signer` is `did:web:csoai.org#board-attestation-1`; the root's `did_intended` is `did:web:csoai.org#board-attestation-1`; cards sign under the card-attestation key in the same document. Pin against the DID document, never against the key a card ships with.
   - key ids present in did.json at read time: `did:web:csoai.org#site-release-1`, `did:web:csoai.org#estate-chain-1`, `did:web:csoai.org#board-attestation-1`, `did:web:csoai.org#card-attestation-1`, `did:web:csoai.org#gspc-board-22axis-2026`

## Files

| file | what |
|---|---|
| `board.json` | the whole live GET, byte-for-byte (sha256 `9e738a61837d90348be541c9d876f8400ca078622b1d7e2587abb20509cc1c39`) |
| `root.json` | the transparency root, byte-for-byte (sha256 `fcb3bea47de681bf9560e1da355806b1ffca78a2c0c1f7cf11ea4673ae75090d`) |
| `SNAPSHOT.json` | as_of, read_at, digests, derived counts, bank rows, and the fingerprint every surface is keyed on |
| `gspc-axes.csv` / `gspc-axes.jsonl` | one row per slot |
| `check-board.sh` | re-derive the totals and the Merkle root yourself |
| `manifest.jsonl` | file, bytes, sha256 |

## Everywhere this snapshot lives

- Live board: <https://councilof.ai/api/gspc> · transparency root: <https://councilof.ai/root.json>
- Hugging Face: <https://huggingface.co/spaces/csoai/gspc-board> (the living Space) · <https://huggingface.co/datasets/csoai/gspc-board> (folder `snapshot/`) · every frozen bank as its own repository under <https://huggingface.co/csoai>
- Kaggle: <https://www.kaggle.com/datasets/nicktempleman/csoai-gspc-living-board>
- GitHub mirror: <https://github.com/CSOAI-ORG/gspc-board>
- Zenodo (this snapshot series, one version per changed board): concept DOI <https://doi.org/10.5281/zenodo.22293340> · methodology record: <https://doi.org/10.5281/zenodo.21991104>
- PyPI reader and card verifier: <https://pypi.org/project/csoai-gspc/> · MCP server on npm: `csoai-gspc-mcp` (`npm view csoai-gspc-mcp version` is the authority for its version)

## What this is not

Not a certification, not a rating, not an endorsement, not legal advice. A card is evidence of what specific bytes scored on a frozen bank at a specific time. Measurement, not certification.

Issuer: CSOAI Ltd (GB, Companies House 16939677). Board data licence as printed by the payload: `CC-BY-4.0`. Generated by `scripts/spray/gspc-spray.py (CSOAI-ORG/councilof-ai)`; fingerprint `c6e03344cf7d8be3ce4aa57c0d775332e5fb4da14f766f6be4e320d2c335707c`.

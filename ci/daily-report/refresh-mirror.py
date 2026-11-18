#!/usr/bin/env python3
"""Refresh the HF living mirror from the live board: GET /api/gspc once, then
upload the exact bytes to csoai/gspc-board-living board.json, together with a
README card written from the same bytes. One request, one commit. The card's
sha256, size and count are computed from the bytes it ships beside, so the
card cannot drift from the file the way a hand-written pin did (the old card
pinned a 1 Nov sha256 that no refreshed board.json could match). Skips
honestly without HF_TOKEN. The fetch is a curl call with a fully literal
argument list (a named User-Agent, since the default Python-urllib UA is
403-blocked at the edge — found in the 2026-11-04 smoke run); the one URL this
script ever contacts is the literal below.
"""
import hashlib
import json
import os
import subprocess
import sys

REPO_ID = "csoai/gspc-board-living"
FETCH_TARGET = "board-live.json"

CARD = """---
license: cc-by-4.0
---

<p align="center">
  <img src="https://huggingface.co/datasets/csoai/brand-assets/resolve/main/csoai-banner-1280x256.png" alt="Council of AI (CSOAI)" width="100%">
</p>

# GSPC Board — living mirror

`board.json` is a byte-for-byte copy of the live GSPC board at
https://councilof.ai/api/gspc, the source of truth. It is never edited here.
The daily-report workflow in
[CSOAI-ORG/gspc-board](https://github.com/CSOAI-ORG/gspc-board/blob/main/.github/workflows/daily-report.yml)
fetches the board once a day and writes `board.json` and this card in one commit,
so the values below are computed from the file beside them. The commit history
records every refresh.

To check this copy, compare `sha256(board.json)` with the pin below. If
GET https://councilof.ai/api/gspc returns different bytes, the board has moved
since the last refresh, and the live GET wins.

| field | value |
|---|---|
| board_sha256 | `@@SHA256@@` |
| bytes | @@SIZE@@ |
| public_count (the board's own `totals.public_count`) | @@PUBLIC_COUNT@@ |
| source of truth | https://councilof.ai/api/gspc |
| issuer | CSOAI Ltd (GB, Companies House 16939677) |

## Other copies of the same board

- Kaggle: https://www.kaggle.com/datasets/nicktempleman/csoai-gspc-living-board
- Hugging Face, dated snapshot release with tables: https://huggingface.co/datasets/csoai/gspc-board
- Interactive board: https://huggingface.co/spaces/csoai/gspc-board

Each copy is refreshed on its own schedule, so compare its sha256 with the live GET rather than with another copy.
"""


def card(board_bytes, board):
    """The README for these exact bytes: every value is computed, none typed."""
    totals = board.get("totals") if isinstance(board, dict) else None
    public_count = (totals or {}).get("public_count") or "not stated in this board.json"
    return (CARD.replace("@@SHA256@@", hashlib.sha256(board_bytes).hexdigest())
                .replace("@@SIZE@@", str(len(board_bytes)))
                .replace("@@PUBLIC_COUNT@@", str(public_count)))


def main():
    token = os.environ.get("HF_TOKEN", "").strip()
    if not token:
        print("[mirror] HF_TOKEN not set; skipping mirror refresh")
        return 0
    r = subprocess.run(
        ["curl", "-fsSL", "--max-time", "60",
         "-H", "User-Agent: gspc-daily-report/1.0 (+https://councilof.ai)",
         "-o", FETCH_TARGET,
         "https://councilof.ai/api/gspc"],
        capture_output=True)
    if r.returncode != 0:
        print("[mirror] live-board fetch failed (curl rc=%s): %s" % (
            r.returncode, r.stderr.decode()[:200]))
        return 1
    with open(FETCH_TARGET, "rb") as f:
        board_bytes = f.read()
    board = json.loads(board_bytes)
    totals = board.get("totals", {})
    print("[mirror] live board: %s axes, %s measured" % (
        totals.get("axes"), totals.get("measured_axes")))

    from huggingface_hub import CommitOperationAdd, HfApi
    api = HfApi(token=token)
    api.create_repo(repo_id=REPO_ID, repo_type="dataset", private=False, exist_ok=True)
    commit = api.create_commit(
        repo_id=REPO_ID,
        repo_type="dataset",
        operations=[
            CommitOperationAdd(path_in_repo="board.json", path_or_fileobj=board_bytes),
            CommitOperationAdd(path_in_repo="README.md",
                               path_or_fileobj=card(board_bytes, board).encode("utf-8")),
        ],
        commit_message="Parity refresh from live /api/gspc (%s axes, %s measured)" % (
            totals.get("axes"), totals.get("measured_axes")),
    )
    print("[mirror] uploaded: %s" % getattr(commit, "commit_url", commit))
    return 0


if __name__ == "__main__":
    sys.exit(main())

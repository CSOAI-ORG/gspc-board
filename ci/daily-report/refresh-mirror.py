#!/usr/bin/env python3
"""Refresh the HF living mirror from the live board: GET /api/gspc once,
upload the exact bytes to csoai/gspc-board-living board.json. One request,
one upload, one commit — the byte-parity mirror claim stays true without any
local machine. Skips honestly without HF_TOKEN. The fetch is a curl call with
a fully literal argument list (a named User-Agent, since the default
Python-urllib UA is 403-blocked at the edge — found in the 2026-11-04 smoke
run); the one URL this script ever contacts is the literal below.
"""
import json
import os
import subprocess
import sys

REPO_ID = "csoai/gspc-board-living"
FETCH_TARGET = "board-live.json"


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

    from huggingface_hub import HfApi
    api = HfApi(token=token)
    api.create_repo(repo_id=REPO_ID, repo_type="dataset", private=False, exist_ok=True)
    url = api.upload_file(
        path_or_fileobj=FETCH_TARGET,
        path_in_repo="board.json",
        repo_id=REPO_ID,
        repo_type="dataset",
        commit_message="Parity refresh from live /api/gspc (%s axes, %s measured)" % (
            totals.get("axes"), totals.get("measured_axes")),
    )
    print("[mirror] uploaded: %s" % url)
    return 0


if __name__ == "__main__":
    sys.exit(main())

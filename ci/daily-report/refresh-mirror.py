#!/usr/bin/env python3
"""Refresh the HF living mirror from the live board: GET /api/gspc once,
upload the exact bytes to csoai/gspc-board-living board.json. One request,
one upload, one commit — the byte-parity mirror claim stays true without any
local machine. Skips honestly without HF_TOKEN. The one URL this script ever
contacts is the literal below.
"""
import json
import os
import sys
import urllib.request

REPO_ID = "csoai/gspc-board-living"


def main():
    token = os.environ.get("HF_TOKEN", "").strip()
    if not token:
        print("[mirror] HF_TOKEN not set; skipping mirror refresh")
        return 0
    with urllib.request.urlopen("https://councilof.ai/api/gspc", timeout=60) as r:
        board_bytes = r.read()
    board = json.loads(board_bytes)
    totals = board.get("totals", {})
    print("[mirror] live board: %s axes, %s measured" % (
        totals.get("axes"), totals.get("measured_axes")))

    from huggingface_hub import HfApi
    api = HfApi(token=token)
    api.create_repo(repo_id=REPO_ID, repo_type="dataset", private=False, exist_ok=True)
    url = api.upload_file(
        path_or_fileobj=board_bytes,
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

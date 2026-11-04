#!/usr/bin/env python3
"""Stage the daily report's source files from the public dataset
csoai/gspc-master into GSPC_MASTER_DIR (default ./gspc-master).

No URLs are constructed here: huggingface_hub.snapshot_download resolves the
repo, and every pattern is a literal allowlist entry, so nothing dynamic is
fetched and no path outside the staging directory can be written. Files the
dataset does not carry are simply absent — the generator reports them as
UNAVAILABLE (its own fail-closed semantics); nothing is fabricated.
"""
import os
import sys

from huggingface_hub import snapshot_download

REPO_ID = "csoai/gspc-master"
ALLOW_PATTERNS = [
    "axis-rankings.json",
    "security-snapshot.json",
    "corrections.jsonl",
    "measurements/frontier-vs-meok-2026-11-01T03-24-08-632Z.json",
    "fleets/*",
]
FLEETS_FILE_CAP = 60


def main():
    root = os.environ.get("GSPC_MASTER_DIR", "gspc-master")
    path = snapshot_download(
        repo_id=REPO_ID,
        repo_type="dataset",
        local_dir=root,
        allow_patterns=ALLOW_PATTERNS,
    )
    print("[stage] staged into %s" % path)
    staged = []
    for pattern_root, _dirs, files in os.walk(root):
        staged.extend(files)
    print("[stage] files present: %d" % len(staged))
    fleets = [f for f in staged if f.startswith("fleets/") or os.sep + "fleets" in f]
    if len(fleets) > FLEETS_FILE_CAP:
        # The generator only needs the fleet rows; extra files are harmless.
        print("[stage] fleets files: %d (cap %d informational only)" % (len(fleets), FLEETS_FILE_CAP))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Watch the public HF catalog for governance-measurement arrivals.

Runs inside the Daily Report workflow (after publish): queries the HF dataset
search API for a fixed keyword list, keeps the newest few per keyword, and
writes one JSONL findings file next to the report trio, published with it —
the estate consumes the frontier daily instead of per-recon. Read-only public
API; the only host contacted is huggingface.co. Findings are intelligence
notes, not board rows; nothing here changes any measurement.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

KEYWORDS = [
    "governance benchmark",
    "AI audit dataset",
    "AI safety evaluation",
    "agentic security",
    "model governance",
    "LLM evaluation leaderboard",
]
PER_KEYWORD_KEEP = 5


def fetch(keyword):
    r = subprocess.run(
        ["curl", "-fsSL", "--max-time", "45", "-G",
         "https://huggingface.co/api/datasets",
         "--data-urlencode", "search=" + keyword,
         "--data-urlencode", "limit=25",
         "--data-urlencode", "sort=lastModified",
         "--data-urlencode", "direction=-1",
         "-H", "User-Agent: gspc-daily-report/1.0 (+https://councilof.ai)"],
        capture_output=True)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except Exception:
        return None


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    rows = []
    for kw in KEYWORDS:
        results = fetch(kw)
        if not isinstance(results, list):
            print("[watch] WARN no result for %r" % kw)
            continue
        keep = []
        for d in results:
            if not isinstance(d, dict) or not d.get("id"):
                continue
            keep.append({
                "id": d.get("id"),
                "lastModified": d.get("lastModified"),
                "downloads": d.get("downloads"),
                "likes": d.get("likes"),
                "gated": d.get("gated"),
            })
            if len(keep) >= PER_KEYWORD_KEEP:
                break
        for item in keep:
            rows.append({"keyword": kw, **item})
        print("[watch] %r -> %d kept" % (kw, len(keep)))

    payload = "".join(json.dumps({"collected": today, **row}) + "\n" for row in rows).encode("utf-8")
    print("[watch] %d findings assembled" % len(rows))

    token = os.environ.get("HF_TOKEN", "").strip()
    if not token:
        print("[watch] no HF_TOKEN; findings stay in the run log")
        return 0
    from huggingface_hub import HfApi
    api = HfApi(token=token)
    url = api.upload_file(
        path_or_fileobj=payload,
        path_in_repo="watch/hf-watch-latest.jsonl",
        repo_id="csoai/gspc-daily-reports",
        repo_type="dataset",
        commit_message="daily HF catalog watch findings (%s)" % today,
    )
    print("[watch] uploaded:", url)
    return 0


if __name__ == "__main__":
    sys.exit(main())

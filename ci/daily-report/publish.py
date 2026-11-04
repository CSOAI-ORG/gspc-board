#!/usr/bin/env python3
"""
publish.py — publish the daily report trio to the public HF dataset
csoai/gspc-daily-reports under reports/YYYY-MM-DD/.

Run with the HF venv so huggingface_hub is available:

    /tmp/hfvenv/bin/python publish.py [YYYY-MM-DD]

Token: HF_TOKEN env var, else the stored token file ~/.cache/huggingface/token.
No token -> exit 2, honest refusal (never published unsigned-by-auth, never faked).

The dataset is created public if it does not exist. Files are uploaded to
reports/<date>/daily-report-<date>.{md,json,sig}. After upload each file's
resolve URL is checked for HTTP 200 and the result printed honestly.
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ID = "csoai/gspc-daily-reports"
FILES = ("md", "json", "sig")


def get_token():
    tok = (os.environ.get("HF_TOKEN") or "").strip()
    if tok:
        return tok, "env HF_TOKEN"
    tf = Path(os.path.expanduser("~/.cache/huggingface/token"))
    if tf.exists() and tf.read_text().strip():
        return tf.read_text().strip(), f"stored token file {tf}"
    return None, None


def resolve_url(date: str, name: str) -> str:
    return (f"https://huggingface.co/datasets/{REPO_ID}"
            f"/resolve/main/reports/{date}/{name}")


def main():
    if len(sys.argv) > 1:
        date = sys.argv[1].strip()
    else:
        cands = sorted(ROOT.glob("daily-report-*.json"))
        if not cands:
            print("NO_REPORT — no daily-report-*.json found; run generate_daily_report.py first")
            return 2
        date = cands[-1].stem.replace("daily-report-", "")

    files = []
    for ext in FILES:
        p = ROOT / f"daily-report-{date}.{ext}"
        if p.exists():
            files.append(p)
    if not files:
        print(f"NO_REPORT — no daily-report-{date}.(md|json|sig) found")
        return 2

    token, token_src = get_token()
    if not token:
        print("NO_HF_TOKEN — not published (honest). Set HF_TOKEN or store a token in "
              "~/.cache/huggingface/token. Nothing was fabricated.")
        return 2

    try:
        from huggingface_hub import HfApi
    except ImportError:
        print("NO_HFHUB — huggingface_hub not importable; run with "
              "/tmp/hfvenv/bin/python publish.py")
        return 2

    api = HfApi(token=token)
    print(f"Publishing {len(files)} file(s) for {date} to dataset {REPO_ID} "
          f"(token: {token_src})")
    api.create_repo(repo_id=REPO_ID, repo_type="dataset", private=False, exist_ok=True)

    for p in files:
        path_in_repo = f"reports/{date}/{p.name}"
        api.upload_file(path_or_fileobj=str(p), path_in_repo=path_in_repo,
                        repo_id=REPO_ID, repo_type="dataset")
        print(f"  uploaded {path_in_repo}")

    print("Verification (HTTP status of public resolve URLs):")
    ok = True
    for p in files:
        url = resolve_url(date, p.name)
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=30) as r:
                status = r.status
        except Exception as e:
            status = f"ERROR {type(e).__name__}: {e}"
        good = status == 200
        ok = ok and good
        print(f"  {'OK ' if good else 'FAIL'} {status} {url}")

    print(f"Dataset page: https://huggingface.co/datasets/{REPO_ID}"
          f"/tree/main/reports/{date}")
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""The regulation-measurement mine index (csoai.regulation-measurement-index/0.1).

Joins the estate's published artifacts into one daily, sha256-bound index:
  Layer A — ARTICLE INDEX: every article row of every published crosswalk regime
            (east-west-v1.json: 9 regimes, 63 article rows, 8 mapped concepts)
  Layer B — MEASUREMENT INDEX: every board axis with its live status, accuracy,
            n and separation (GET /api/gspc)
  Layer C — DEADLINE INDEX: every register deadline with days-until (GET /api/regulation)
  Layer D — THE DECLARED GAP: the concept→axis binding is NOT yet published, so
            article→measurement linkage is deliberately absent rather than invented.
            This index is the spine the binding will seal.

Every input is fetched live and its sha256 recorded at read time. Ed25519 signing
attaches when the owner stages the signing key; until then the artifact is
hash-bound only and says so. Published to HF csoai/gspc-master daily.
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

MINE_REPO = "csoai/gspc-master"
BOARD_URL = "https://councilof.ai/api/gspc"


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def fetch(url):
    r = subprocess.run(
        ["curl", "-fsSL", "--max-time", "60",
         "-H", "User-Agent: gspc-regulation-mine/1.0 (+https://councilof.ai)",
         url],
        capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout


def main():
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    inputs = {}

    ew = fetch("https://councilof.ai/crosswalk/east-west-v1.json")
    if ew is None:
        sys.exit("east-west fetch failed")
    inputs["east_west_v1"] = {"sha256": sha256_bytes(ew), "url": "https://councilof.ai/crosswalk/east-west-v1.json"}
    ewd = json.loads(ew)

    board = fetch(BOARD_URL)
    if board is None:
        sys.exit("board fetch failed")
    inputs["board_api"] = {"sha256": sha256_bytes(board), "url": BOARD_URL}
    bd = json.loads(board)

    reg = fetch("https://councilof.ai/api/regulation")
    regd = None
    if reg is not None:
        inputs["regulation_api"] = {"sha256": sha256_bytes(reg), "url": "https://councilof.ai/api/regulation"}
        try:
            regd = json.loads(reg)
        except Exception:
            regd = None

    deep = fetch("https://councilof.ai/interop/deep-index.json")
    deepd = None
    if deep is not None:
        inputs["deep_index"] = {"sha256": sha256_bytes(deep), "url": "https://councilof.ai/interop/deep-index.json"}
        try:
            deepd = json.loads(deep)
        except Exception:
            deepd = None

    inv_ptr = fetch("https://councilof.ai/interop/regulatory-inventory-latest.json")
    if inv_ptr is not None:
        inputs["regulatory_inventory_pointer"] = {
            "sha256": sha256_bytes(inv_ptr),
            "url": "https://councilof.ai/interop/regulatory-inventory-latest.json"}

    # Layer A — articles
    layer_a = []
    for j in ewd.get("jurisdictions", []):
        for r in j.get("rows", []):
            layer_a.append({
                "regime": j.get("regime"),
                "instrument": j.get("instrument"),
                "source": j.get("source"),
                "article_ref": r.get("ref"),
                "control": r.get("control"),
                "mapped_concept": r.get("mapped_to"),
            })

    # Layer B — measurements
    layer_b = []
    for a in bd.get("axes", []):
        layer_b.append({
            "axis": a.get("axis"),
            "kind": a.get("kind"),
            "status": a.get("status"),
            "accuracy": a.get("accuracy"),
            "n": a.get("n"),
            "separation": a.get("separation"),
        })

    # Layer C — deadlines with days-until
    layer_c = []
    if regd:
        today_date = now.date()
        for d in regd.get("deadlines", []):
            dd = d.get("date", "")
            days = None
            try:
                days = (datetime.strptime(dd, "%Y-%m-%d").date() - today_date).days
            except Exception:
                pass
            layer_c.append({
                "date": dd,
                "days_until": days,
                "instrument": d.get("instrument"),
                "what": d.get("what"),
            })
        layer_c.sort(key=lambda x: (x["days_until"] is None, x["days_until"]))

    layer_e = None
    if deepd:
        layer_e = {
            "schema": deepd.get("schema"),
            "counts": deepd.get("counts"),
            "bindings_declared": deepd.get("bindings"),
            "note": "the deep cross-product: sectors_frameworks, industries, accounts (the spine), layer0, board_axes, deadlines - consumed from the published artifact, never re-derived here",
        }

    counts = {
        "regimes": len(ewd.get("jurisdictions", [])),
        "article_rows": len(layer_a),
        "mapped_concepts": len({a["mapped_concept"] for a in layer_a}),
        "board_axes": len(layer_b),
        "axes_measured": sum(1 for a in layer_b if a["status"] == "MEASURED"),
        "deadlines": len(layer_c),
        "deadlines_within_90_days": sum(
            1 for c in layer_c if c["days_until"] is not None and 0 <= c["days_until"] <= 90),
    }

    index = {
        "schema": "csoai.regulation-measurement-index/0.1",
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "inputs": inputs,
        "counts": counts,
        "layer_a_articles": layer_a,
        "layer_b_measurements": layer_b,
        "layer_c_deadlines": layer_c,
        "layer_e_deep_index": layer_e,
        "layer_d_declared_gap": {
            "missing_binding": "concept->axis",
            "statement": ("Article rows map to governance concepts and the board carries "
                          "measured axes, but no published artifact binds concepts to axes. "
                          "Article-to-measurement linkage is therefore ABSENT here — "
                          "deliberately, rather than invented. Sealing that binding is the "
                          "next artifact in this mine."),
            "concepts": sorted({a["mapped_concept"] for a in layer_a}),
        },
        "signature_status": {
            "ed25519": "UNSIGNED — signing key not staged; the artifact is sha256-bound only.",
            "content_sha256": None,
        },
    }
    body = json.dumps(index, sort_keys=True, ensure_ascii=False).encode("utf-8")
    index["signature_status"]["content_sha256"] = sha256_bytes(body)
    out = json.dumps(index, sort_keys=False, ensure_ascii=False, indent=1).encode("utf-8")

    print("[mine] counts:", json.dumps(counts))
    print("[mine] content_sha256", index["signature_status"]["content_sha256"][:16])

    token = os.environ.get("HF_TOKEN", "").strip()
    if not token:
        print("[mine] no HF_TOKEN; artifact stays in the run log")
        return 0
    from huggingface_hub import HfApi
    api = HfApi(token=token)
    url = api.upload_file(
        path_or_fileobj=out,
        path_in_repo="mine/regulation-measurement-index-latest.json",
        repo_id=MINE_REPO,
        repo_type="dataset",
        commit_message="regulation-measurement mine index %s (A:%d articles B:%d axes C:%d deadlines)"
                       % (today, counts["article_rows"], counts["board_axes"], counts["deadlines"]),
    )
    print("[mine] uploaded:", url)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env bash
# Re-check the board yourself. No account, no key, no CSOAI code.
set -euo pipefail
echo "== live board =="
curl -fsS https://councilof.ai/api/gspc | python3 -c '
import json,sys
d=json.load(sys.stdin); t=d["totals"]
print("slots   :", t["axes"])
print("measured:", t["measured_axes"])
print("public  :", t["public_count"])
derived_measured = sum(1 for a in d["axes"] if a["status"]=="MEASURED")
print("derived from the axis array:", len(d["axes"]), "slots,", derived_measured, "measured")
assert len(d["axes"])==t["axes"], "slot count does not match the axis array"
assert derived_measured==t["measured_axes"], "measured count does not match the axis array"
print("OK - the printed totals are derived from the array, not typed")
'
echo
echo "== transparency root =="
curl -fsS https://councilof.ai/root.json | head -c 400; echo
echo
echo "Verify any single card (free, no account): https://councilof.ai/gspc-verify"
echo "By hand: https://councilof.ai/signed/HOW-TO-VERIFY.md"

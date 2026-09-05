#!/usr/bin/env bash
# Re-check the board yourself. No account, no key, no CSOAI code beyond curl and python3.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
echo "== live board =="
curl -fsS https://councilof.ai/api/gspc | python3 -c '
import json,sys
d=json.load(sys.stdin); t=d["totals"]
print("lid     :", t.get("lid"))
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
echo "== transparency root: recompute the Merkle root from card_sha256[] =="
curl -fsS https://councilof.ai/root.json | python3 -c '
import hashlib,json,sys
r=json.load(sys.stdin)
leaves=[bytes.fromhex(h) for h in r["card_sha256"]]
assert len(leaves)==r["card_count"], "REJECT: len(card_sha256) != card_count"
level=leaves
while len(level)>1:
    if len(level)%2==1: level=level+[level[-1]]   # odd node paired with itself, as root.json states
    level=[hashlib.sha256(level[i]+level[i+1]).digest() for i in range(0,len(level),2)]
root=level[0].hex() if level else None
print("as_of      :", r["as_of"])
print("card_count :", r["card_count"])
print("merkle_root:", r["merkle_root"])
print("recomputed :", root)
assert root==r["merkle_root"], "REJECT: recomputed root differs from merkle_root"
print("OK - the root commits to exactly these", r["card_count"], "cards")
'
echo
if [ -f "$HERE/SNAPSHOT.json" ]; then
  echo "== this snapshot vs live =="
  python3 - "$HERE/SNAPSHOT.json" <<'PY'
import json,sys,urllib.request
s=json.load(open(sys.argv[1]))
live=json.load(urllib.request.urlopen(urllib.request.Request("https://councilof.ai/root.json", headers={"User-Agent": "check-board.sh"})))
print("snapshot as_of:", s["as_of"], "| live as_of:", live["as_of"])
print("snapshot root :", s["merkle_root"])
print("live root     :", live["merkle_root"])
print("SAME" if s["merkle_root"]==live["merkle_root"] else "MOVED - the live board has changed since this snapshot; the live GET wins")
PY
fi
echo
echo "Verify any single card (free, no account): https://councilof.ai/gspc-verify"
echo "By hand: https://councilof.ai/signed/HOW-TO-VERIFY.md"

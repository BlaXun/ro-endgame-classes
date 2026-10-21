#!/usr/bin/env python3
"""add_kept.py: to every spec here, add the transcendent (or base) class's reference runs cast by the
new class at 175 ("L175_kept_<id>"). A class keeps those skills and they grow with its stats: the
Rune Knight's kept Bowling Bash out-damaged its own skills. Idempotent."""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in sorted(HERE.glob("*.json")):
    d = json.loads(p.read_text())
    runs = d["runs"]
    ids = {r["id"] for r in runs}
    new_class = next((r["class"] for r in runs if r["class"] >= 4060), None)
    if new_class is None:
        continue
    add = []
    for r in runs:
        if r["class"] < 4060 and f"L175_kept_{r['id']}" not in ids and "versus" not in r:
            k = {**r, "id": f"L175_kept_{r['id']}", "class": new_class, "level": 175, "versus": r["id"]}
            k.pop("aim", None)
            if any(x.get("user") == "fem" for x in runs if x["class"] == new_class):
                k["user"] = "fem"
            add.append(k)
    if add:
        d["runs"] = runs + add
        p.write_text(json.dumps(d, indent=1) + "\n")
        print(p.name, "+", len(add))

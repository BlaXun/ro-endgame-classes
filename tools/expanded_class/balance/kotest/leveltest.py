#!/usr/bin/env python3
"""leveltest.py <spec.json> [--only id,id] [--levels 100,175]

The rule: base level must not enter a skill's damage. For each run of a class spec (the
run_specs.py format) the skill is cast with the same base stats, weapon and job level at two
base levels, on the anchor, and its middle hit compared (the middle one, so an odd critical does not count;
where the two differ the skill is measured twice more, and it counts as different only if the levels' results
do not overlap). Stats are fixed at 99 each, so
nothing but the level differs (MaxHP and MaxSP do rise with the level: a skill whose damage
is built on them, such as Dragon Breath, shows up here and is judged apart).
Prints one line per run; exits 1 if any differs by more than 3 % (weapon damage varies a
little from cast to cast).
"""
import json, os, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
a = sys.argv[1:]
spec = json.loads(Path(a[0]).read_text())
only = a[a.index("--only") + 1].split(",") if "--only" in a else None
levels = a[a.index("--levels") + 1].split(",") if "--levels" in a else ["100", "175"]
seen, bad, out = set(), 0, {}
for run in spec["runs"]:
    key = (run["class"], run["skills"], run.get("weapon"))
    if key in seen or run["class"] < 4060 and run["class"] not in (4211, 4212, 4215, 4239, 4240, 4190) or (only and run["id"] not in only):
        continue
    seen.add(key)
    def once(lv, secs):
        user = run.get("user", "player")
        args = ["python3", "kotest/measure2.py", user, user + "123", str(run["class"]), str(run["weapon"]), str(run.get("ammo", 0)),
                str(run["skills"]), str(run["levels"]), str(secs), run.get("how", "mob"), run.get("pre") or "-", "0.5"]
        env = {**os.environ, "BLEVEL": lv, "FIXSTATS": "99/99/99/99/99/99", "DUMMY": "dummy#6", "EXTRA": run.get("extra", ""),
               "STATS": run.get("stats", ""), "COUNT": str(run.get("count", "")), "LEFT": str(run.get("left", "")), "CARTLOAD": run.get("cartload", "")}
        r = subprocess.run(args, cwd=HERE, env=env, capture_output=True, text=True, timeout=secs * 3 + 140).stdout
        d = next((json.loads(l) for l in r.splitlines() if l.startswith("{")), {})
        return d.get("median_hit", 0)
    per = {lv: [once(lv, 20)] for lv in levels}
    def differ():
        lo = min(min(v) for v in per.values()); hi = max(max(v) for v in per.values())
        # the levels differ if their ranges do not overlap and the gap is more than 3 %
        a, b = (per[lv] for lv in levels[:2])
        apart = max(a) < min(b) or max(b) < min(a)
        return hi == 0 or (apart and (hi - lo) / hi > 0.03)
    if differ():   # a skill whose hits vary (arrows, a wide weapon range) can look different once: look twice more, longer
        for lv in levels:
            per[lv] += [once(lv, 40), once(lv, 40)]
    same = not differ()
    bad += not same
    per = {lv: (v[0] if len(v) == 1 else v) for lv, v in per.items()}
    out[run["id"]] = per
    print("%-4s %-30s %s" % ("same" if same else "DIFF", run["id"], "  ".join("level %s: %s a hit" % (k, v) for k, v in per.items())), flush=True)
if "--json" in a:
    Path(a[a.index("--json") + 1]).write_text(json.dumps(out, indent=1))
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""tune.py <class> <round> [--apply]: from a class's round results, the next factors.

Reads level175/results/phase3/<class>_r<round>.json and the class's spec. For every run aimed at
1.35-1.65 (an own single-target rotation at 175) that is outside the band, the rotation's skills
are scaled so that it lands on 1.5. For every area run aimed at "at most 0.55 of an own run", if
it is over 0.55 of that run AFTER the single-target change, its skills are scaled down to 0.5.
Skills are the percent factors in the mod's lua files (NAME = percent); a skill without one
counts as 100 and gets an entry in third_classes.lua. Prints the changes; --apply writes them.
"""
import json, re, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]   # ro-endgame-classes
DEV = REPO.parent                            # the results live in DEV/level175
cls, rnd = sys.argv[1], sys.argv[2]
EXPANDED = {"kagerou_oboro", "rebellion", "star_emperor", "soul_reaper", "super_novice"}
LUA = REPO / "mods" / ("expanded-classes" if cls in EXPANDED else "transcendent-third-classes") / "lua"
spec = json.loads((REPO / f"tools/transcendent-third-classes/level175/{cls}.json").read_text())
res = json.loads((DEV / f"level175/results/phase3/{cls}_r{rnd}.json").read_text())
# Recompute every value from its measurements: three runs a method, the middle one, the best method.
# (Two rigs ran round 1 with a run_specs.py that took the middle of all runs across methods, which
# gave 0 for a caster whose paced method works and whose fixed-pace methods do not.)
for rid, v in res.items():
    groups = [v["all"][i:i + 3] for i in range(0, len(v["all"]), 3)]
    if groups:
        v["value"] = max(sorted(g)[len(g) // 2] for g in groups)
for rid, v in res.items():
    ref = res.get(v.get("versus") or "", {})
    v["ratio"] = round(v["value"] / ref["value"], 2) if ref.get("value") else None
names = {}
for m in re.finditer(r"- Id: (\d+)\s*\n\s+Name: (\S+)", (DEV / "rathena-level175/db/pre-re/skill_db.yml").read_text(encoding="utf-8", errors="replace")):
    names[m.group(1)] = m.group(2)
luas = {p: p.read_text() for p in sorted(LUA.glob("*.lua"))}
def factor(name):
    for p, t in luas.items():
        m = re.search(rf"^\s*{name}\s*=\s*(\d+)\s*,", t, re.M)
        if m:
            return int(m.group(1)), p
    return 100, None
runs = {r["id"]: r for r in spec["runs"]}
def own(run):   # the rotation's skills that are the class's own (not a kept first/second/transcendent skill, not a buff cast on yourself)
    out = []
    for s in str(run["skills"]).split(","):
        n = names.get(s.rstrip("s"), "")
        if s != "attack" and n != "RA_DETONATOR" and re.match(r"(RK|GC|AB|WL|RA|NC|SC|LG|SR|WA|MI|WM|SO|GN|KO|OB|KG|RL|SJ|SP)_", n):
            out.append(n)
    return out
scale, notes = {}, []
single_after = {}
# Owner, 2026-10-11: kept skills grow freely with the character. Where a kept single-target skill
# passes 1.5x by itself, the class's own single-target skills are lifted just above it (4 %), so the
# new skills stay the better choice; the target for this class is then that figure, not 1.5.
# (not a burst: Asura Strike measured with its SP refilled is no sustained figure)
kept = [v["ratio"] for rid, v in res.items() if rid.startswith("L175_kept_") and "_area" not in rid and "burst" not in rid and v.get("ratio")]
TARGET = max([1.5] + [round(k * 1.04, 2) for k in kept])
LOW, HIGH = round(TARGET * 0.9, 2), round(TARGET * 1.1, 2)
notes.append("target for own single-target skills: %.2fx (%.2f-%.2f)%s" % (TARGET, LOW, HIGH, "  [kept skill at %.2fx]" % max(kept) if kept and TARGET > 1.5 else ""))
for rid, r in runs.items():
    v = res.get(rid)
    if not v or not v.get("ratio") or r.get("aim") != [1.35, 1.65] or "burst" in rid:
        continue
    s = 1.0 if LOW <= v["ratio"] <= HIGH else TARGET / v["ratio"]
    single_after[rid] = v["value"] * s
    notes.append("%-34s %6d  %.2fx -> %s" % (rid, v["value"], v["ratio"], "kept" if s == 1.0 else "x%.2f" % s))
    if s != 1.0:
        for n in own(r):
            scale[n] = s if n not in scale else min(scale[n], s)   # a skill in two rotations: the smaller raise
for rid, r in runs.items():
    v = res.get(rid)
    if not v or r.get("aim") != [0.0, 0.55] or r.get("versus") not in single_after or "Unlimit" in rid:
        continue   # (Unlimit + Aimed Bolt is a buffed single-target run, not an area skill)
    base = single_after[r["versus"]]
    now = v["value"] * min([scale.get(n, 1.0) for n in own(r)] or [1.0])
    share = now / base if base else 0
    if share > 0.55:
        s = 0.5 * base / v["value"]
        for n in own(r):
            scale[n] = s if n not in scale else min(scale[n], s)
        notes.append("%-34s %6d  %.2f of own single -> x%.2f" % (rid, v["value"], share, s))
    else:
        notes.append("%-34s %6d  %.2f of own single: kept" % (rid, v["value"], share))
print("\n".join(notes))
if "--all" in sys.argv:
    for rid, v in res.items():
        print("   %-36s %6d  %s" % (rid, v["value"], v["ratio"] if v["ratio"] is not None else ""))
changes = {}
for n, s in sorted(scale.items()):
    old, path = factor(n)
    new = max(1, round(old * s))
    if new != old:
        changes[n] = (old, new, path)
        print("  %-24s %4d -> %4d  (%s)" % (n, old, new, path.name if path else "new entry, third_classes.lua"))
if "--apply" in sys.argv:
    for n, (old, new, path) in changes.items():
        if path is None:
            path = LUA / "third_classes.lua"
            t = luas[path]
            t = t.replace("local FACTOR = {\n", "local FACTOR = {\n  %-21s = %d,\n" % (n, new), 1)
        else:
            t = re.sub(rf"^(\s*{n}\s*=\s*)\d+(\s*,)", rf"\g<1>{new}\2", luas[path], count=1, flags=re.M)
        luas[path] = t
        path.write_text(t)
    print("applied %d change(s)" % len(changes))

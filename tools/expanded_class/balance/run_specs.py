#!/usr/bin/env python3
"""Measure a class mod's balance from its spec file and compare it with the aims.

    python3 tools/expanded_class/balance/run_specs.py tools/<mod>/balance.json
    ... --only GX_CI,AX_SB      measure only these runs (and what they are compared with)
    ... --no-load               use the mods the test server already has loaded

A spec file lists runs. Each run is one rotation on the measuring template
(kotest's build#: base 99, job 70, a STR/AGI, DEX or INT/DEX build by class)
against a test dummy for SECONDS, and its result is damage per second on that
one target (for an area skill: on each target). A run may name another run as
`versus` and an `aim`, a band for the ratio of the two.

Run fields (only id, class, weapon, skills and levels are required):
    id        a name for the run
    class     the job id (4013 Assassin Cross, 4065 Guillotine Cross T, ...)
    weapon    item id, usually a test weapon from kotest/db/item_db.yml
    ammo      ammunition item id (arrows, bullets), 0 for none
    left      item id of a second weapon worn in the left hand (dual wielding)
    stats     "int", "dex" or "str": that stat build instead of the class's usual one
    level     base level, with every stat point spent in the build's order (the full
              build: 99 for a transcendent class, up to 175 for a third class);
              without it the template is the fixed level-99 build
    user      the test account to play (default "player"; "fem" for female-only classes)
    skills    comma-separated skill ids cast in turn; "attack" for auto-attacks;
              a trailing "s" casts on yourself (2036s)
    levels    their levels, comma-separated
    how       "mob" (cast on the dummy), "pos" (on the dummy's cell) or "near"
              (on a free cell two to its east: traps, which cannot go beside it)
    pre       "id:lv[:self][:once]" casts before the rotation and every 10 s
    extra     kotest commands before the dummy, ";"-separated (a shield, a dragon)
    cartload  "item:n": n of an item moved into the cart before the run (cart skills
              grow with its weight; "989:79", Emperium Anvils, fills it to 7900; a
              full 8000 is refused)
    count     comma-separated skill ids whose hits also count (a skill that hits
              under another id, as Crazy Weed's units do as GN_CRAZYWEED_ATK)
    charge    "id:lv:n": cast a self skill n times before the dummy (charms:
              "3016:1:10" holds ten water charms through the run)
    dummy     "anchor" (anchored, with the Abysmal Knight's defences, size, race and
              element: the level 175 work's target), "anchored" (default: never hits back, cannot be knocked back),
              "normal" (hits back; use it for skills that knock targets away) or
              "mdef" (anchored, with high magic defence: MDEF 40, INT 80, VIT 50)
    method    "step" (requests at a fixed pace: instant skills), "paced" (one
              cast at a time: cast-time skills) or "best" (both, the higher)
    step      seconds between requests for "step" (default 0.1), or a list of
              them to try, the highest kept (casters' rhythms differ: [1.0, 1.5])
    seq       true: one skill per step, in turn
    repeat    measurements per method, the highest kept (default 2)
    versus    the id of the run this one is compared with
    aim       [low, high] for this run's result / versus's result

A spec may set "defaults": {"dummy": "anchor", "repeat": 3, "median": true}: every
run on that dummy, measured three times, the middle value kept (without
"median" the highest is).

The rig must be set up (setup.sh) and the mod generated (its build.py).
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]   # the repository: a spec loads mods/<mod>


DEFAULTS = {}   # the spec's "defaults": dummy, repeat, median


def measure(run, seconds):
    method = run.get("method", "step")
    steps = run.get("step", 0.1)
    steps = steps if isinstance(steps, list) else [steps]
    modes = ([("step", s) for s in steps] if method != "paced" else []) + ([("paced", 1)] if method != "step" else [])
    results, by_mode = [], []
    for mode, step in modes:
        by_mode.append([])
        if mode == "paced":
            tail = ["1", "paced"]
        else:
            tail = [str(step)] + (["seq"] if run.get("seq") else [])
        user = run.get("user", "player")
        args = ["python3", "kotest/measure2.py", user, user + "123", str(run["class"]), str(run["weapon"]),
                str(run.get("ammo", 0)), str(run["skills"]), str(run["levels"]), str(seconds),
                run.get("how", "mob"), run.get("pre") or "-"] + tail
        extra = run.get("extra", "")
        if run.get("charge"):
            sid, lv, n = run["charge"].split(":")
            extra = ";".join([f"skill {sid} {lv} self;wait 0.8"] * int(n) + ([extra] if extra else []))
        env = {**os.environ, "BLEVEL": str(run.get("level", "")), "EXTRA": extra, "LEFT": str(run.get("left", "")), "STATS": run.get("stats", ""), "COUNT": str(run.get("count", "")), "CARTLOAD": run.get("cartload", ""),
               "DUMMY": {"anchored": "dummy#4", "mdef": "dummy#5", "anchor": "dummy#6"}.get(run.get("dummy", DEFAULTS.get("dummy", "anchored")), "dummy")}
        for _ in range(int(run.get("repeat", DEFAULTS.get("repeat", 2)))):
            try:
                out = subprocess.run(args, cwd=HERE, env=env, capture_output=True, text=True,
                                     timeout=seconds * 3 + 120).stdout
            except subprocess.TimeoutExpired:
                continue
            for line in out.splitlines():
                if line.startswith("{"):
                    d = json.loads(line)
                    results.append(d["dps"] + sum(d["other_dps"].values()))
                    by_mode[-1].append(results[-1])
    if DEFAULTS.get("median") and results:   # the spec's "median": true: each method's middle run, the best method kept
        return max(sorted(m)[len(m) // 2] for m in by_mode if m), results
    return max(results) if results else 0, results


def main():
    ap = argparse.ArgumentParser(description="Measure a class mod's balance from its spec file.")
    ap.add_argument("spec", type=Path)
    ap.add_argument("--only", default="", help="comma-separated run ids")
    ap.add_argument("--no-load", action="store_true", help="do not (re)start the server with the spec's mods")
    ap.add_argument("--json", type=Path, help="also write every run's value, measurements and ratio here")
    args = ap.parse_args()
    spec = json.loads(args.spec.read_text())
    DEFAULTS.update(spec.get("defaults", {}))
    runs = {r["id"]: r for r in spec["runs"]}
    wanted = [i for i in args.only.split(",") if i] or list(runs)
    for i in list(wanted):
        v = runs[i].get("versus")
        if v and v not in wanted:
            wanted.insert(0, v)
    if not args.no_load:
        mods = [str(ROOT / m) for m in spec.get("load", [])] + [str(HERE / "kotest")]
        out = subprocess.run([str(HERE / "up.sh")] + mods, capture_output=True, text=True)
        status = [l for l in out.stdout.splitlines() if l.startswith("map.log")]
        print(status[0] if status else out.stdout[-400:], flush=True)
    seconds = int(spec.get("seconds", 40))
    value, outside, record = {}, 0, {}
    print(f"{'run':28} {'dmg/s':>7}  {'ratio':>6}  aim         all measurements", flush=True)
    for i in (r for r in runs if r in wanted):
        run = runs[i]
        value[i], allv = measure(run, seconds)
        ratio, verdict = "", ""
        if run.get("versus") in value and value[run["versus"]]:
            r = value[i] / value[run["versus"]]
            ratio = f"{r:.2f}"
            if "aim" in run:
                lo, hi = run["aim"]
                ok = lo <= r <= hi
                outside += not ok
                verdict = f"{lo:.2f}-{hi:.2f} {'ok' if ok else 'OUT'}"
        print(f"{i:28} {value[i]:7}  {ratio:>6}  {verdict:11} {allv}", flush=True)
        record[i] = {"value": value[i], "all": allv, "versus": run.get("versus"), "ratio": float(ratio) if ratio else None,
                     "aim": run.get("aim")}
        if args.json:
            args.json.write_text(json.dumps(record, indent=1))
    sys.exit(1 if outside else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""The soft cap's invariant test (level175-softcap-plan.md, step 9.1).

    invariant.py <rig dir> record <file>     write what the test characters come out as
    invariant.py <rig dir> check <file>      the same, compared with a recorded file; exit 1 on any difference

Every test character has base stats of 99 or less. For each one the status
window is read back as the server sends it: every stat as base + bonus, ATK,
MATK, DEF, MDEF, HIT, FLEE, critical, ASPD (as amotion), MaxHP, MaxSP and max
weight; for the casters the cast time of a level 10 spell too. Record it on a
build without the soft cap, check it on one with it. The rig must be up with
the sctest directory beside this file loaded as a mod.
"""
import json
import subprocess
import sys

CASES = {
    1: ("High Wizard 99 INT 99 DEX, Blessing, Increase AGI", (89, 10)),
    2: ("Assassin Cross 99 AGI, katar, Berserk Potion", None),
    3: ("Lord Knight 99 VIT 99 STR", None),
    4: ("Sniper exactly 99 DEX +30, Blessing", None),
    5: ("Novice 1/1", None),
    6: ("Knight, mixed build", None),
    7: ("Baby Knight at 80", None),
    8: ("High Priest, Blessing, Gloria, Angelus", (79, 10)),
    9: ("High Wizard 99 DEX, +51 bonus DEX: instant cast", (89, 10)),
    10: ("Super Novice", (21, 10)),
    11: ("Star Gladiator", None),
    12: ("Soul Linker", None),
}


def client(rig, cmds, user="player"):   # an account with no companions: theirs would cast too
    p = subprocess.run(["python3", "roclient.py", "--user", user, "--pass", user + "123", "do"] + cmds,
                       cwd=rig, capture_output=True, text=True, timeout=120)
    out = []
    for line in p.stdout.splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def measure(rig, setup, cast=None):
    """setup: ScTest commands. Returns the status window, and the cast time when a spell is given."""
    cmds = []
    for s in setup:
        cmds += ["whisper npc:ScTest " + s, "wait 2"]
    cmds += ["whisper npc:ScTest refresh", "wait 3", "stats"]
    if cast:
        cmds += ["clear", "skill-pos %d %d 170 375" % cast, "dump-events 2 skill_cast,skill_fail"]
    ev = client(rig, cmds)
    st = next((e for e in reversed(ev) if e.get("ev") == "stats"), None)
    if st is None:
        raise SystemExit("no status window came back: %r" % ev[-5:])
    res = {k: v for k, v in st.items() if k not in ("ev", "t", "weight", "status_point")}
    if cast:
        fails = [e for e in ev if e.get("ev") == "skill_fail"]
        casts = [e for e in ev if e.get("ev") == "skill_cast" and e.get("skill") == cast[0]]
        res["cast_ms"] = "failed" if fails else (casts[0]["cast_ms"] if casts else 0)
    return res


def main():
    rig, mode, path = sys.argv[1:4]
    got = {}
    for n, (name, cast) in CASES.items():
        got[str(n)] = dict(name=name, **measure(rig, ["case#%d" % n + ("#9" if n == 9 else "")], cast))   # 9: the High Wizard's job bonus DEX
        print(n, name, json.dumps({k: v for k, v in got[str(n)].items() if k != "name"}), flush=True)
    if mode == "record":
        json.dump(got, open(path, "w"), indent=1)
        print("recorded", path)
        return
    want = json.load(open(path))
    bad = 0
    for n in want:
        for k in sorted(set(want[n]) | set(got.get(n, {}))):
            if want[n].get(k) != got.get(n, {}).get(k):
                bad += 1
                print("DIFFERENT case %s (%s) %s: recorded %r, now %r" % (n, want[n]["name"], k, want[n].get(k), got.get(n, {}).get(k)))
    print("invariant: %d cases, %d differences" % (len(want), bad))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

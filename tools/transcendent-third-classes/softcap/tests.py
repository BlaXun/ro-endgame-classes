#!/usr/bin/env python3
"""The soft cap's tests with the class mod loaded (level175-softcap-plan.md, step 9, tests 3 to 7).

    tests.py <rig dir> [out.json]

The rig must be up with the class mod and the sctest directory loaded. Prints
one line per check and exits 1 if any fails. Test 1 (the invariant) is
invariant.py; run it against this rig too.
"""
import json
import re
import sys

from invariant import client, measure

RIG = sys.argv[1]
results = []


def check(test, what, want, got, ok=None):
    ok = (want == got) if ok is None else ok
    results.append(dict(test=test, what=what, want=want, got=got, ok=bool(ok)))
    print("%s  %-4s %s: want %s, got %s" % ("ok  " if ok else "FAIL", test, what, want, got), flush=True)


def tell(cmds, user="player", pattern=r"ScTest: (.*)"):
    """Whisper ScTest commands; returns the ScTest lines that came back."""
    seq = []
    for c in cmds:
        seq += [c if c.startswith(("wait", "skill", "clear", "dump", "stats")) else "whisper npc:ScTest " + c, "wait 1.5"]
    out = []
    for e in client(RIG, seq, user):
        m = re.search(pattern, e.get("text") or "")
        if m:
            out.append(m.group(1))
    return out


def info(user="player"):
    line = [l for l in tell(["info"], user) if l.startswith("info")][-1]
    m = re.match(r"info job (\d+) blvl (\d+) jlvl (\d+) points (\d+) stats ([\d/]+) maxweight (\d+) next (\d+)", line)
    return dict(job=int(m[1]), blvl=int(m[2]), jlvl=int(m[3]), points=int(m[4]),
                stats=[int(x) for x in m[5].split("/")], maxweight=int(m[6]), next=int(m[7]))


WARLOCK, GX, KAGEROU = 4061, 4065, 4211
SG = (89, 10)   # Storm Gust 10: 15 s before DEX

ONLY = [a[7:] for a in sys.argv if a.startswith("--only=")]
if ONLY:   # --only=4: just that test
    import io
    src = open(__file__).read().split("# --- ")
    keep = [p for p in src[1:] if p.split(".")[0] in ONLY]
    exec("".join("# --- " + p for p in keep).split("bad = [r for r in results")[0])
    bad = [r for r in results if not r["ok"]]
    print("%d checks, %d failed" % (len(results), len(bad)))
    sys.exit(1 if bad else 0)

# --- 3. a level 175 character with 150 base DEX ----------------------------------
lo = measure(RIG, ["raw#%d#175#70" % WARLOCK, "stat#5#98"], SG)            # 99 base DEX
hi = measure(RIG, ["raw#%d#175#70" % WARLOCK, "stat#5#200"], SG)           # as far as it goes
check("3", "base DEX stops at", 150, hi["dex"][0])
check("3", "status window bonus at 150 base = bonus at 99 base (no negative bonus)", lo["dex"][1], hi["dex"][1])
check("3", "HIT rises by the effective part, (150-99)/3 = 17", lo["hit"] + 17, hi["hit"])
check("3", "cast time at 150 base DEX = cast time at 99 base DEX", lo["cast_ms"], hi["cast_ms"])
check("3", "... and it is not instant", True, hi["cast_ms"] > 0)
jb = hi["dex"][1]
below = measure(RIG, ["raw#%d#175#70" % WARLOCK, "stat#5#200", "bonus#5#%d" % (50 - jb)], SG)
at = measure(RIG, ["raw#%d#175#70" % WARLOCK, "stat#5#200", "bonus#5#%d" % (51 - jb)], SG)
check("3", "150 base DEX, +50 bonus DEX: not instant (15000 * 1/150 = 100 ms)", 100, below["cast_ms"])
check("3", "150 base DEX, +51 bonus DEX: instant", 0, at["cast_ms"])
classic = measure(RIG, ["raw#%d#175#70" % WARLOCK, "stat#5#98", "bonus#5#%d" % (50 - jb)], SG)
check("3", "99 base DEX, +50 bonus DEX: the same 100 ms", 100, classic["cast_ms"])
st = measure(RIG, ["raw#%d#175#70" % WARLOCK, "stat#4#200", "stat#2#200"])
st99 = measure(RIG, ["raw#%d#175#70" % WARLOCK, "stat#4#98", "stat#2#98"])
check("3", "150 base INT counts as 116: MATK max is that of INT 116 + bonus",
      True, st["matk_max"] > st99["matk_max"], ok=st["matk_max"] > st99["matk_max"])
results[-1]["got"] = "%d (99 base: %d)" % (st["matk_max"], st99["matk_max"])

# --- 5. spend, relog, reset -------------------------------------------------------
tell(["raw#%d#175#70" % WARLOCK])
p0 = info()["points"]
tell(["up#5#200"])
a = info()
check("5", "DEX raised with stat points stops at", 150, a["stats"][4])
check("5", "1 to 150 costs 1334 points", 1334, p0 - a["points"])
b = info()   # a new login
check("5", "after relog: DEX and points kept", (150, a["points"]), (b["stats"][4], b["points"]))
tell(["resetstat"])
c = info()
check("5", "reset refunds every point", p0, c["points"])
check("5", "stat points of a transcendent class at 175 (3545 + 52)", 3597, p0)

# --- 6. EXP from 99 to 175 --------------------------------------------------------
tell(["raw#%d#99#70" % WARLOCK])
i99 = info()
check("6", "EXP 99 -> 100 is the transcendent 98 -> 99", 343210000, i99["next"])
tell(["exp#1"])
i100 = info()
check("6", "one level through EXP", 100, i100["blvl"])
check("6", "level 100 gives floor(99/5)+3 = 22 stat points", 22, i100["points"] - i99["points"])
check("6", "EXP 100 -> 101", 347786000, i100["next"])
tell(["exp#40", "exp#35"])
i175 = info()
check("6", "75 levels through EXP reach", 175, i175["blvl"])
check("6", "stat points at 175 equal a character set to 175", p0, i175["points"])
tell(["exp#1"])
check("6", "no level beyond 175", 175, info()["blvl"])

# --- 7. the stat cap and the level cap per class ----------------------------------
for job, name, lvl, cap in ((GX, "Guillotine Cross", 175, 150), (KAGEROU, "Kagerou", 175, 150),
                            (4215, "Rebellion", 175, 150), (4239, "Star Emperor", 175, 150), (4240, "Soul Reaper", 175, 150),
                            (4010, "High Wizard", 99, 99), (7, "Knight", 99, 99), (4030, "Baby Knight", 99, 80),
                            (25, "Ninja", 99, 99), (24, "Gunslinger", 99, 99), (4047, "Star Gladiator", 99, 99),
                            (4049, "Soul Linker", 99, 99), (23, "Super Novice", 99, 99)):
    tell(["raw#%d#175#70" % job, "points#3000", "up#1#200", "stat#2#200"])
    i = info()
    check("7", "%s: job taken" % name, job, i["job"])
    check("7", "%s: base level stops at" % name, lvl, i["blvl"])
    check("7", "%s: STR with stat points, AGI by script stop at" % name, (cap, cap), (i["stats"][0], i["stats"][1]))

# --- 4. Marionette Control --------------------------------------------------------
# 'axe' is the puppeteer, 'player' the target, in one party, on the same cell.
def marionette(caster_setup, target_setup):
    """The target's DEX [base, bonus] while Marionette Control is on it."""
    import subprocess, time
    tell(["leaveparty"], "axe"); tell(["leaveparty"])
    tell(caster_setup, "axe")
    pid = [l for l in tell(["mkparty", "party"], "axe") if l.startswith("party")][-1].split()[1]
    tell(target_setup + ["joinparty#" + pid])
    tgt = subprocess.Popen(["python3", "roclient.py", "--user", "player", "--pass", "player123", "do",
                            "wait 10", "stats"], cwd=RIG, stdout=subprocess.PIPE, text=True)
    time.sleep(3)
    client(RIG, ["wait 1", "skill 396 1 2000001", "wait 5"], "axe")
    out = tgt.communicate()[0]
    st = [json.loads(l) for l in out.splitlines() if '"ev": "stats"' in l]
    return st[-1]["dex"] if st else None


if "--no-marionette" not in sys.argv:
    clown = ["raw#4020#99#70", "stat#5#80"]            # Clown, 81 base DEX: gives 40
    jbw = 9                                            # a Warlock's job bonus DEX at job 70
    check("4", "target 1 base DEX: gets the Clown's 81/2 = 40", [1, jbw + 40],
          marionette(clown, ["raw#%d#99#70" % WARLOCK]))
    check("4", "target 70 base DEX: total stops at 99", [70, 29],
          marionette(clown, ["raw#%d#99#70" % WARLOCK, "stat#5#69"]))
    check("4", "target 150 base DEX (counts 116): gets nothing", [150, jbw],
          marionette(clown, ["raw#%d#175#70" % WARLOCK, "stat#5#200"]))
    check("4", "Minstrel with 150 base DEX gives (99 + 51/3)/2 = 58, not 75", [1, jbw + 58],
          marionette(["raw#4075#175#70", "stat#5#200", "learn#396"], ["raw#%d#99#70" % WARLOCK]))

bad = [r for r in results if not r["ok"]]
if len(sys.argv) > 2 and not sys.argv[2].startswith("--"):
    json.dump(results, open(sys.argv[2], "w"), indent=1)
print("%d checks, %d failed" % (len(results), len(bad)))
sys.exit(1 if bad else 0)

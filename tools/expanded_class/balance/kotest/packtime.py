#!/usr/bin/env python3
"""packtime.py user job weapon level skills levels [how=mob|self|pos] [step] [pre]

How long the full build of a class at a level takes to kill the pack of five (KoTest pack5: five
monsters with an Abysmal Knight's HP and defences, clustered beside the character, standing
still). The skills are cast in turn at the nearest one left ("mob"), on yourself ("self": a
skill centred on the caster) or on the nearest one's cell ("pos"); "attack" auto-attacks.
SP is refilled every 3 s, as in measure2.py. Prints one JSON line; "seconds" is the server's
own time from the spawn to the fifth death, null if the pack outlived LIMIT (default 180 s).
"""
import json, os, re, subprocess, sys, time
a = sys.argv[1:]
user, job, weapon, level, sids, lvs = a[:6]
how = a[6] if len(a) > 6 else "mob"
step = float(a[7]) if len(a) > 7 else 0.3
pre = [x.split(":") for x in a[8].split(",")] if len(a) > 8 and a[8] not in ("", "-") else []
limit = float(os.environ.get("LIMIT", "180"))
sids, lvs = sids.split(","), lvs.split(",")
PLAIN = os.environ.get("PACK") in ("plain", "wide")   # PACK=plain: five monsters without defence or element (casters)
WIDE = os.environ.get("PACK") == "wide"             # PACK=wide: eight of them around the caster, spread over 9x9 cells: the size of an area counts
T = "mob:25508" if PLAIN else "mob:25507"
p = subprocess.Popen(["python3", "roclient.py", "--user", user, "--pass", user + "123", "run", "-"],
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
def send(*ls):
    for l in ls:
        p.stdin.write(l + "\n")
    p.stdin.flush()
stats = os.environ.get("STATS", "")
send(f"whisper npc:KoTest build#{job}#{weapon}#{stats}#{level}", "wait 3", "whisper npc:KoTest rlkit", "wait 1")
for c in [c for c in os.environ.get("EXTRA", "").split(";") if c]:
    send(c)
for q in pre:
    send(f"skill {q[0]} {q[1]} self", "wait 1")
send("whisper npc:KoTest heal", "whisper npc:KoTest pack5" + ("#2" if WIDE else "#1" if PLAIN else ""), "wait 1.5", "mobs")
ticks = int(limit / step)
for i in range(ticks):
    if i % max(1, int(3 / step)) == 0:
        send("whisper npc:KoTest heal")
    if i % max(1, int(1 / step)) == 0:
        send("whisper npc:KoTest packstate")
    s, l = sids[i % len(sids)], lvs[i % len(lvs)]
    if s == "attack":
        send("attack " + T)
    elif s.endswith("s") or how == "self":
        send(f"skill {s.rstrip('s')} {l} self")
    elif how == "pos":
        send(f"skill-pos-at {s} {l} {T}")
    else:
        send(f"skill {s} {l} {T}")
    send(f"wait {step}")
send("whisper npc:KoTest packstate", "wait 1", "quit")
p.stdin.close()
left, ms = (8 if WIDE else 5), 0
for line in p.stdout:
    m = re.search(r"KoTest: pack left (-?\d+) ms (\d+)", line)
    if m:
        left, ms = int(m.group(1)), int(m.group(2))
        if left <= 0 and ms:
            p.kill()
            break
print(json.dumps({"job": int(job), "level": int(level), "skills": ",".join(sids), "left": max(left, 0),
                  "seconds": round(ms / 1000, 1) if left <= 0 and ms else None}))

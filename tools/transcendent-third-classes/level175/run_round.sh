#!/usr/bin/env bash
# run_round.sh <rig dir> <round> <class> ...: for each class, the level test and then its level 175 spec, on one rig.
# Results: level175/results/phase3/<class>_leveltest.{json,txt} and <class>_r<round>.{json,txt}.
RIG="$1"; ROUND="$2"; shift 2
APP="$(cd "$(dirname "$0")/../../.." && pwd)"; DEV="$(dirname "$APP")"; OUT=$DEV/level175/results/phase3   # APP: ro-endgame-classes
cd "$RIG" || exit 1; mkdir -p logs
./up.sh $APP/mods/level175-core $APP/mods/transcendent-third-classes $APP/mods/expanded-classes ./kotest > logs/up.txt 2>&1 || { tail -5 logs/up.txt; exit 1; }
for c in "$@"; do
  spec=$APP/tools/transcendent-third-classes/level175/$c.json
  echo "== $c: level test"
  python3 -u kotest/leveltest.py "$spec" --json "$OUT/${c}_leveltest.json" 2>&1 | tee "$OUT/${c}_leveltest.txt"
  echo "== $c: round $ROUND"
  python3 -u run_specs.py "$spec" --no-load --json "$OUT/${c}_r$ROUND.json" 2>&1 | tee "$OUT/${c}_r$ROUND.txt"
done
echo "== done: $*"

#!/usr/bin/env bash
# sweep_classes.sh <rig> <out dir> <level>: every third class and advancement, one at a time, as the
# attacker beside a Lord Knight tank and a High Priest, in the fixed gear, against one Abysmal Knight
# and then three. Prints what each cast. The rig must be up with the class mod, the plans and rwtest.
RIG="$1"; OUT="$2"; LEVEL="$3"; mkdir -p "$OUT"; cd "$RIG"
for spec in 4060:m 4061:m 4062:m 4063:f 4064:m 4065:m 4073:m 4074:m 4075:m 4076:f 4077:m 4078:m 4079:m 4211:m 4212:f 4215:m 4239:m 4240:m 23:m; do
  j=${spec%:*}; sex=${spec#*:}
  rm -f logs/client-gmtest.jsonl
  GEAR=mid LEVEL=$LEVEL LIMIT=90 timeout 300 python3 rwparty.py 4008:Tank:tank:m,4009:Hela:support:f,$j:Cls:attacker:$sex 1219:1 1219:3 > "$OUT/sweep_${LEVEL}_$j.out" 2> "$OUT/sweep_${LEVEL}_$j.err"
  echo "== job $j level $LEVEL: $(grep -o 'gearof Cls[^"]*' "$OUT/sweep_${LEVEL}_$j.err" | head -1 | cut -c1-120)"
  python3 -c "
import json,sys
for l in open('$OUT/sweep_${LEVEL}_$j.out'):
    try: d=json.loads(l)
    except ValueError: continue
    print('   x%d cleared=%s %ss deaths=%d' % (d['count'], d['cleared'], d['seconds'], d['deaths']))"
  python3 skilluse.py . | grep "^job $j " | cut -c1-700
done

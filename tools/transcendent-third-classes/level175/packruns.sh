#!/usr/bin/env bash
# packruns.sh <rig> <out.jsonl> <label> <packtime args...>: three runs of one pack fight, each line kept; prints the median.
RIG="$1"; OUT="$(realpath -m "$2")"; LABEL="$3"; shift 3; cd "$RIG"
vals=()
for i in 1 2 3; do
  r=$(LIMIT=${LIMIT:-180} timeout 300 python3 kotest/packtime.py "$@" | tail -1)
  echo "{\"label\": \"$LABEL\", \"run\": $i, \"result\": $r}" >> "$OUT"
  vals+=("$(echo "$r" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["seconds"] if d["seconds"] is not None else 9999)')")
done
med=$(printf '%s\n' "${vals[@]}" | sort -n | sed -n 2p)
echo "$LABEL: ${vals[*]}  median $med"

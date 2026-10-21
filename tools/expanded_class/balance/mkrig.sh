#!/usr/bin/env bash
# Stamp out a copy of this rig with its own container names and ports, so
# several can run side by side (one party per server; FIGHT_TESTS.md §2).
#
#   ./mkrig.sh <rig dir> <name> <port prefix> [rathena checkout | built rig to copy]
#
#   ./mkrig.sh ~/level175-rigs/a l175-a 51 ../rathena-level175
#       containers l175-a-server / l175-a-db, ports 51900 (login), 51121 (char),
#       51120 (map), 51306 (database); rathena cloned at the commit
#       config/VENDOR_PINS pins, the population engine applied, and built.
#   ./mkrig.sh ~/level175-rigs/b l175-b 52 ~/level175-rigs/a
#       the same, but the built rathena tree is copied from rig a (minutes
#       instead of a full build).
#
# The fight-test harness (rwparty.py, rwsuite.py, rwtest) is copied in beside
# it. Run it again on an existing rig directory to refresh the scripts and the
# harness; the database is left alone, and so is the rathena tree unless a
# checkout is given and config/VENDOR_PINS has moved: then the new commit is
# checked out, the engine applied again and the build brought up to date.
# ENGINE=1 does the same when only the population engine changed.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
# the app checkout (pin, population engine) and ro-endgame-world (the harness)
APP="$(cd "${RO_APP:-$REPO/../ragnarokoffline.app}" && pwd)"
WORLD="${RO_WORLD:-$REPO/../ro-endgame-world}"
[ $# -ge 3 ] || { sed -n '2,17p' "$0"; exit 1; }
RIG="$1"; NAME="$2"; P="$3"; SRC="${4:-}"
mkdir -p "$RIG"
RIG="$(cd "$RIG" && pwd)"

# --- scripts, config, client: copied, then renamed and re-ported -------------
(cd "$HERE" && tar -c --exclude=./rathena --exclude=./logs --exclude=./.lock --exclude=__pycache__ .) | tar -x -C "$RIG"
H="$WORLD/tools/companion-strategies/harness"
if [ -d "$H" ]; then
	cp "$H"/*.py "$RIG/"
	mkdir -p "$RIG/rwtest/npc"
	cp "$H/rwtest.txt" "$RIG/rwtest/npc/rwtest.txt"
fi
cd "$RIG"
sed -i -e "s/rorig-server/$NAME-server/g" -e "s/rorig-db/$NAME-db/g" \
	-e "s/\b13306\b/${P}306/g" -e "s/\b16900\b/${P}900/g" -e "s/\b16121\b/${P}121/g" -e "s/\b15121\b/${P}120/g" \
	up.sh down.sh tools/run_servers.sh base/conf/*.txt roclient.py README.md
cat > base/conf/battle_conf.txt <<'CONF'
// rig: the population engine on (the app sets this from Settings)
population_engine_enable: 1
population_engine_companion_limit: 8
population_engine_companion_inventory: 1
CONF
echo "$NAME $P" > .rig

# --- rathena ------------------------------------------------------------------
PIN="$(awk '$1 == "rathena" { print $3 }' "$APP/config/VENDOR_PINS")"
if [ -x rathena/map-server ] && [ -n "$SRC" ] && [ -d "$SRC/.git" -o -f "$SRC/.git" ] && { [ "$(git -C rathena rev-parse HEAD)" != "$PIN" ] || [ -n "${ENGINE:-}" ]; }; then
	# the pin moved, or ENGINE=1 says the population engine changed: check the pinned commit out
	# over the tree, put the engine back, rebuild what changed
	git -C rathena fetch -q "$(cd "$SRC" && pwd)" "$PIN" 2>/dev/null || git -C rathena fetch -q "$(cd "$SRC" && pwd)"
	git -C rathena checkout -q -f "$PIN"
	git -C rathena clean -q -fd -e conf/import -e db/import -e npc/rigmod
	echo "rathena moved to $(git -C rathena log --oneline -1)"
	"$APP/scripts/apply-server-mods.sh" "$RIG/rathena"
	./build.sh
elif [ -x rathena/map-server ]; then
	echo "$RIG: scripts and harness refreshed; rathena left as it is ($(git -C rathena log --oneline -1))"
elif [ -n "$SRC" ] && [ -x "$SRC/rathena/map-server" ]; then
	echo "copying the built rathena from $SRC"
	cp -a "$SRC/rathena" rathena
	rm -rf rathena/conf/import rathena/db/import rathena/npc/rigmod
elif [ -n "$SRC" ]; then
	git clone -q "$(cd "$SRC" && pwd)" rathena
	git -C rathena checkout -q "$PIN"
	echo "rathena at $(git -C rathena log --oneline -1)"
	"$APP/scripts/apply-server-mods.sh" "$RIG/rathena"
	./build.sh clean
else
	echo "no rathena yet: give a checkout or a built rig as the fourth argument" >&2; exit 1
fi
echo "rig $NAME ready in $RIG: login ${P}900 char ${P}121 map ${P}120 db ${P}306"

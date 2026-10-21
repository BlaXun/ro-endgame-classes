# level175-core

What the classes that level past 99 share. Needed by **transcendent-third-classes**
and **expanded-classes**; on its own it changes nothing a level-99 character can
see.

### The soft cap for base stats

The class mods let their classes raise a base stat to 150 (their
`db/job_stats.yml`), but the part above 99 counts for a
third (150 counts as 116), and base DEX above 99 does not shorten cast
time at all: instant cast needs the same +51 DEX from job, gear and
buffs as at level 99. A character whose base stats are 99 or less
computes exactly as without the mod. The rule is this mod's Lua
(`lua/soft_cap.lua`), on the server's `player` hooks `base_stat` and
`cast_dex` (rAthena's `src/map/skill_lua.hpp` lists every hook).

### Base level stays out of skill damage

Some skills read the caster's base level in their output (Dragon Breath,
Gates of Hell, Cross Slash, Heal and others; `lua/level_rule.lua` lists
them). Here the base level counts up to 99 and no further, so those
skills do not grow with levels 100 to 175; a character at or below 99 is
untouched. The job level is left alone. It is the server's Lua `level`
hook, one per skill.

### Files

`lua/soft_cap.lua` and `lua/level_rule.lua`, both written by hand. They
need a server with the Lua `player` and `level` hooks (rAthena's
`src/map/skill_lua.hpp` lists every hook).

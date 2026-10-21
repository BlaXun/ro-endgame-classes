# Skill descriptions for the classes this mod adds

The client shows a skill's text from one table, `SKILL_DESCRIPT` in
`data/luafiles514/lua files/skillinfoz/skilldescript.lub`. In pre-renewal the app serves
ROenglishRE's Pre-Renewal translation of it, which has no entry for most skills this mod adds (the
Kagerou/Oboro, Rebellion, Star Emperor and Soul Reaper skills, one or two per third class, the
Expanded Super Novice's three). The client replaces the table rather than merging, so the mod ships
the whole table: `build_skill_descriptions.py` takes the Pre-Renewal translation from the pinned
`vendor/ROenglishRE` and adds (or replaces) the entries in the `*.lua` files beside this note.

## One file per class group, entries only

```lua
	[SKID.KO_ZANZOU] = {
		"Illusion - Shadow",
		"Max Level: 5",
		"^CC3399Requirement: Cicada Skin Shed 1^000000",
		"Skill Form: ^3F0099Active^000000",
		"Type: ^339900Supportive^000000",
		"Target: ^6666CCCaster^000000",
		"Description: ^777777Creates a ^990099Shinobi^777777 clone that takes hits",
		"for the caster until its ^CC6600HP^777777 runs out or it expires.^000000",
		"<i>^777777Its HP does not grow with base level.^000000</i>",
		"[Lv 1]: ^777777Clone HP <b>6000</b>, 10 sec^000000",
		"[Lv 5]: ^777777Clone HP <b>18000</b>, 10 sec^000000"
	},
```

- Tab-indented, one string per line, a comma after every line but the last, `},` after the entry.
  Plain ASCII; `"` inside a line is written `''`, as the translation does.
- Lines of about 40 characters: the skill window does not wrap well.

## The order of lines

1. The skill's name (as the Renewal translation names it).
2. `Max Level: N` (this mod's maximum: `db/skill_db.yml` of the mod, else rAthena's pre-re table).
3. `^CC3399Requirement: ...^000000` when the skill tree has prerequisites (the mod's `db/skill_tree.yml`).
4. `Skill Form: ^3F0099Active^000000` or `^6666CCPassive^000000`, `^3F0099Toggle^000000`.
5. `Type: ` with `^FF0000Physical Melee/Ranged^000000`, `^FF0000Magical^000000`, `^339900Supportive^000000`
   or `^FF0000Debuff^000000`.
6. `Target: ^6666CC1 Enemy / Caster / Ground / Party^000000`.
7. `Description: ^777777...^000000` over several lines; weapon and ammunition needs; then the
   per-level lines `[Lv N]: ^777777...^000000`.

## Colours and emphasis (the translation's own, plus bold and italic)

| What | Markup |
|---|---|
| body text | `^777777` ... `^000000` |
| requirement | `^CC3399` |
| skill form | `^3F0099` (active), `^6666CC` (passive) |
| type | `^FF0000` (attack, debuff), `^339900` (support) |
| target | `^6666CC` |
| another skill's name | `^0000FF` |
| a status (Stun, Bleeding, Cross Wound) | `^663399` |
| a class (Kagerou, Oboro) | `^00A100` |
| a weapon or item kind (Huuma Shuriken, Bullet) | `^990099` |
| a stat or level (STR, Base Level) | `^CC6600` |
| a warning or a cost that matters | `^FF0000` |
| the numbers that matter in a level line | `<b>...</b>` |
| a note about this game's rules (no base level in damage, fixed cast) | `<i>...</i>` |

Colours open with `^RRGGBB` and run until the next one; always return to `^777777` inside the body
and close the line or the entry with `^000000`. `<b>` and `<i>` must close on the same line.

## The numbers are this game's, not renewal's

- Damage ratios, durations, cast, delay, cooldown, SP: what the mod does. Read in this order: the
  mod's Lua (`mods/transcendent-third-classes/lua/*.lua`, which changes ratios and adds
  effects), its `db/skill_db.yml` (cast, delay, cooldown, SP, range, duration), the README's class
  section ("How strong"), and for anything the mod leaves alone rAthena's pre-renewal table and code
  (`rathena-level175/db/pre-re/skill_db.yml`, `src/map/skills/`, `src/map/battle.cpp`).
- **Fixed cast** (the fixed-cast rule): renewal's fixed cast is three quarters after-cast delay and a
  quarter cast time here; a skill with a cooldown of 10 s or more keeps it as cast. Write the cast
  and delay that result.
- **Level rule**: base level counts only up to 99 in the skills `lua/level_rule.lua` lists; job level
  as renewal. Say "Base Level (up to 99)" where it applies, and nothing about base level where it no
  longer counts.
- When a number cannot be pinned down, describe the effect without it rather than guess; never copy a
  renewal number the mod changed.

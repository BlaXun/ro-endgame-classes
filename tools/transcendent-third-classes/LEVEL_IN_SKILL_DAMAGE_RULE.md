# Rule: base level and job level in skill output (third classes and expanded advancements)

> **Kept as the record of 2026-10-11.** What was built in the end: the fork's Lua `level` / `job_level` hooks behind `status_get_lv_dmg()`, with the rule in `level175-core/lua/level_rule.lua`; the `skill_damage_level` extension and the app-side patches described here are gone. See `docs/RENEWAL_ENDGAME.md`, phase 3.

Set by the owner on 2026-10-11. It follows [LEVEL_IN_SKILL_DAMAGE.md](LEVEL_IN_SKILL_DAMAGE.md),
which lists where the levels enter the formulas. This file holds the rule, the
check of that list against the source, and the specification of the Lua
hooks that let the class mod apply it (§4). Nothing here is implemented yet.

Source read: rAthena `upstream/ragnarokoffline` (`8ff133fb`), pre-renewal
branches of the code. All `file:line` references are to that commit.

## 1. The rule

Skill output (damage, healing, the value of a damage-raising status) must not
grow with a character's level past the classic caps. Bonuses beyond that
belong on cards, buffs and equipment.

**Base level counts up to 99 and no further.** A character above 99 gets the
level-99 value; a character at or below 99 is unchanged. (The owner first
asked for no level effect at all on the first eight rows, then settled on the
same cap for all, 2026-10-11, so that no skill gets weaker for a level-99
character.)

| Skill | What reads the level today |
|---|---|
| `RK_DRAGONBREATH`, `RK_DRAGONBREATH_WATER` | base damage × level / 100 above level 100 (so capped: never) |
| `NC_SELFDESTRUCTION` | the same factor, before HP is added |
| `SR_GATEOFHELL` | flat + 10 × level (+ 40 × level in the Fallen Empire combo) |
| `AB_RENOVATIO` | damage to Undead = level × 10 + INT |
| `SR_CRESCENTELBOW` | counter ratio × the Sura's level / 125 |
| `AB_HIGHNESSHEAL` | (level + INT) / 8 × … |
| `AL_HEAL`, and `AB_CHEAL` through it | (level + INT) / 8 × (4 + 8 × lv) |
| `SJ_GRAVITYCONTROL` | fall damage on a monster + 50 × level |
| `SC_ENCHANTBLADE` (`RK_ENCHANTBLADE`) | (100 + 20 × lv) × level / 100 + INT |
| `SC_EXEEDBREAK` (`LG_EXEEDBREAK`) | weight / 10 × weapon level × level / 100 (its 15 × job level: see below) |
| `SC_ZANGETSU` (`KO_ZANGETSU`) | ± (level / 3 + 20 or 30 × lv) |
| `KO_JYUMONJIKIRI` | + skill lv × level on a marked target |
| `SL_SMA` | ratio = (40 + level) % |
| `TK_JUMPKICK` | ratio = 4 × level %, × 2 under Spurt |
| `SG_SUN_ANGER`, `SG_MOON_ANGER`, `SG_STAR_ANGER` | (level + DEX + LUK [+ STR]) / (12 − 3 × lv) % |
| `AL_DEMONBANE` | lv × (level / 20 + 3) |
| `PR_TURNUNDEAD` | kill chance and fail damage both add level |

**Job level is left alone.** The class mod keeps `MaxJobLevel` at 70 (60 for
Kagerou, Oboro and Rebellion), so these cannot grow with level 175:
`RL_QD_SHOT` (hits = 1 + job level / 20), `SC_RUSHWINDMILL` and
`SC_MOONLITSERENADE` (job level / 5), Exceed Break's 15 × job level, Auto
Blitz Beat (level cast = (job level + 9) / 10) and `GS_FLING` (damage = job
level).

**Nothing to do:** the Sorcerer's elementals and Sanctuary-type heals read no
level (§2, corrections 2 and 3).

Everything else in LEVEL_IN_SKILL_DAMAGE.md (§1 ratio terms, §4 chances and
durations, the two skills that read the **target's** level) is not covered by
this rule as given.

### Coluceo Heal

`AB_CHEAL` is the Arch Bishop's party heal. It has no formula of its own: it
heals each member for the caster's **learned Heal level** through Heal's
formula, whatever its own level (§2, correction 4), plus 2.5 % per party
member on the map when there are two or more. Its own level sets the area
(7×7, 15×15, 31×31 cells), the cast time and the SP cost. So it follows Heal
in this rule with no extra code.

| | Heal (`AL_HEAL`) | Coluceo Heal (`AB_CHEAL`) |
|---|---|---|
| SP | 13 at level 1, +3 a level, 40 at level 10 | 90 / 100 / 110 in the class mod (renewal: 200 / 220 / 240) |
| Cast, cooldown | none, 1 s delay | about 3 s cast, 2 s cooldown |
| Amount at level 1 | Heal level 1: (level + INT) / 8 × 12 | the learned Heal level: with Heal 10, (level + INT) / 8 × 84, seven times Heal level 1 |

**Wanted balance (owner, 2026-10-11): too strong as it is.** It keeps its 3
levels and heals the whole party, but for 70 % / 85 % / 100 % of the caster's
normal Heal per member at level 1 / 2 / 3, and without the bonus per party
member. The percentages are a proposal the owner accepted with "keep 3";
they have not been measured.

Not implemented. The amount and the party bonus are both hard-coded in
`skills/acolyte/coluceoheal.cpp:23-26`, which ignores the skill's own level.
Settled route (owner, 2026-10-11): a Lua **`heal` hook** in the fork, called
from Heal, Highness Heal and Coluceo Heal when they heal. The hook gets the
amount the server would restore as `stock` and the amount before the skill's
own bonus as `c.base`, so a mod drops the party bonus by building on
`c.base`. The mod's `lua/coluceo_heal.lua` then returns
`c.base × {70, 85, 100}[skill level] / 100`. Specification: §4.

## 2. Check against the source

Every expression and location LEVEL_IN_SKILL_DAMAGE.md gives for the skills
above was re-read at `8ff133fb` and is correct, including that none of them
sits behind a renewal switch. A second pass listed every pre-renewal-active
level read in `battle.cpp` and in `src/map/skills/`; it found no damage term
for these classes that the note lacks.

**The claim that some of these have no hook is true, and wider than the note
says.** A Lua `ratio` hook runs only where a skill class's
`calculateSkillRatio` is called (`battle.cpp:4470` weapon, `:5984` magic). Of
the skills in the rule:

| Reach today | Skills |
|---|---|
| Exact, by a ratio hook | `SL_SMA` (`stock − level + min(level, 99)`); `TK_JUMPKICK` (the two level branches give exactly 4 × or 8 × level, the third 30 + 10 × lv, at most 100, so above level 99 the hook can tell them apart by value) |
| Close, by a ratio hook | Dragon Breath, both: the level is a factor of the base damage and the ratio multiplies it afterwards (`battle.cpp:5466`), so `stock × 100 / level` cancels it, with a rounding loss under 1 % |
| None | everything else |

Why the rest is out of reach:

| Skill | Where the level is read | Why no hook sees it |
|---|---|---|
| `NC_SELFDESTRUCTION` | `battle.cpp:4101-4106` | HP is added after the level factor; the hook would need the Mainframe level to recompute, which it cannot read |
| `SR_GATEOFHELL` | `battle.cpp:5691`, `:5693` | added after the ratio |
| `AB_RENOVATIO` | `battle.cpp:5935` | fixed magic damage, no ratio call |
| `PR_TURNUNDEAD` | `battle.cpp:5908`, `:5924` | fixed magic damage and a chance |
| `GS_FLING` | `battle.cpp:6534` | fixed misc damage |
| `RL_QD_SHOT` | `skills/gunslinger/quickdrawshot.cpp:19` | hit count in `modifyDamageData`, which the Lua wrapper passes through unhooked. The hit count multiplies the damage (`DAMAGE_DIV_FIX`, `battle.cpp:4239`) |
| `SR_CRESCENTELBOW` | `battle.cpp:5211` | computed inside the attacker's hit, no skill class |
| `AB_HIGHNESSHEAL`, `AL_HEAL`, `AB_CHEAL` | `skill.cpp:555-556`, `:590` | `skill_calc_heal` has no hook. Heal and Highness Heal on Undead take the same number as damage (`battle.cpp:5896`) |
| `SJ_GRAVITYCONTROL`, `RK_ENCHANTBLADE` | `skills/taekwon/gravitycontrol.cpp:23`, `skills/swordman/enchantblade.cpp:17` | status value set in `castendNoDamageId` |
| Exceed Break, Zangetsu, the two songs | `status.cpp:12141`, `:12351-12358`, `:12060` | status value set in `status_change_start` |
| Wrath, Demon Bane | `battle.cpp:4694`, `:2295` | passives, no skill class |
| Auto Blitz Beat | `skill.cpp:1358-1360` | the level of an automatic cast |

### Corrections to LEVEL_IN_SKILL_DAMAGE.md

1. **Dragon Breath has a skill class** (`skills/swordman/dragonbreath.cpp`,
   both ids). The note found none. The class mod already puts a ratio hook on
   both (`lua/third_classes.lua`, factor 64), so the hook point works.
2. **"Sorcerer's elementals (`EL_*` attack skills)" is wrong.** The five
   skills that read the master's level are `EM_EL_AVALANCHE`,
   `EM_EL_AGE_OF_ICE`, `EM_EL_DEADLY_POISON`, `EM_EL_FLAMEROCK` and
   `EM_EL_STORM_WIND`: the Elemental Master's (fourth job) elementals. No
   `EL_*` skill reads a level. The class mod leaves those five out of its
   `elemental_db.yml`, so this entry has nothing to act on. A ratio hook could
   not fix them anyway: its `c.caster` is the elemental, and the master's
   level is not passed.
3. **"Sanctuary-type heals" carry no level.** Sanctuary is a fixed table
   (`skill.cpp:542-543`) and pre-renewal Apple of Idun has its own formula
   (`:536-540`). For players the default heal line is reached only by
   `AL_HEAL` and `AB_CHEAL`.
4. **`AB_CHEAL` has no formula of its own.** It calls
   `skill_calc_heal(src, target, AL_HEAL, <learned Heal level>, true)`
   (`skills/acolyte/coluceoheal.cpp:23`), so it cannot be told apart from Heal
   inside `skill_calc_heal`. It skips Undead targets and never deals damage.
5. **Crescent Elbow** reads `status_get_lv(target)`: the target of the
   incoming hit, which is the Sura. The note's wording is right, the variable
   name misleads.
6. **Enchant Blade**: the comment at `battle.cpp:5242` says level / 150, the
   code divides by 100. The note's expression follows the code.

## 3. What already exists

Branch `level175/softcap` (worktree `rathena-level175/`, commit `a94699e44`,
local, not pushed) adds the extension **`skill_damage_level`**, off by
default, with two values: `base_level` (default 99) and `job_level` (default
70). Two helpers in `status.cpp` carry it: `status_get_lv_dmg(bl)` returns
`min(level, base_level)` for a player, and `status_get_joblv_dmg(sd, fallback)`
returns `job_level` for every player. About 27 calls in the formulas use them
in place of the raw level.

Against this rule:

| | State |
|---|---|
| Covered as the rule wants (cap at 99) | Dragon Breath, Self Destruction, Gates of Hell, Renovatio, Crescent Elbow, Gravity Control, Enchant Blade, Exceed Break (base part), Zangetsu, Cross Slash, Esma, Flying Kick, Wrath, Demon Bane, Turn Undead's kill chance |
| **Against the rule**: job level fixed at 70 | Quick Draw Shot, Exceed Break (job part), the two songs. The rule leaves the job level alone; the extension gives every player 70, also below the cap: a job-level-20 Rebellion gets the 4 hits of job level 60 to 70. The mod must not rely on the extension for this, or the `job_level` value has to go |
| **Missing** | `AB_HIGHNESSHEAL`, `AB_CHEAL`, `AL_HEAL`: the commit does not touch `skill_calc_heal`. Turn Undead's fail damage (`battle.cpp:5924`): only its kill chance (`:5908`) is capped |
| Not touched, as the rule wants | Fling, Auto Blitz Beat |
| Extra | the five `EM_EL_*` skills |

It is one switch with two numbers: a mod cannot change a single skill's term.

## 4. What to build (settled 2026-10-11, not implemented)

Three Lua hooks in the rathena fork, and two Lua files in the class mod. The
step-by-step guide with the code for every step is
LEVEL_HOOK_GUIDE.md (not kept) (also published as the
artifact "Lua Level Hook"); this section is the specification it follows.
Where the two differ, this section wins. None of the guide's code has been
compiled or run.

**Where:** the worktree `rathena-level175/`, branch `level175/softcap`, on top
of `a94699e44`. Do not switch branches in any checkout. The mod files go in
`ragnarokoffline.app/mods/transcendent-third-classes/`.

### Server (rathena fork)

1. **Hook names.** `skill_lua.cpp`: add `HOOK_LEVEL`, `HOOK_JOB_LEVEL`,
   `HOOK_HEAL` to `e_hook` and `"level"`, `"job_level"`, `"heal"` to
   `hook_names`, same order; name them in the unknown-hook error text. No
   change to `skill_lua_attach`: these hooks run by skill id, so they also
   reach skills without a skill class.
2. **`skill_lua_level(skill_id, bl, stock)`** and
   **`skill_lua_job_level(skill_id, bl, stock)`**, built on
   `call_number_hook`, result clamped to 0..`MAX_LEVEL`. The hook's context
   has `c.caster` only: `c.target` is nil and `c.skill_lv` is 0.
3. **The helpers take a skill id**, with no default value, so every call site
   must name its skill: `status_get_lv_dmg(bl, skill_id)` and
   `status_get_joblv_dmg(sd, fallback, skill_id)`. Order inside: real level,
   then the `skill_damage_level` extension, then the Lua hook. Players only;
   any other unit gets its real level.
4. **Call sites pass their id** (table in the guide, phase 04). Where a
   formula reads the level more than once (Dragon Breath, Self Destruction,
   Zangetsu), ask once into a local. The two songs share a line and need the
   id by status: `MI_RUSH_WINDMILL` or `WA_MOONLIT_SERENADE`.
5. **The gaps join:** the pre-renewal lines of `AB_HIGHNESSHEAL` and of the
   default branch in `skill_calc_heal` (`skill.cpp:555`, `:590`), and Turn
   Undead's fail damage (`battle.cpp:5924`). Coluceo Heal is covered through
   `AL_HEAL`. Only pre-renewal lines are touched.
6. **`skill_lua_heal(skill_id, skill_lv, src, target, stock, base)`**:
   `call_number_hook` gains an optional `base` that is put on the context as
   `c.base`. Called in `coluceoheal.cpp` after the party bonus and before the
   immunity check, with `base` = the amount before the bonus; and in
   `heal.cpp` and `highnessheal.cpp` right after `skill_calc_heal`, with
   `base` = `stock`. It runs when these skills heal, not when Heal damages an
   Undead.
7. **Docs:** the API comment at the top of `skill_lua.hpp` (canonical Lua
   reference), the description of `skill_damage_level` in
   `db/extension_db.yml` (add the heals and Turn Undead's fail damage), and
   the covered skills in `doc/extensions.md`.

With no hook registered, every formula reads the real level and every heal is
stock: the change does nothing by default and needs no extension of its own.

### Class mod

- `lua/level_rule.lua`: one list of the skills in §1's table (with `AL_HEAL`
  standing for Coluceo Heal too), each with
  `level = function(c, stock) return math.min(stock, 99) end`. No `job_level`
  hook: the job level is left alone.
- `lua/coluceo_heal.lua`: `heal` on `AB_CHEAL` returning
  `c.base * ({70, 85, 100})[c.skill_lv] // 100`, 100 % for any other level.
- The mod does **not** enable the `skill_damage_level` extension: its
  `job_level` value would give every player job level 70, against §1.
- `mod.json`: raise `requires.app` to the first app version whose rathena pin
  has the hooks. An older server raises an error on an unknown hook name
  (`lua_register_skill`), which stops that Lua file; that is why the rules
  sit in files of their own.

### Tests

Guide, phase 08: Esma with a probe hook returning level 1 (ratio 41 %), nil
(stock), and no file (stock, no log line); one skill without a class
(`AL_DEMONBANE`), one status value (`KO_ZANGETSU`), the extension together
with Lua (`stock` reads 99 at level 150); Coluceo Heal in a party of three
with and without `coluceo_heal.lua`; one skill at level 99 against 175 on the
rig of FIGHT_TESTS.md.

### To confirm while implementing

- The `sc_type` parameter of `status_change_start_post_delay` is assumed to
  be named `type` (used to tell the two songs apart).
- Line numbers are from `level175/softcap`; re-find by the expressions if the
  branch has moved.
- The 70 / 85 / 100 % for Coluceo Heal are the owner's choice, not measured.

### Delivery

Two commits for the levels (`extensions: skill_damage_level also covers heals
and Turn Undead's fail damage`, then `Lua: level and job_level hooks`), one
for `Lua: heal hook for Heal, Highness Heal and Coluceo Heal`. Push and merge
only when the owner says so; then the app's pin moves with
`scripts/vendor-bump.sh rathena` and the mod files follow.

### Left out on purpose

- Coluceo Heal apart from Heal for the level cap (it follows Heal).
- Fling, Auto Blitz Beat, and every other job-level term.
- A plain number in place of a function (`level = 99`), which would save the
  Lua call that Demon Bane and Wrath make on every attack. Add it if a
  profile asks for it.
- The renewal lines of the same formulas.
- Hooks on the other amounts (base damage, final damage, hit count, status
  values, Heal's damage on Undead): three to four times the code, and each
  would need context the hooks do not have (learned skill levels, weapon
  weight and level, combo state).
- Chances and durations that read a level (LEVEL_IN_SKILL_DAMAGE.md §4).

# Where base level and job level enter the damage of third-class and advancement skills (pre-renewal build)

> **Kept as the record of 2026-10-11.** What was built in the end: the fork's Lua `level` / `job_level` hooks behind `status_get_lv_dmg()`, with the rule in `level175-core/lua/level_rule.lua`; the `skill_damage_level` extension and the app-side patches described here are gone. See `docs/RENEWAL_ENDGAME.md`, phase 3.

Written for research request 5 (2026-10-11). The owner's rule: for every third
class and expanded advancement, base level and job level must not affect skill
damage at all. This lists every place where one of them does, in rAthena
`upstream/ragnarokoffline` (`8ff133fb`) **compiled without `RENEWAL`**, and
whether a Lua ratio hook can take it out.

**How it was found.** Every line in `src/map/**/*.cpp` containing
`status_get_lv`, `base_level`, `job_level`, `BaseLevel` or `change_level` was
listed with its enclosing function and whether it sits inside `#ifdef RENEWAL`
(450 lines; 109 in `src/map/skills/`). Lines with only `RE_LVL_DMOD`,
`RE_LVL_MDMOD` or `RE_LVL_TMDMOD` were left out: those macros are empty in this
build (`src/config/const.hpp:105-108`). The classification below was done by
reading each line. A level read that hides behind another name would be
missed; none was seen.

**What a ratio hook can do.** The hook wraps the skill class's
`calculateSkillRatio` (`src/map/skill_lua.cpp:490-491`) and receives the stock
ratio, `c.skill_lv`, and `c.caster.level` and `c.caster.job_level`
(`skill_lua.cpp:233`, `254`, `399-400`). So a term **added inside the ratio
function** can be removed exactly (`stock − term + term at the fixed level`),
and a factor on the whole ratio can be divided out. Anything computed
elsewhere (`battle.cpp`, `status.cpp`, a hit count, a status value) the hook
never sees.

---

## 1. Level in the skill ratio: a ratio hook can remove it

All lines are outside any renewal switch, so they are active in this build.

| Skill | File:line | Expression | Shape | Hook |
|---|---|---|---|---|
| `SO_DIAMONDDUST` | skills/mage/diamonddust.cpp:33 | `skillratio += job_level * 5` | added | subtract `5 × c.caster.job_level` |
| `SO_EARTHGRAVE` | skills/mage/earthgrave.cpp:26 | `skillratio += job_level * 5` | added | same |
| `SO_POISON_BUSTER` | skills/mage/poisonbuster.cpp:26 | `skillratio += job_level * 5` | added | same |
| `SO_VARETYR_SPEAR` | skills/mage/varetyrspear.cpp:26 | `skillratio += job_level * 5` | added | same |
| `SO_CLOUD_KILL` | skills/mage/cloudkill.cpp:28 | `skillratio += job_level` | added | subtract `c.caster.job_level` |
| `SO_FIREWALK`, `SO_ELECTRICWALK` | skills/mage/firewalk.cpp:31, electricwalk.cpp:31 | `skillratio += job_level / 2` | added | subtract `job_level // 2` |
| `GC_COUNTERSLASH` | skills/thief/counterslash.cpp:24 | `skillratio += job_level * 4` | added | subtract `4 × job_level` |
| `GN_DEMONIC_FIRE` (the Fire Expansion branch) | skills/merchant/demonicfire.cpp:20 | `skillratio += 10 + 20*(skill_lv−10) + INT + job_level` | added, in one branch only | subtract `job_level` when that branch runs; read the file for the branch condition |
| `KO_BAKURETSU` (Kunai Explosion) | skills/ninja/kunaiexplosion.cpp:21 | `skillratio += 10 * job_level` | added | subtract `10 × job_level` |
| `SC_FEINTBOMB` | skills/thief/feintbomb.cpp:19 | `skillratio += −100 + (skill_lv+1) * DEX/2 * (job_level/10)` | **factor** of the whole ratio (integer division: 0 below job 10, 7 at job 70) | recompute: return `(c.skill_lv+1) × (dex // 2) × K` with a fixed K |
| `SR_WINDMILL` | skills/acolyte/windmill.cpp:32 | `skillratio += −100 + base_level + DEX` | added | subtract `c.caster.level`, add the fixed value |
| `KO_JYUMONJIKIRI` (Cross Slash) | skills/ninja/kocrossslash.cpp:33-36 | `if target has SC_JYUMONJIKIRI: skillratio += skill_lv * base_level`, then `× (100 + Kagemusya)%` | added, conditional on the target's mark, before a multiplier | only if the hook can tell that the target is marked and the caster is under Kagemusha; **not checked** whether the hook context exposes statuses. If it does not, this one needs a source change |

Two skills read the **target's** level, not the player's. They do not break the
rule as worded (the player's level has no effect), but they grow with the
monster's level:

| Skill | File:line | Expression |
|---|---|---|
| `SR_KNUCKLEARROW` (the knock-into-wall hit) | skills/acolyte/knucklearrow.cpp:21 | `skillratio += … + status_get_lv(target) * 5` |
| `SR_TIGERCANNON` | battle.cpp:5681, 5683 | flat `+ skill_lv × 240 (or 500) + target level × 40` |

## 2. Level in the damage, outside the ratio: a ratio hook cannot remove it

| Skill | File:line | Expression | Where it sits | What a hook can do |
|---|---|---|---|---|
| `RK_DRAGONBREATH`, `RK_DRAGONBREATH_WATER` | battle.cpp:4082-4084 | `damagevalue = (HP/50 + MaxSP/4) × skill_lv; if level > 100: × level / 100` | base damage (`battle_calc_skill_base_damage`), **not** behind a renewal switch | The level is a factor of the whole base damage, and the ratio multiplies base damage afterwards (battle.cpp:5466), so a ratio of `stock × 100 / level` cancels it to within rounding, **if** the skill has a ratio hook point. No skill class with `Impl(RK_DRAGONBREATH)` was found by a quick search: check before relying on it |
| `NC_SELFDESTRUCTION` | battle.cpp:4101-4106 | `(skill_lv+1) × (Mainframe+8) × (SP + VIT); if level > 100: × level/100; then + HP` | base damage | Not exactly: the HP is added after the level factor |
| `SR_GATEOFHELL` | battle.cpp:5691, 5693 | flat `+ 40 × base_level` in the Fallen Empire combo, else `+ 10 × base_level` | added after the ratio | No. At level 175: +7,000 or +1,750 a cast |
| `AB_RENOVATIO` (damage to Undead) | battle.cpp:5935 | `damage = base_level × 10 + INT` | fixed magic damage | No |
| `RL_QD_SHOT` (Quick Draw Shot) | skills/gunslinger/quickdrawshot.cpp:16-19 | `hits = 1 + job_level / 20` (4 at job 70) | hit count (`modifyDamageData`) | No |
| `SR_CRESCENTELBOW` (the counter) | battle.cpp:5208-5214 | counter ratio `= attacker HP/100 × skill level × the Sura's base_level / 125`, capped at 5000 % | reaction to being hit, in `battle.cpp` | No |
| `SJ_GRAVITYCONTROL` | skills/taekwon/gravitycontrol.cpp:18-23 | fall damage on a monster `= ATK − soft DEF + 50 × base_level − DEF`, stored in the status | status value | No. At level 175: +8,750 |
| Sorcerer's elementals (`EL_*` attack skills) | skills/elemental/avalanche.cpp:19 and four alike | `ratio += ratio × master's base_level / 100` | the elemental's own skill, level of the Sorcerer | Only by hooking each elemental skill (factor: `stock × 100 / (100 + level)`) |

**Damage-raising statuses these classes give:**

| Status (skill) | File:line | Expression | Effect |
|---|---|---|---|
| `SC_ENCHANTBLADE` (`RK_ENCHANTBLADE`) | skills/swordman/enchantblade.cpp:17; used at battle.cpp:5241-5250 | `val2 = (100 + 20 × skill_lv) × base_level / 100 + INT` | magic damage added to every normal attack. At 175 and level 5: 350 + INT, against 198 + INT at 99 |
| `SC_EXEEDBREAK` (`LG_EXEEDBREAK`) | status.cpp:12136-12141; used at battle.cpp:4667-4668 | `val2 = 150 × lv + 15 × job_level + weight/10 × weapon level × base_level / 100` | % added to the next normal attack; both levels |
| `SC_ZANGETSU` (`KO_ZANGETSU`) | status.cpp:12349-12358; used at status.cpp:7316-7317, 7464 | `± (base_level / 3 + 20 or 30 × lv)` | base ATK and MATK up or down |
| `SC_RUSHWINDMILL` (`WM` song) | status.cpp:12060; used at status.cpp:7383-7384 | `val3 = 4 + 3 × lv + lesson + job_level / 5` | weapon ATK |
| `SC_MOONLITSERENADE` (`WM` song) | status.cpp:12060; used at status.cpp:7466 | same value | MATK |

None of these is reachable from a ratio hook; each needs a change where the
value is computed, or an extension that fixes the level those lines read.

## 3. Healing (listed apart; the rule as given is about damage)

| Skill | File:line | Expression (pre-renewal branch) |
|---|---|---|
| `AB_HIGHNESSHEAL` | skill.cpp:555-556 | `((base_level + INT) / 8) × (4 + 8 × Heal level) × (17 + 3 × lv) / 10` |
| `AB_CHEAL` and every skill that falls to the default heal | skill.cpp:590 | `(base_level + INT) / 8 × (4 + 8 × lv)` |
| `AL_HEAL`, `PR_SANCTUARY`-type heals kept from earlier jobs | skill.cpp:590 | same default (Sanctuary itself is a fixed table, skill.cpp:542-543) |

Heal used on an Undead monster deals this amount as damage, so it is also a
damage formula with the level in it. `AB_RENOVATIO`'s damage is in §2. The
Soul Ascetic and Cardinal heals at skill.cpp:565-577 belong to fourth jobs.

## 4. Level read for something other than damage (one line each)

- `AB_ADORAMUS`: blind/slow chance, job level (skills/acolyte/adoramus.cpp:18).
- `AB_CANTO`, `AB_CLEMENTIA`: level of Increase AGI / Blessing given, job level / 10 (cantocandidus.cpp:18, crementia.cpp:18). Blessing's stats then feed damage: a borderline case.
- `AB_DUPLELIGHT`: proc chance by level difference (skill.cpp:3268).
- `WL_SIENNAEXECRATE`, `WL_WHITEIMPRISON`: chance, job level / 4 (skills/mage/siennaexecrate.cpp:27, whiteimprison.cpp:21).
- `WL_EARTHSTRAIN`: strip chance, job level / 4 (skill.cpp:2118-2123).
- `WL_FREEZE_SP`: memorise capacity, base level / 10 (skill.cpp:13775).
- `SO_ARRULLO`: sleep chance, job level / 5 (skills/mage/arrullo.cpp:17). `SO_DIAMONDDUST`: freeze chance, job level / 5 (diamonddust.cpp:20).
- Sorcerer's elemental: HP, HIT, DEF, FLEE from the master's levels (elemental.cpp:59-77).
- `SC_*` Masquerades (six): chance, both levels (skills/thief/masquerade*.cpp:30-33).
- `SR_GENTLETOUCH_QUIET`, `SR_GENTLETOUCH_CURE`: chance, base level (gentletouchquiet.cpp:15, gentletouchcure.cpp:26). `SC_CRESCENTELBOW`, `SC_LIGHTNINGWALK`: trigger chance, job level / 2 (status.cpp:12178, 12181).
- `LG_PINPOINTATTACK`: break chance, base level / 10 (skills/swordman/pinpointattack.cpp:32). `LG_BANDING`: stop chance (skill.cpp:7470). `SC_PRESTIGE`: magic evade and DEF, base level (status.cpp:12146-12147).
- `SC_STONEHARDSKIN` (`RK` rune): DEF/MDEF, job level (status.cpp:11840).
- `WM_LULLABY_DEEPSLEEP`, `WM_VOICEOFSIREN`, `WM_SATURDAY_NIGHT_FEVER`: chance or duration (skills/archer/*.cpp). `SC_SYMPHONYOFLOVER`, `SC_ECHOSONG`: MDEF and DEF, job level (status.cpp:12056, 12063).
- `GN_SLINGITEM` bombs: chance and duration, both levels (skills/merchant/slingitem.cpp:89-99). Genetic potion research statuses and creation rates (status.cpp:12322-12335, skill.cpp:13148-13251).
- `NC_SILVERSNIPER`, `NC_MAGICDECOY`: the summon's HP, base level × 12 (status.cpp:2960, 2972).
- `KO_JYUSATSU`: instant-kill condition, level comparison (skills/ninja/illusiondeath.cpp:25).
- Max HP/SP caps by level bracket (status.cpp:4358-4363) and HP/SP growth per level: stats, not skill formulas, but they feed HP- and SP-based skills (Dragon Breath, Gate of Hell, Self Destruction).

Nothing was found for `RA_`, `MI_`, `WA_`, `SP_`, `OB_`, `KG_`,
`NV_BREAKTHROUGH` or `NV_TRANSCENDENCE` (the last two are flat per-skill-level
bonuses, battle.cpp:2315, status.cpp:3159-3161). The Ranger's trap macro and
the renewal Hunter-trap formula (battle.cpp:6354-6359) are off in this build.

## 5. Second-class, transcendent and base-class skills these classes keep

The request expected none. There are several, all active in a pre-renewal
build (detail in STATS_ERAS.md §11a and §11b):

| Skill | Level term | Kept by | Source |
|---|---|---|---|
| Esma (`SL_SMA`) | ratio per hit = (40 + base level) % | Soul Reaper | skills/taekwon/esma.cpp:14-15 (ratio: hook can fix it) |
| Flying Kick (`TK_JUMPKICK`) after Tumbling or running | ratio = 4 × base level %, ×2 under Spurt | Star Emperor, Soul Reaper | skills/taekwon/jumpkick.cpp:17-22 (ratio: hook can fix it) |
| Wrath of the Sun/Moon/Stars (`SG_*_ANGER`) | bonus % = (base level + DEX + LUK [+ STR]) / (12 − 3 × lv) | Star Emperor | battle.cpp:4693-4699 (not a ratio) |
| Demon Bane (`AL_DEMONBANE`) | mastery + lv × (base level / 20 + 3) against Undead/Demon | Arch Bishop, Sura | battle.cpp:2292-2295 (not a ratio) |
| Turn Undead (`PR_TURNUNDEAD`) | kill chance and fail damage add base level | Arch Bishop | battle.cpp:5907-5924 (not a ratio) |
| Heal on Undead (`AL_HEAL`) | (base level + INT) / 8 × … | Arch Bishop, Sura, Royal Guard | skill.cpp:590 |
| Auto Blitz Beat | level used = (job level + 9) / 10; a Ranger always gets 5 | Ranger (exempt by code) | skill.cpp:1354-1362 |
| Fling (`GS_FLING`) | damage = job level | Rebellion | battle.cpp:6533-6534 |

**The owner's decision (2026-10-11, given in the research session):** "those
earlier skills that are already in pre-renewal and take the base level into
account should still do so, but they should cap at base 99". So these skills
keep their level term, computed with `min(base level, 99)`: a character above
99 gets exactly what a level-99 character gets.

**How it is built (reported by the main session, 2026-10-11; not read by the
research agent).** The rule and its implementation are in
[LEVEL_IN_SKILL_DAMAGE_RULE.md](LEVEL_IN_SKILL_DAMAGE_RULE.md), which is the
authority; where it and this file differ, it wins. The cap is not done with
ratio hooks: a Lua `level` hook sits on the helper the formulas ask for the
level, so it also reaches the terms outside a ratio function (Wrath, Demon
Bane, Turn Undead's chance and fail damage). The class mod's
`lua/level_rule.lua` lists Esma, Flying Kick, the three Wraths, Demon Bane,
Turn Undead, Heal and Highness Heal. Heals are settled there too: capped at
99, Coluceo Heal through Heal. Job-level terms (Auto Blitz Beat, Fling) are
left alone; the job cap stays 70.

The "a ratio hook cannot remove it" notes in §2 describe the stock hook API
of `upstream/ragnarokoffline` at `8ff133fb`, which has no `level` hook; with
that hook on the work branch, more of §2 may be reachable than this file says.

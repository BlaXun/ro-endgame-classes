# Renewal's endgame in pre-renewal: how it was built

This collection of mods brings renewal's endgame into the pre-renewal era: third classes and the expanded advancements, levels up to 175, renewal's lands with their monsters, bosses, gear and cards. Everything is balanced against pre-renewal rather than copied from renewal.

This document is the record of how it was made. Each phase says what it did, how, and why that way. It is written so that someone new, a person or an AI agent, can pick the work up and keep refining it without redoing what is settled.

**If you are continuing this work, read in this order:**
1. [What the collection provides](#what-the-collection-provides)
2. [The rules](#the-rules-that-hold-everywhere). Each was settled by the owner and must not be broken by a later change.
3. [How to change something](#how-to-change-something)
4. [What is open](#what-is-open)

The phases in between explain why things are the way they are. Read the relevant phase before changing a number it set.

---

## What the collection provides

Eight mods, all pre-renewal only, in two repositories: the three class mods in this one (`mods/`), the five renewal-world mods in [ro-endgame-world](https://github.com/BlaXun/ro-endgame-world) (`mods/`). The app's registry lists each as a GitHub source entry, so players install it from its repository's latest release:

| Mod | Provides | Requires |
|---|---|---|
| `level175-core` | The rules shared by every class that levels past 99. Above 99 a base stat point counts for a third, and base DEX past 99 gives no cast speed (`lua/soft_cap.lua`). Skill formulas that read the base or job level read at most 99 (`lua/level_rule.lua`). | — |
| `transcendent-third-classes` | Renewal's 13 third classes. Each is the step *after* its transcendent class at 99/70: the job level starts at 1 and runs to 70, and the base level runs to 175. They keep every earlier skill. Gear, shops, job changers, skill descriptions. | level175-core |
| `expanded-classes` | Kagerou/Oboro (from Ninja), Rebellion (Gunslinger), Star Emperor (Taekwon Master/Star Gladiator), Soul Reaper (Soul Linker) and the Expanded Super Novice (Super Novice), each an advancement of the finished base class. | level175-core |
| `renewal-world-monsters` | 115 renewal monsters on 45 renewal-world maps, levels 80–175, on a ladder of level steps. Dewata and Malangdo sit at 70–99. | renewal-world (maps) |
| `renewal-world-minibosses` | King Dramoh, Wild Rider, the gold Scarabas and their eggs. | renewal-world, -monsters |
| `renewal-world-mvps` | 14 renewal bosses and MVPs (Leak, Kraken, the Scaraba Queens, Spider Chariot, Nightmare Amon Ra, Boss Meow, Bestia, …) with their MVP rewards. | renewal-world, -monsters, -minibosses |
| `renewal-world-gear` | 54 renewal equipment items from these monsters, held to pre-renewal's best of their kind, and 3 sets. | renewal-world-monsters |
| `renewal-world-cards` | 95 cards pre-renewal lacks, made pre-renewal cards, and 11 sets. | renewal-world-monsters |

`renewal-world` itself, the maps alone, was already upstream and is not part of this collection.

**What a player gets**, in short:
- A transcendent character at 99/70 can advance once more and level to 175. The expanded classes can advance too.
- Endgame content runs from 100 to 175 across Malaya, Izlude 5, Rockridge, Bifrost, El Dicastes, Eclage and Verus. Every level step has monsters that press a party of that level.
- Bosses for parties, and renewal's loot converted so it fits next to pre-renewal's.

**What it does not change:**
- A character whose base stats are all at or below 99 computes exactly as in stock pre-renewal. This is tested; see the invariant in phase 1.
- Every class other than the new ones stays capped at 99.
- Pre-renewal's own items, cards and monsters are untouched. Two exceptions: monsters the conversion places on the new maps, and drops the gear and cards mods add to monsters.

### What it needs outside the mods

- **App ≥ 1.6.7** for the class mods. Since 1.6.7 a mod ships only its own skill descriptions, and the app hands them to the client as an extra table (`customSkillDescript`) laid over the client's, skill by skill.
- **App ≥ 1.6.8** (the release after the row-join PR) for the minibosses and MVPs. Two mods' `mob_skill_db.txt` rows are joined rather than one replacing the other (`ROW_TABLES` in `stack/src/mods.rs`). Without it, the last of the three monster mods to load takes every other monster's skills away. Both are documented in the app's `docs/MODDING.md`.
- **rAthena fork with the Lua hooks** (the app's `config/VENDOR_PINS`; Flux159's `ragnarokoffline` from 62e435d, which has PR #66). With no mod loaded the hooks do nothing, and the canonical reference is the comment block at the top of `src/map/skill_lua.hpp` and `doc/extensions.md` in the fork. The hooks used here:
  - `skill(name, {ratio, hit, element, on_hit, level, job_level, heal, bonus})`
  - `item(aegis, {on_attack, on_hit_taken})`
  - `player({base_stat, cast_dex})`
  - `status("SC_…", {on_start})` on a server status, with the `c:status_val()` action

  Mods bring the numbers through these hooks; rAthena carries no balance values for this collection.

---

## How it is built

**No table in these mods is written by hand.** Each is generated by a script that keeps the CSVs and rules it works from beside it. Each script has `--check`, which fails when a committed table no longer matches what it would write.

The class scripts are in this repository's `tools/`, the renewal-world ones in ro-endgame-world's `tools/`. They read the rAthena pin and the translation from a ragnarokoffline.app checkout: the one beside the repository (`../ragnarokoffline.app`), or `RO_APP`. The balance rig finds ro-endgame-world beside this one, or at `RO_WORLD`.

| Script | Writes | From |
|---|---|---|
| `transcendent-third-classes/build.py` | Both class mods' `db/` tables (job stats, trees, skills, items, combos, mobs, statuses, spellbooks, elementals), `System/itemInfo.lua` | rAthena's renewal tables (`--rathena <checkout>`), per-class folders (`<class>/equipment.csv`, `drops.csv`, `combos.csv`), `SKILL_OVERRIDES`, `TREE_LEAVE_OUT`, `ITEM_FIELDS` |
| `expanded_class/expanded_class.py` | The shared engine `build.py` drives, for one class or a group | — |
| `transcendent-third-classes/build_skill_descriptions.py` | Each class mod's `skilldescript.lub` | `skill_descriptions/*.lua`, written to `skill_descriptions/STYLE.md` |
| `renewal-world-monsters/build_monsters.py` | All five renewal-world mods. Monsters go into monsters, minibosses or mvps by `is_mvp()` and kind. It also runs the gear, cards, sets and itemInfo builds. | renewal's `mob_db.yml`, `monsters.csv` (per-monster scales), `steps.csv`/`ladder.csv` (level steps), `monster_maps.csv` (spawns) |
| `renewal-world-monsters/build_equipment.py`, `build_cards.py`, `build_combos.py`, `build_iteminfo.py`, `itemdesc.py` | Gear, cards, sets, the client's item text, and readable item descriptions | `equipment.csv`, `cards.csv`, the owner's card draft |
| `tools/package.py` (each repository) | The release zips, `dist/<mod>-<version>.zip`, and the release notes from `CHANGELOG.md` | the mod folders |

**Measuring tools:**
- **The balance rig**, `tools/expanded_class/balance/`. `mkrig.sh` makes an isolated server plus database plus headless client with its own ports; `up.sh` and `build.sh` bring it up; `run_specs.py` runs a spec. Its README has the details.
- **Per-class specs:** `transcendent-third-classes/level175/*.json`, with the frozen results in `level175/README.md`.
- **The fight harness:** `companion-strategies/harness/`. It drafts companion parties at any level and measures kill time, wear, falls and experience. `rwsuite.py` holds the mod lists, and `calibrate_boss.py` runs the boss fights.
- **Party plans**, one per region and per boss: `companion-strategies/*.party.yml`.
- **Soft-cap tests:** `transcendent-third-classes/softcap/` (`invariant.py`, `tests.py` and the recorded stock baseline).

---

## The rules that hold everywhere

The owner settled each of these. A later change must keep all of them; if one seems wrong, ask rather than work around it.

**Levels and stats**
1. **Invariant:** a character with every base stat at or below 99 computes exactly as in stock rAthena. Run `softcap/invariant.py` after any change near stats or levels; it must report 0 differences.
2. Base level 175 and stat cap 150 apply only to the third classes and the five advancements, set per job in `job_stats.yml`, never server-wide. Everyone else stays at 99 (80 for baby classes).
3. **No base or job level in skill damage.** Level-scaled formulas read at most 99 (the level rule). Every class has a level test at 99/130/150/175, and a skill must hit the same at each.

**Classes**

4. **Upgrade, not sidegrade.** A third class comes after its transcendent class. It keeps every skill it had and adds its own tree.
5. **Never weaker after an advancement.** A kept skill is never scaled below what the earlier class did. A class mechanic (Kagerou's charms, for example) only ever adds.
6. **Power target:** a 175/70 third class does about **1.5×** the single-target damage of its 99/70 transcendent class. An advancement does about 1.5× its base class at its cap, which lands below a third class.
7. **Area skills:** per target, an area skill does at most **0.5** of the class's own single-target skill. The exceptions are the area casters (Warlock, Soul Reaper, a magical Kagerou/Oboro), which are held by the pack limit instead. Packs of five are cleared within 1.25× the transcendent class, or within 1.5× one-by-one where that class has no area skill. Killing one at a time must stay worthwhile for every class.
8. **Fixed-cast rule:** renewal's fixed cast time becomes 75 % after-cast delay plus 25 % cast time. A skill with a cooldown of 10 s or more keeps it as cast.

**Monsters and bosses**

9. **Monsters keep their renewal level.** Their strength comes from the level-step ladder, tuned by fights.
10. **Monsters must not be too easy for players.** The test party is companions in modest gear, and real players are stronger, so err on the hard side.
11. **A boss:** eight companions at its level wear down about **13 % of its HP per minute**, with **at most 10 falls per minute**. It need not die in a test, but its HP must head steadily towards a kill.
    - Pre-renewal's top MVPs, the yardstick, lose about 16 % per minute.
    - A miniboss dies to four companions in about 15 s.
12. **MVP: tactics first.** Exhaust tactics, counters and party composition in the plan before cutting a boss's damage or HP. Two hours per boss; after that, record it as open rather than keep tuning.
13. A plan that beats a boss is saved as its own `mvp-<boss>.party.yml`.
14. Anything flagged `Modes: Mvp` must pay MVP experience (`MvpExp > 0`).

**Items**

15. **Converted gear** is held to pre-renewal's best item of its kind plus one budget step. Weapons over the budget are cut, with ATK rounded down to a ten.
16. **Cards** are never stronger than pre-renewal's best card of the same slot for the same bonus. They never copy or make obsolete a pre-renewal card, and pre-renewal's own cards are never changed.
17. **Single-skill bonuses** on gear and cards keep renewal's effect at **a third**: at most +15 % skill damage per line, and a third of cooldown, cast and delay. A fixed cast becomes delay first (rule 8). The same goes for renewal's set bonuses.

**Measuring**

18. A number is the **median of at least three runs**. A target is met within 10 %. Use at most three tuning rounds per class or level step, then record the best as open.

---

## The phases

The run followed a written plan: eleven end-state points and phases 0 to 8. The owner added phase 9 and the follow-ups after the final report. Phases ran in order, and each was finished and committed before the next started.

### Phase 0: Base

- **What:** fresh work branches from upstream. The earlier work was brought over rather than started again: the strategy engine branch, the class mods branch, and the monster mod branch. The run also set up a status page and the first balance rig, and checked that a mod can require another mod.
- **How:**
  - The sources were merged whole, with no conflicts.
  - `requires.mods` in `mod.json` already existed, so mod dependencies are expressed there.
  - Rigs are separate Docker stacks with their own ports (`mkrig.sh`).
- **Why:** every later number comes from fights on rigs, so the rigs had to be isolated from the player's game and from each other. Bringing the old work over kept the skill implementations, gear, shops and NPCs that were already good.

### Phase 1: Level 175 and the soft cap

- **What:**
  - The new classes get base level 175, job level 70 and a stat cap of 150.
  - Above 99 a stat point counts for a third.
  - Base DEX above 99 stops shortening cast time.
  - The 99→175 experience rows and HP/SP tables.
- **How:**
  - Per job in the class mod's `job_stats.yml`. rAthena's stock stat-point table already runs to 275 with the classic formula, so the mod ships none.
  - The soft cap was first three battle settings in a fork commit (`stat_softcap`, …). The owner asked that rAthena open hook points instead of carrying the values. So it became the fork's Lua `player({base_stat, cast_dex})` hook (rathena PR #62), and the curve lives in `level175-core/lua/soft_cap.lua`.
  - `base_stat` runs at every place a raised base stat enters a calculation: the status calc, the status window bonus column, weight, Marionette, Beast Bane, and the Vacuum Extreme and Bind Trap resistances.
- **Why:**
  - Without a soft cap, 150 in a stat breaks pre-renewal's formulas, which assume 99 (instant cast at 150 DEX, for example).
  - As a hook, another mod can bring a different curve without touching rAthena again.
  - The invariant test (12 stock characters recorded on stock rAthena, compared field by field) proves that nothing changed for anyone at or below 99.
- **Tested:**
  - invariant 0 differences;
  - 64/64 soft-cap tests: casting at 150 DEX, Marionette, spending and resetting points, experience 99→175, and the caps per class.

### Phase 2: Strategy system

- **What:** companions can be drafted as third classes and advancements at any level from 99 to 175. The fight harness was extended to match.
- **How:**
  - The engine side, draft profiles (NEEDS 19), was done by the session that owns the population engine; this run never edits `third-party/population-engine/`.
  - The harness got exact levels and each class's kit and fixed gear (`GEAR=mid`).
  - The headless client got party chat. Without it roles were never set, so every fight before the fix was discarded as a reference.
  - `third-classes.party.yml` added plan rules for classes whose own skills the engine's rotation didn't use.
- **Why:** all balance is measured by companion parties fighting on rigs, so the new classes had to be playable by companions before anything could be measured.

### Phase 3: Classes

- **What:** all 13 third classes and 5 advancements were measured at 175/70, tuned and frozen.
- **How:**
  - **Upgrade:**
    - The class changer takes the finished class (99/70).
    - The trees keep every earlier skill.
    - Each class has its own job experience table.
    - The sidegrade route at rebirth was removed.
  - **Measuring:** a scripted player attacks a stat copy of the Abysmal Knight that can't be knocked back.
    - Builds are full, and melee takes DEX 60 first so it hits.
    - Per class: the median of three runs of the best single-target skill, of each own area skill per target, and of the pack of five, plus the level test.
    - The reference skill of each transcendent and expanded class is in `REFERENCE_ROTATIONS.md`. The first class showed the trap: Lord Knight's real single-target skill is Bowling Bash, not Spiral Pierce.
  - **Tuning:**
    - Damage factors are Lua `skill()` ratio hooks in `third_classes.lua` and one file per advancement.
    - Cast, cooldown and area changes are in `build.py` `SKILL_OVERRIDES`.
    - Three damage skills became single target to meet the area rule: Varetyr Spear, Hell Inferno, Soul Expansion.
  - **Level rule:** about thirty renewal formulas read the level directly (`LEVEL_IN_SKILL_DAMAGE.md`, and the owner's rule for them in `LEVEL_IN_SKILL_DAMAGE_RULE.md`). The fork's level helper `status_get_lv_dmg()` asks the mod's `level` / `job_level` hooks. `level175-core/lua/level_rule.lua` returns at most 99, and `heal_int.lua` / `coluceo_heal.lua` handle heals.
- **Why:**
  - Renewal gave nearly every third class an area skill that made its other skills obsolete and ended party play. The 0.5 area rule and the pack limits stop that.
  - The 1.5× target makes the advancement worth taking without leaving pre-renewal's classes behind.
  - The level rule stops damage from growing simply because the level is past 99.
- **Results:** single target is about 1.4–1.8× (Rune Knight 1.76, Royal Guard 1.81, Ranger 1.62, Sorcerer 1.60, Warlock 1.38–1.52, …). Genetic and Arch Bishop have no single-target skill of their own and use a kept one. Each class's record is in `level175/README.md`; the player-facing tables are in the mod's README.

### Phase 4: Ordinary monsters

- **What:** 115 renewal monsters, each at its renewal level, on 45 maps.
- **How:**
  - **The anchor:** fair pre-renewal endgame monsters (Abysmal Knight, Acidus, Bloody Knight) against a 99/70 party. That fight defines what a fair endgame fight is.
  - **The ladder:** level steps of ten (100…170). A monster belongs to the nearest step and is tested by a party of that step's level. Each step is about 5 % harder for its party than the step below was for its own.
  - **Strength from the step:** a monster's HP and attack are its step's reference value times its standing in renewal against monsters of its level (`steps.csv`, `ladder.csv`, `monsters.csv` for individual corrections).
  - **Raised for the owner's yardstick:** a well-geared party must still be pressed by a map pull of five, so every step from 100 got HP ×1.25 and attack ×1.15.
  - **Test budget per step:**
    - two third-class parties, one 99/70 party, and a mixed party with and without its 99/70 member;
    - packs of 1 and 3;
    - three runs each.
  - **Experience:** from the yardstick party's kill times at pre-renewal's anchor rate.
  - **Dewata and Malangdo** (renewal 43–91) sit in 70–99 and are balanced for ordinary pre-renewal parties (`BALANCING.md`).
- **Why:**
  - Pre-renewal has no fair monster above 99, so nothing can be compared "with a stock monster of the same level". The ladder climbs from something known.
  - Raw stats can't simply be extended: pre-renewal DEF/MDEF are percentages that stop making sense near 100.
  - Renewal's levels are kept so that renewal's equipment levels match where the gear drops.
- **Results:**
  - The well-geared party clears 76–100 % of each step's map pulls.
  - 99/70 parties struggle from 120, and the plain test party from 140; the owner accepted both.
  - Eight monsters have individual corrections, and the Scaraba eggs hatch when hit.

### Phase 5: Drops

- **What:** every converted monster drops what it drops in renewal. 54 renewal equipment items were converted.
- **How:**
  - `build_equipment.py` (the spec is `PORTING_EQUIP.md`, why it holds back is `RENEWAL_PERCEPTION.md`, the results are in `EQUIPMENT_REVIEW.md`) checks each item against a power budget: pre-renewal's best of its type plus one step. 25 items convert by rule and 29 by best attempt, with overrides in `equipment.csv`.
  - Gear sets per level step (`GEAR_SETS.md`) were fixed for the boss tests.
  - New cards were left out on purpose (phase 8).
  - **Check:** the first party in its step's gear set against the well-geared party without converted gear. Kill times were within a tenth at every step checked.
- **Why:**
  - Gear is levelled to where it drops, so renewal's levels are kept.
  - Cards work in any gear and reach level-99 characters, so new ones would blur every measurement. They came last.

### Phase 6: Bosses and MVPs

- **What:** 14 renewal bosses and minibosses on the ladder, with their spawns.
- **How:**
  - **Yardstick:** pre-renewal's own top MVPs fought by eight companions at 99. They lose 5–27 % of their HP per minute, with a median of 16, and cause 0–13 falls per minute. A converted boss aims at about 13 % with at most 10 falls (rule 11). Miniboss: about 15 s for four companions.
  - **Two porting faults fixed:**
    - Renewal-only second versions of monster skills had been dropped. Now pre-renewal's first versions are used, which gave Spider Chariot back its stone curse and Hell Judgement.
    - Boss spells used pre-renewal's INT; Leak's MATK of 1,284 had become 35. A boss's INT now gives its renewal magic attack, scaled like its physical attack and capped at twice it.
  - **Not ported on purpose:** renewal's `DamageTaken`.
  - **Tuning:** a party plan per boss first (rule 12), then stats. Two hours per boss.
- **Results:**
  - Met: Leak, Scaraba Queen, Nightmare Amon Ra, Spider Chariot, Boss Meow, Bestia, and the minibosses.
  - **Open:** Kraken (6 %, 22 falls) and the Gold Queen Scaraba (12 %, 18 falls).
  - Boss experience is the conversion's first figure, not calibrated from fights.
  - Dark Lord stays pre-renewal's own.

### Phase 7: Gear that lost its single-skill effects (added by the owner)

- **What:** 38 items whose renewal bonus named one skill had become broad stand-ins in phase 5. They got effects of their own.
- **How:** `SINGLE_SKILL_GEAR.md` gives the order of preference:
  1. a party role;
  2. a class theme, without naming a skill;
  3. a small proc.

  Effects stay within the slot's budget, and refining adds a second part at +7 or +9. Changes are made through `equipment.csv` `Effect`/`Script`.
- **Why:** a flat "+50 % to skill X" makes one skill the only one worth using. The item should still feel like it belongs to its class.
- **Later changed:** phase 9 brought the skill effects back at a third, beside these effects.

### Phase 8: Cards (added by the owner)

- **What:** the 95 cards that the converted monsters drop and pre-renewal lacks became pre-renewal cards.
- **How:** `build_cards.py`, with the rules in `CARDS.md`:
  - It starts from the owner's draft (`CARD_REBALANCE_DRAFT.yml` beside the script) and takes the weaker of the draft and renewal, number by number.
  - Each card is held to pre-renewal's cards of the same slot.
  - Flat MATK becomes a rate.
  - **An abuse check:** caps on immunities, resistances, reflects, drains and boss damage, and flags on autocasts, scaling, special flags, ignored defence, and drop or zeny bonuses. Flagged cards are listed for the owner.
- **Why:** cards are pre-renewal's main way to build a character. A card stronger than pre-renewal's best for its slot would make the old cards worthless and break the monster balance.

### Phase 9: Cards too like existing ones; skill effects back; skill descriptions (added by the owner)

- **Too-similar cards:**
  - `build_cards.py` compares every converted card with pre-renewal's cards of the same slot and with the other converted cards, by what each does, numbers aside. It flags a card that does the same, is a weaker copy, or makes an existing card obsolete.
  - The first run flagged 21 cards. Each was changed in `cards.csv`, with the reason, and the check now reports 0.
  - The Kraken Card keeps its bleeding autocast on Raid, for the Rogue line only.
  - Why: a copy adds nothing, and a card that makes a pre-renewal card obsolete changes pre-renewal itself.
- **Single-skill effects back, at a third** (rule 17):
  - `build_equipment.py` `scaled_skill()` (`SKILL_SCALE=3`, `SKILL_ATK_CAP=15`).
  - 38 items and 11 cards carry one.
  - Summoner skills stay as stand-ins, because no class here has them.
  - Why: the owner wanted the flavour kept but not dominant. "+50 % to one skill" read as mandatory.
- **Skill descriptions:**
  - 359 skills of the class trees showed no text in pre-renewal: the translation had nothing for the advancements, and only names for most third-class skills.
  - They were written in the client's formatting (colours, bold, italic, `skill_descriptions/STYLE.md`), with this game's numbers.
  - Now each class mod ships only its own entries, and the app merges them.
- **Status page item text:** `itemdesc.py` describes every item and card from its script at every refine level, for review.

### Follow-ups after phase 9

1. **Port check:** the owner asked what the port had missed. The check is in `port_check.md` in the workspace reports. Fixed:
   - The client's item text: `System/itemInfo.lua` per mod, 196 entries generated from the converted values. Without it, cards showed renewal's numbers or no text at all.
   - MVP rewards: `MvpDrops` were stripped and not rebuilt.
   - 15 renewal sets whose pieces all exist here, every bonus at a third.
   - Skills that could not work in pre-renewal:
     - Full Throttle and Help Angel had no status.
     - Moon Slasher's and Killing Cloud's statuses were missing.
     - Illusion - Shadow's clone monster was missing.

     The build now brings the statuses and monsters over from renewal (`STATUSES_FROM_RENEWAL`, `MOBS_FROM_RENEWAL`).
2. **rAthena opened up instead of hard-coded:**
   - The soft-cap settings were replaced by the `player()` hooks (PR #62), with base stats added to every hook's context.
   - A follow-up branch (`lua-status-hooks`) added a `status(name, {start})` hook and a `skill(name, {passive})` hook for the DEF buffs. It was never merged: rathena PR #52 (app 1.6.7) brought a fuller `status()` and passive `bonus`/`stats` hooks first, and the DEF buffs were ported to those (2026-10-20).
   - One small commit remained, `lua-level-call-sites` (PR #66, merged 2026-10-20): Prestige, Freezing Spell and Deep Sleep Lullaby read the level through the level helper, so `level_rule.lua` reaches them.
   - Every hook is documented in the fork's `skill_lua.hpp` header and `doc/extensions.md`.
   - Why: in this fork, behaviour that should be optional is a hook switched on by a mod. Values belong to the mod.
3. **One big mod split into eight.** The owner asked for smaller mods, so the split follows the table above, with `requires.mods` between them and `build_monsters.py` writing all five renewal-world mods. Two app features made the split possible:
   - skill descriptions merged by skill;
   - `mob_skill_db.txt` rows joined across mods.

   The row join is app PR #645 (`mods/mob-skill-rows`, merged 2026-10-20). The description merge was dropped: app 1.6.7 lays each mod's skill tables over the client's by itself.

   On 2026-10-21 the app's maintainer asked for the mods to live in their own repositories, listed as GitHub registry entries, to keep the app's pull request small and let the mods update by release. The split is by kind: classes here, renewal-world in ro-endgame-world. The scripts and harness moved with them; nothing in their output changed but the paths in the generated headers.
4. **Spider Chariot became an MVP.** It had the Mvp mode but paid no MVP experience: renewal leaves `MvpExp` commented out for 57 monsters. The rule is now that any `Modes: Mvp` monster is an MVP and pays MVP experience (`is_mvp()`). It was rebalanced as an MVP:
   - HP 4,487,372, ATK 8,587, MvpExp 110,664;
   - wear about 14 % per minute, about 9.7 falls per minute.
5. **What the skill descriptions turned up** (OPEN_QUESTIONS 33):
   - **Dead skills:**
     - Full Throttle, Help Angel, Illusion - Shadow, Moon Slasher and Killing Cloud were made to work.
     - Sacrament, Purify and Soul Division were removed from the trees (`TREE_LEAVE_OUT`).
     - The Ancilla item now starts its buff. Its SP part is 0 in pre-renewal: rAthena divides val2 by 100.
   - **Hundred Spear** became single target, because its factor had been landing on its splash.
   - **Flat DEF buffs** (Prestige, Echo Song, Golem's Soul, Remodel Mainframe) now give pre-renewal DEF equal to the damage cut they give in renewal. That is renewal's formula `1-(4000+D)/(4000+10D)` at a typical DEF of 300; MDEF uses `1-(1000+M)/(1000+10M)` at 100. This is in `third_def_buffs.lua` and `expanded_def_buffs.lua`. A server status's `on_start` runs before the server works out its values, so each hook computes the stock value with the server's formula (level counted to 99) and replaces it with `c:status_val()` once the status is on. Remodel Mainframe uses a passive `bonus` hook that takes back the difference on a Madogear.
     - Why: pre-renewal DEF *is* the percentage, capped at 99, so renewal's flat +100 made a character nearly immune. Prestige alone gave 127 DEF at level 175.
   - **Area skills that had no factor,** measured against each class's single target and then timed on a pack of five:
     - Diamond Dust and Earth Grave at 48 % and 44 % of renewal's ratio: 0.49 and 0.44 per target, the pack 1.16× and 1.14× the Professor's Heaven's Drive.
     - Magma Eruption's lava is fixed damage the ratio hook can't reach, and at renewal's 0.5 s tick one cast killed a whole pack, whatever the cooldown. The lava now ticks every 1 s, with a 12 s cooldown: the pack takes 18.8 s (1.36× Power Swing one by one), and on one target it does 0.28 of Power Swing.
     - Icebound Trap hits the whole pack with each burst, so its cooldown is 3 s (1.16× the Sniper).
     - Hesperus Lit hits one target in this server, so it is held as single target: 11 % of renewal's ratio, 1800 dmg/s, 0.96 of Banishing Point (measured on the committed mod).
     - Rampage Blaster and Howling of Lion were slower on a pack than single target one by one: 250 %, giving 1.28× and 1.22×.
     - Gate of Hell was raised to Sura's band (2.06×).
   - **Elemental spirits** fight but give their master no status: pre-renewal's skill table has none for their skills. The owner chose to leave it that way. With renewal's statuses, Diamond Dust, Earth Grave and Varetyr Spear would be 13–42 % stronger, past their limits.
   - **Banding is left as is:** it reads the skill unit's level, which is always 1, and gives +30 DEF only with two or more Royal Guards.

---

## How to change something

**The loop:** edit the source (CSV, Lua or a build script) → run the build → `--check` → load on a rig → measure → median of three → update the README's numbers.

**Where each kind of change goes:**
- **A class's skill damage:** a Lua `skill()` hook in `third_classes.lua` or the advancement's file.
- **A skill's cast, cooldown or area:** `SKILL_OVERRIDES` in `build.py`.
- **A skill's description:** `skill_descriptions/<group>.lua`.
- **A monster:** `monsters.csv` (per-monster HP, attack and other scales). A step's strength is in `steps.csv`; spawns are in `monster_maps.csv`.
- **Gear:** `equipment.csv`. **Cards:** `cards.csv`. Every override carries a reason in its note.
- **A boss:** first its `mvp-<boss>.party.yml` plan, then `monsters.csv`. Fight it with eight companions at its level in its step's gear set (`--gearset --attrition`).
- **Something rAthena can't let a mod decide yet:** propose the smallest general hook in the fork, off by default and documented in `skill_lua.hpp` and `doc/extensions.md`. Never hard-code a value for one mod in rAthena or in the population engine.

**Before committing:**
- `build.py --rathena <checkout> --check`
- `build_skill_descriptions.py --check`
- `build_monsters.py --check`
- `tools/package.py` in each repository changed (versions match, archives within the app's limits)

**After a change near stats or levels**, also run `softcap/invariant.py`.

**Traps found on the way:**
- **Results swing:**
  - A single run proves nothing.
  - Criticals skew averages, so the level test compares the middle hit.
  - A build that misses (low DEX) gives nonsense.
  - A target that can be knocked back breaks the scripted client.
  - Packs are timed at 0.1 s.
- **Kept skills grow by themselves** with level and stats. A kept area skill can break the pack limit whatever the class's own skills do.
- **Rigs:**
  - After a rig's rathena moves, rebuild it clean (`build.sh clean`). Otherwise logins fail with `chrif_authok: Data size mismatch`.
  - A rig database made before the companion table got its `roam` column fails every companion save. `up.sh` adds the column.
- **Client:** roBrowser caches downloaded files by name in its own file system. A changed mod file can look as if it did nothing until that cache is cleared; the overlay fingerprint usually does it.

---

## What is open

- **Kraken and the Gold Queen Scaraba** are above the boss aim after their two hours. The owner has to decide whether they stay hard or are weakened.
- **Boss experience** is not calibrated from fights.
- **Single-skill strength:** whether a third, capped at +15 %, is right, and how it sits beside phase 7's own effects. The owner has to decide.
- **Nothing has been checked in the real client yet:**
  - the skill and item descriptions and the sets;
  - the new classes' sprites and the status window above 99. The server sends base stats as one byte each, so 150 fits.
- **Not measured:**
  - Spell Fist, Cluster Bomb, Acid Demonstration;
  - the Rune Knight's runes;
  - Oboro's own magic;
  - an elemental spirit's share of a Sorcerer's damage;
  - a class right after its change at job level 1.
- **The Sorcerer was re-timed** on the current build (2026-10-19). Heaven's Drive clears the pack in 36.6 s, not the 45.2 s once recorded. Against it Psychic Wave (39.1 s), Poison Buster (33.4 s, 1.10×) and Cloud Kill (36.0 s) are all within both limits, so no factor changed. Varetyr Spear reads 2700–2800 dmg/s because its factor was lowered from 116 to 98 on 2026-10-13; the README's table had kept the older figures.
- **Casters** were measured on a target without defence.
- The **Arch Bishop** has no attack of its own.
- **A charged Kagerou's kept magic** is over the pack limit by stats alone. It was left as is.
- **rAthena:** the pin is Flux159's `ragnarokoffline` at 62e435d, the merge of PR #66. Its tree is the same as the tested `lua-level-call-sites` commit (b348cab), so the 1.6.7 results above hold. The release after 1.6.7 has to ship this pin or a later one.

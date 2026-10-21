# Reference damage rotations: transcendent and expanded classes (pre-renewal, level 99, PvE)

For each class: what to play when it is measured for **sustained
single-target damage** on an ordinary monster, whether it has a real
**pack-clearing** skill, and, for five skills with quirks, how rAthena
pre-renewal computes them. Written for research request 1 (2026-10-11): phase 3
measures every third class against its transcendent class on an Abysmal
Knight's defences, and the comparison is only fair if the transcendent side
plays what players played.

**Where each statement comes from**

- **[rA]** read in rAthena, `upstream/ragnarokoffline` at `8ff133fb`, the
  pre-renewal branch of the code (`#ifndef RENEWAL`) and `db/pre-re/skill_db.yml`.
  Line numbers are for that commit.
- **[wiki]** iRO Wiki Classic, mostly through [BUILDS.md](https://github.com/BlaXun/ro-endgame-world/blob/main/tools/companion-strategies/BUILDS.md), which
  holds the builds, stats and sources. The pages are from 2010–2013 and
  describe the official server.
- **[judgement]** my conclusion from the two above. No source was found that
  compares damage per second between a class's skills, except for the Lord
  Knight. Where the choice of reference is a judgement, it says so.

The target named in the request: Abysmal Knight (`KNIGHT_OF_ABYSS`,
`db/pre-re/mob_db.yml`): level 79, HP 36,140, DEF 55, MDEF 50, VIT 64, INT 25,
AGI 68, LUK 50, Large, Demihuman, Dark 4. Three of these matter below: **Large**
(Spiral Pierce ×0.75, Pierce 3 hits), **VIT 64** (Acid Demonstration), and
**not Undead element, not Demon race** (Magnus Exorcismus does nothing).

---

## 1. The table

Cast and delay are the level-10 (or maximum) values in `db/pre-re/skill_db.yml`
[rA], in milliseconds, before DEX and Bragi. "ASPD" means no delay in the
database: the next use waits only for the attack animation.

| Class | (a) Sustained single target | Weapon | (b) Pack clearing | Basis |
|---|---|---|---|---|
| **Lord Knight** | **Bowling Bash** (`KN_BOWLINGBASH`): 2 hits of 500 % on a lone target (§2.1); cast 700 uninterruptible, ASPD. Second choice on a Large target: Pierce (`KN_PIERCE`), 3 hits of 200 %, no cast, ASPD | two-handed sword or spear; Pierce and Spiral need a spear | **Yes**: Bowling Bash (3×3 chain), Brandish Spear (spear, mounted) | [rA] for the hits; [wiki] for use: "Pierce or Bowling Bash will deal more damage per minute against MvPs if no Magic Strings is present" (Clashing Spiral page, 2010) |
| **Paladin** | **Shield Chain** (`PA_SHIELDCHAIN`): 5 hits, range 4, cast 1000, delay 1000. (Sacrifice, `PA_SACRIFICE`, is 9 % of max HP per swing and DEF-ignoring, a tank's tool, not a damage build) | one-handed weapon + heavy refined shield | **Yes**: Grand Cross (`CR_GRANDCROSS`), Holy magic, cast 3000, delay 1500, costs the caster HP | [wiki] via BUILDS.md; choice of Shield Chain over Sacrifice is [judgement] |
| **Assassin Cross** | **Sonic Blow with EDP** (`AS_SONICBLOW`, 8 hits, delay 2000), auto-attacks in between; or the katar crit auto-attack build. Soul Destroyer is the ranged alternative (§2.5) | katar | **Weak**: Meteor Assault (`ASC_METEORASSAULT`, 5×5 around self, cast 500, delay 500, no card bonus), Grimtooth (3×3, from hiding) | [wiki] via BUILDS.md; which of Sonic Blow / crit / Soul Destroyer is highest was not found: measure all three and take the best [judgement] |
| **Stalker** | **Double Strafe** (`AC_DOUBLE`, 2 hits, no cast, ASPD) with a bow; melee builds lean on a plagiarised skill (Bowling Bash, Triple Attack) | bow, elemental arrows | **None of its own**: Arrow Shower (5×5, knockback 2) and Raid (3×3) are weak; a copied Storm Gust or Bowling Bash is the class's real answer | [wiki]: the Stalker leveling page lists "Bowling Bash, Raging Trifecta Blow, DS". Measuring with its own skills and reporting a plagiarised one separately is [judgement] |
| **High Priest** | **None in general.** Holy Light (`AL_HOLYLIGHT`, cast 2000) is the only attack that works on anything; Turn Undead and Magnus need Undead/Demon | rod | **Only against Undead element or Demon race**: Magnus Exorcismus (cast 15000, delay 4000). Nothing on an Abysmal Knight | [wiki] via BUILDS.md; treat as a support class with no damage reference [judgement] |
| **High Wizard** | **The bolt of the target's weak element** (`MG_FIREBOLT` etc., level 10: 10 hits, cast 7000, delay 2800) or **Jupitel Thunder** (12 hits, cast 7000, no delay), with Mystical Amplification | staff/rod | **Yes**: Storm Gust (cast 15000, delay 5000), Meteor Storm, Lord of Vermilion | [wiki] via BUILDS.md ("the same build used two ways") |
| **Professor** | **Bolts under Double Casting** (`PF_DOUBLECASTING`), cast by hand (INT/DEX build) or through Hindsight auto-cast (AGI/INT, wants a Sage link) | rod or book; a fast weapon for Hindsight | **Modest**: Heaven's Drive (`WZ_HEAVENDRIVE`, 5×5 Earth, cast 5000, delay 1000). No Storm Gust class skill | [wiki] via BUILDS.md; hand-cast bolts as the reference (no Soul Linker needed) is [judgement] |
| **Champion** | **The combo**: Triple Attack → Chain Combo → Combo Finish → Tiger Fist → Chain Crush. Asura Strike is burst, not sustained (§2.3) | knuckle (mace for Asura) | **No.** In rAthena Combo Finish has a 5×5 splash (`SplashArea: 2`) [rA], a by-product, not a clearing skill | [wiki]: the combo build is "the highest sustained melee DPS of the class" (BUILDS.md) |
| **Sniper** | **Double Strafe** (`AC_DOUBLE`, no cast, ASPD) under True Sight. Falcon Assault (cast 1000, delay 3000) is burst | bow, elemental arrows | **Yes, modest**: Arrow Shower (5×5, knockback 2), Sharp Shooting (line, cast 2000, delay 1500), traps | [wiki] via BUILDS.md |
| **Clown / Gypsy** | **Arrow Vulcan** (`CG_ARROWVULCAN`, 9 hits, cast 3800, delay 3000 at level 10), Double Strafe in between is not possible with an instrument/whip: Musical Strike / Throw Arrow (cast 1500) fill | instrument / whip, elemental arrows | **No** (Arrow Shower needs a bow) | [wiki] via BUILDS.md |
| **Whitesmith** | **Cart Termination** (`WS_CARTTERMINATION`, no cast, ASPD, no card bonus, costs zeny, needs Cart Boost and a full cart) or auto-attack under Maximum Overthrust | axe or mace | **Marginal**: Cart Revolution (`MC_CARTREVOLUTION`, 3×3, knockback 2) | [wiki] via BUILDS.md |
| **Creator** | **Acid Demonstration** (`CR_ACIDDEMONSTRATION`, cast 1000, delay 1000, one Bottle Grenade and one Acid Bottle per cast) (§2.4) | any | **No** | [wiki] via BUILDS.md |
| **Ninja** | Magic: **Freezing Spear** (`NJ_HYOUSENSOU`, 12 hits, cast 7000, no delay) or Flaming Petals. Throwing: **Throw Kunai** (`NJ_KUNAI`, 3 hits, no cast, delay 1000). Final Strike is burst that leaves the Ninja at 1 HP | dagger (magic); kunai / huuma | **Yes**: Exploding Dragon (`NJ_BAKUENRYU`, cast 3000, delay 2000), Lightning Jolt, First Wind, Snow Flake Draft; Throw Huuma (3×3, damage split) | [wiki] via BUILDS.md ("Magic: fastest leveler") |
| **Gunslinger** | **Rapid Shower** (`GS_RAPIDSHOWER`, 5 hits, no cast, delay 1000) with a revolver, or **Tracking** (`GS_TRACKING`, cast 3000, no delay) with a rifle; auto-attack with Chain Action / Gatling Fever | revolver, rifle or gatling | **Yes**: Desperado (`GS_DESPERADO`, 7×7 around self, delay 1000), Spread Attack (shotgun) | [wiki] via BUILDS.md for Desperado and the auto-attack builds; Rapid Shower and Tracking as references are [judgement] ("community, unconfirmed" in BUILDS.md) |
| **Star Gladiator** | **The kicks** on auto-attack (`TK_STORMKICK`, `TK_DOWNKICK`, `TK_TURNKICK`, `TK_COUNTER`), with Wrath only against its Hatred targets | book (or bare) | **Only on its three Feeling maps**: Heat (`SG_SUN_WARM` etc.). Elsewhere no | [wiki] via BUILDS.md |
| **Soul Linker** | **Esma** (`SL_SMA`, 10 hits, cast 2000, delay 500) after Estin/Estun (cast 100, delay 500); monsters only | rod/dagger | **No** | [wiki] via BUILDS.md |
| **Super Novice** | Either **bolts** (`MG_FIREBOLT` etc.; the "instant cast" INT/DEX build) or **melee auto-attack** with Double Attack (STR/AGI). No class skill of its own | dagger or one-handed sword | **Weak**: Magnum Break (delay 2000), Thunderstorm, Fire Wall | [wiki]: iRO Wiki Classic, Super Novice (2012), builds "Instant Cast", "Super Flee", "God Strength Critical". Not in BUILDS.md |

Sorted for the plan's two treatments [judgement]:

- **A real pack-clearing skill:** Lord Knight, Paladin, High Wizard, Sniper,
  Ninja, Gunslinger.
- **None that works on an arbitrary pack:** Champion, Creator, Soul Linker,
  Clown, Gypsy, High Priest (Magnus only on Undead/Demon), Star Gladiator
  (Heat only on Feeling maps), Stalker (only by plagiarism).
- **In between** (a small or weak area skill that players did not clear packs
  with): Assassin Cross (Meteor Assault, Grimtooth), Professor (Heaven's
  Drive), Whitesmith (Cart Revolution), Super Novice (Magnum Break).

---

## 2. The five quirky skills in rAthena pre-renewal

### 2.1 Bowling Bash: two hits on a lone target is the rule, not a rig artefact

`src/map/skills/swordman/bowlingbash.cpp:43-115` (the `#else` branch is
pre-renewal); ratio 100 + 40 × level = 500 % at level 10 (line 32).

What happens on one cast, level 10:

1. The chain length is `c = (level − depth + 1) / 2` = 5 for the first target
   (line 46).
2. The target is pushed one cell in the direction the **caster faces or last
   walked** (lines 83, 92-97), not away from the caster. A target that cannot
   be pushed (boss, rooted) stays; the code goes on either way.
3. Enemies in the 3×3 around the cell the target was pushed towards are
   counted (line 104). The target itself is in that 3×3, moved or not, so the
   count is at least 1. Every *other* enemy there is hit by a recursive Bowling
   Bash with a shorter chain (line 106), and the target takes the
   **"self-collision" hit** (line 109).
4. The target takes the original hit (line 114).

So a lone target, movable or not, takes **2 × 500 %** per cast. That is the
official behaviour as well: iRO Wiki Classic, Bowling Bash (2010): "causing
damage in a 3x3 cell area that hits twice". The rig's Bowling Bash figure is
therefore what a player got.

It drops to **one hit** in two cases, both worth excluding on the rig:

- **A wall cell directly behind the target** in the push direction (line 95
  breaks before the second hit).
- **Gutter lines** (`bowling_bash_area: 0`, the default and official setting,
  `conf/battle/skill.conf:335-340`). The chain only works inside a 40×40 block
  of the map; the block is found from the caster's position minus the chain
  length (lines 50-55), so near a block's edge the push cell falls outside it
  and no collision happens. The wiki puts it as: every cell whose X or Y is
  divisible by 40, and the five cells next to it. Fight with both the caster's
  and the target's X and Y at least 6 cells away from a multiple of 40.
  (`bowling_bash_area: 2..20` replaces the blocks with a square around the
  caster; that would be a deviation from stock.)

Other properties [rA, `skill_db.yml`]: cast 700 ms, cannot be interrupted
(`CastCancel: false`), no after-cast delay (ASPD decides), weapon element,
normal weapon damage: DEF, FLEE, size penalty, cards and masteries all apply.
Damage itself carries no knockback (`dmg.blewcount = 0`, line 27).

### 2.2 Spiral Pierce: weight, not ATK

`src/map/battle.cpp:4028-4054` (pre-renewal base damage), `3411-3416`,
`4920`; `db/pre-re/skill_db.yml` id 397.

```
per hit = ( weight × 0.8 × (100 + 50 × level) %  +  (STR / 10)² ) × size
size:    Small 125 %, Medium 100 %, Large 75 %
total  = per hit × 5      (HitCount 5; level 5: weight × 2.8 + …)
```

- `weight` is the weapon's weight as the player sees it (the database stores
  tenths; the code takes `weight × 8 / 100`). `(STR/10)` is an integer division
  before squaring.
- The weapon's ATK, the character's ATK, and the usual weapon-against-size
  table play **no part**. The skill ratio is 100 % in pre-renewal (the ratio
  function is renewal-only).
- **Ignores DEF** (`IgnoreDefense`). Can miss (no `IgnoreFlee`).
- Added afterwards: the **refine bonus and Star Crumbs** only. Masteries (Spear
  Mastery), spirit spheres and ATK-percent statuses (Provoke, Concentration's
  ATK, …) are switched off for it (`battle_skill_stacks_masteries_vvs`,
  lines 3411-3416, also used by `battle_get_atkpercent`, line 4358). **Aura
  Blade does not apply** (line 4920).
- Damage cards and the weapon's element do apply (no `IgnoreAtkCard`).
- Cast 1000, delay 2000 at level 5, spear only, range 4.

Spear weights in `db/pre-re/item_db_equip.yml`: Hunting Spear 420, Hell Fire
350, Brionac 300, Lance and Halberd 250, Pike 100. With a Hunting Spear and
STR 120 on a Large target: (420 × 0.8 × 3.5 + 144) × 0.75 = 990 a hit, about
4,950 a cast before refine and cards, once every three seconds. With a Pike it
is 318 a hit. **The rig's "test weapons" decide this number almost alone**: say
which spear was used. On an Abysmal Knight (Large) it also loses a quarter.

What players said [wiki, Clashing Spiral, 2010]: without Magic Strings it has
"awful DPM" and Pierce or Bowling Bash do more per minute against MVPs; with a
good Magic Strings a Spiral build "will likely dominate". It is the Lord
Knight's skill against players (Medium, high DEF) and for a Bragi party, not
its ordinary single-target damage.

### 2.3 Asura Strike: one blow, then five minutes without SP regeneration

`src/map/skills/acolyte/asurastrike.cpp`, `src/map/battle.cpp:3402`,
`4494-4496`, `src/map/status.cpp:5421-5424`; `skill_db.yml` id 271.

```
damage = base attack × (800 + 10 × current SP) %  +  250 + 150 × level
```

- Ratio capped at 500,000 % (`asurastrike.cpp:55-60`). The flat part is added
  after the ratio (`battle.cpp:4494`).
- **Ignores DEF and FLEE.** Element: none set in the database, so Neutral; the
  "forced neutral" list at `battle.cpp:3686-3692` is renewal-only.
- No masteries, refine bonus, Star Crumbs, sphere bonus or ATK-percent statuses
  (`battle.cpp:3402`). Damage cards are not excluded.
- On use: SP set to 0, Fury (Critical Explosion) ended, and `SC_EXTREMITYFIST`
  for 300 s (`Duration1: 300000`), which **stops natural SP regeneration**
  unless the Champion is under the Monk spirit (`status.cpp:5421-5424`). The
  caster moves 3 cells towards the target.
- Needs Fury and 5 spheres (cast 2000, delay 1000 at level 5), or follows
  Combo Finish / Chain Crush in a combo (`skill.cpp:8475-8494`).
- Not read this session: whether the "base attack" keeps the weapon's size
  penalty. Check before trusting a number on a Large target.

For a sustained measurement it is not a rotation: one cast empties the
Champion. Measure the combo as the reference, and Asura separately as burst
(damage of one cast at full SP), saying what feeds the SP if it is repeated.

### 2.4 Acid Demonstration: the target's VIT and the caster's INT, nothing else

`src/map/battle.cpp:6464-6470` (pre-renewal), `6643-6662`; `skill_db.yml`
id 490.

```
per hit = 0.7 × targetVIT × INT² / (targetVIT + INT)      (halved on players)
total   = per hit × level                                  (HitCount = level)
```

- **Misc** damage: no DEF, no MDEF, never misses (`IgnoreFlee`), Neutral.
  The element table is applied (line 6652), so Ghost armour reduces it.
- ATK, MATK, weapon and DEX do not enter. Only total INT and the target's VIT.
- Cast 1000, delay 1000; one Bottle Grenade (`Fire_Bottle`) and one Acid
  Bottle per cast.
- Not read this session: which card bonuses the misc card step
  (`battle_calc_cardfix(BF_MISC…)`, line 6643) lets through.

On the Abysmal Knight (VIT 64) with INT 120: 0.7 × 64 × 14,400 / 184 = 3,506 a
hit, **35,060 a cast**, against 36,140 HP: it dies to the second cast, about
17,500 damage a second. Against a VIT 10 monster the same cast does 6,646.
**The choice of test monster sets the Creator's reference by a factor of five**,
and at VIT 64 it is several times any other class's figure in the request (the
rig's Bowling Bash: 3,775 a second). A third class "1.5× its transcendent
class" measured this way inherits that. Either measure the Creator on a
second, low-VIT target as well, or state the VIT with the number. That it is
paid for in consumables per cast is the class's balance, as players saw it
[wiki, BUILDS.md].

### 2.5 Soul Destroyer: a weapon part and an INT part, added

`src/map/skills/thief/souldestroyer.cpp:19-21`, `src/map/battle.cpp:5257-5263`,
`6414-6418`, `3748-3753`; `skill_db.yml` id 379.

```
weapon part = normal attack damage × (100 × level) %        level 10: 1000 %
INT part    = 500 + random(0..499) + 5 × level × INT        level 10, INT 100: 5,500–5,999
damage      = weapon part + INT part
```

- **Weapon part:** reduced by DEF, can miss, takes the weapon's element, but
  **no damage cards** (`IgnoreAtkCard`) and therefore **no EDP**: the EDP bonus
  sits behind `!nk[NK_IGNOREATKCARD]` (`battle.cpp:3748-3753`). This agrees
  with the wiki ("EDP does not affect Soul Breaker", BUILDS.md).
- **INT part:** a misc attack that ignores FLEE and element
  (`battle.cpp:6416-6417`), added to the weapon damage at
  `battle.cpp:5258-5262`. No DEF.
- Range 9, cast 700, delay 2800 at level 10. One hit.
- Not read this session: whether the INT part still lands when the weapon
  part misses. The wiki says it "never misses"; the code path was not traced.

With delay 2800 it is a slow, steady ranged skill: one cast every 3.5 s
without Bragi. For an Assassin Cross that can stand next to the target, Sonic
Blow with EDP is the likely higher figure; Soul Destroyer is the reference only
for the INT build or where the fight must be ranged [judgement].

---

## 3. What was not found

- **No damage-per-second comparison between a class's own skills** in any
  fetched source, except the Lord Knight sentence quoted above. For Assassin
  Cross (Sonic Blow, crit, Soul Destroyer), Gunslinger (Rapid Shower,
  Tracking, auto-attack), Whitesmith (Cart Termination, auto-attack) and Ninja
  (magic, kunai) the table names the candidates; the rig can settle them by
  measuring each and taking the best, which is also what a player would have
  done.
- **Stalker and Super Novice** have little written about PvE damage. The
  Stalker row rests on one leveling page that itself says it is outdated; the
  Super Novice row on one wiki page.
- Searched: iRO Wiki Classic skill and class pages (Bowling Bash, Clashing
  Spiral, Pierce, Super Novice, Stalker leveling), and web searches for
  pre-renewal Lord Knight, Stalker and Super Novice damage comparisons. No
  forum threads with numbers turned up.

## Sources

- rAthena `upstream/ragnarokoffline` (`8ff133fb`): `src/map/battle.cpp`,
  `src/map/skills/swordman/bowlingbash.cpp`, `…/swordman/spiralpierce.cpp`,
  `…/swordman/pierce.cpp`, `…/acolyte/asurastrike.cpp`,
  `…/merchant/aciddemonstration.cpp`, `…/thief/souldestroyer.cpp`,
  `src/map/status.cpp`, `conf/battle/skill.conf`, `db/pre-re/skill_db.yml`,
  `db/pre-re/mob_db.yml`, `db/pre-re/item_db_equip.yml`.
- iRO Wiki Classic: [Bowling Bash](https://irowiki.org/classic/Bowling_Bash)
  (last edited 27 August 2010), [Clashing Spiral](https://irowiki.org/classic/Spiral_Pierce)
  (27 August 2010), [Pierce](https://irowiki.org/classic/Pierce),
  [Super Novice](https://irowiki.org/classic/Super_Novice) (13 September 2012).
- iRO Wiki: [Stalker Leveling](https://irowiki.org/wiki/Stalker_Leveling)
  (flagged there as outdated pre-renewal material).
- [BUILDS.md](https://github.com/BlaXun/ro-endgame-world/blob/main/tools/companion-strategies/BUILDS.md) and its source list, for the builds behind each row.

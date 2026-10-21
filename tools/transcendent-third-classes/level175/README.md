# Level 175: the classes measured again

The classes were first balanced as sidegrades (`../balance.json`). As upgrades
they are measured again here, one spec a class, against their transcendent
class (the advancements: against their base class).

## The method

- **Who plays:** the rig's headless client (`../../expanded_class/balance`),
  at the pace the server allows. Not companions: a companion's damage is what
  its plan makes of the class.
- **The build:** `build#job#weapon#build#level`, every stat point spent.
  Melee: STR 90, DEX 60, AGI to 99, then on; ranged: DEX, AGI; casters: INT,
  DEX. Above 99 the main stats go on to 150. A test weapon, no consumables,
  SP refilled every 3 s.
- **The target:** the anchor (`dummy#6`), an Abysmal Knight's level,
  defences, stats, size, race and element, immovable, and `pack5`, five of
  them with its 36,140 HP, clustered.
- **A number** is the middle of three runs (`"defaults"` in the spec).
- **Single target:** the class's best sustained skill, kept skills included.
  The transcendent class's reference is in `REFERENCE_ROTATIONS.md`.
- **Pack:** `kotest/packtime.py`, requests every 0.1 s (at 0.3 s the slower
  client pace, not the class, decided the time).
- **The level test** (`kotest/leveltest.py`): the same base stats, weapon and
  job level at base level 100 and 175; the middle hit must be the same.
  Rule: base level and job level never enter a skill's damage.

## The targets

- best single target at 175/70: about 1.5 times the transcendent class's at
  99/70 (within 10 %). Kept skills grow freely with the character (owner,
  2026-10-11); where a kept single-target skill passes 1.5 times by itself,
  the class's own single-target skills are lifted to just above it (4 %), so
  the new skills stay the better choice, and that figure is the class's
  target;
- the class's own area skills: at most 0.5 of its own best single target, per
  target;
- the pack of five: at most 1.25 times as fast as the transcendent class
  where that has a real area skill, otherwise at most 1.5 times as fast as
  the same character killing them one by one. A kept area skill is not held
  to this (it grows freely); the figure is reported;
- skills built on the caster's HP or SP grow with the level's HP and SP
  tables; the owner accepts that, and the level test reports them apart.

## Rune Knight against Lord Knight (first class; three rounds; frozen)

Lord Knight 99/70: Bowling Bash 3781 dmg/s (its reference: two hits a cast on
a lone target), Spiral Pierce 1200; pack of five 15.2 s.

The Rune Knight keeps Bowling Bash, which reaches 1.70 times at 175 through
its stats alone. Kept skills grow freely, so the target for its own
single-target skills is just above that: 1.76 times.

| At 175/70 | dmg/s | against the Lord Knight | target |
|---|---|---|---|
| Sonic Wave (own) | 6662 | 1.76 | 1.76: met |
| Hundred Spear (own) | 6640 | 1.76 | 1.76: met |
| Bowling Bash (kept) | 6427 | 1.70 | grows freely |
| Wind Cutter, a target | 1252 | 0.19 of Sonic Wave | at most 0.5: met |
| Ignition Break, a target | 762 | 0.11 | met |
| Dragon Breath, a target | 287 | 0.04 | met |
| pack of five, Bowling Bash | 9.5 s | 1.60 times as fast | reported (kept area skill) |

Earlier levels (round 2 factors, before the last raise of about 15 %): Sonic
Wave 1.11 at 99, 1.40 at 130, 1.50 at 150. Round 3 at 150: 1.72.

Factors (`lua/third_classes.lua`): Sonic Wave 17 -> 68 -> 78, Hundred Spear
76 -> 295 -> 351 percent of renewal's ratio.

Level test on the build with the level hooks: Sonic Wave, Hundred Spear,
Bowling Bash, Wind Cutter and Ignition Break hit the same at level 100 and
175 with the same stats. Dragon Breath hits 638 and 1617: its formula reads
no level any more, but it is built on HP and SP, which the owner accepts.

Not measured: Enchant Blade, Giant Growth, the runes; the pack of five with
the round-3 factors; the class right after the change, at job level 1.

## Sura: frozen after round 3

Reference: the Champion's Occult Impaction under Zen, 2341 dmg/s. Kept at 175: 2.04×, so the
target for the Sura's own skills is 2.12× (1.91 to 2.33).

| At 175/70 | dmg/s | Ratio | |
|---|---|---|---|
| Knuckle Arrow | 5092 | 2.20× | met |
| Dragon Combo | 5294 | 2.28× | met |
| Tiger Cannon after Raising Dragon | 4078 | 1.76× | **not met**; three rounds used. It spends HP and SP, and the part built on them does not follow the factor (353 → 668 gave 1.11× → 1.76×) |
| Earth Shaker, Sky Net Blow, Lightning Ride, Rampage Blast, per target | 326 to 455 | 0.06 to 0.09 of single | within the limit |

Asura Strike and Gates of Hell are bursts built on SP and HP; they grow with the character
(owner's decision) and are not held to a target.

Pack of five: Champion (Occult Impaction, Zen) 138.0 s; Sura Dragon Combo 37.2 s, Knuckle Arrow
41.1 s: 3.7× as fast, against 2.2× on one target. The Champion deals 1309 dmg/s in the pack and
2341 on the anchor, unexplained; the Sura was not tuned on this figure.

## Ranger: frozen after round 2

Reference: the Sniper's Double Strafe, 1588 dmg/s; kept at 175: 1.52×, target 1.58×.

| At 175/70 | dmg/s | Ratio | |
|---|---|---|---|
| Aimed Bolt | 2576 | 1.62× | met |
| Warg Strike | 2519 | 1.59× | met |
| Arrow Storm, per target | 863 at factor 65 | 0.34 of single | within the limit; factor then 60 for the pack |
| Cluster Bomb | not measured | | the trap run returns 0 in two of three |

Pack of five: Sniper Arrow Shower 79.7 s (Double Strafe 117.3 s); Ranger Arrow Storm 46.7 s at
factor 65 (1.71×), 50.4 s at 60 (**1.58×, met**); kept Double Strafe 78.4 s, Aimed Bolt 81.6 s.

## Wanderer: frozen after round 3

Reference: the Gypsy's Throw Arrow with the whip, 928 dmg/s; kept at 175: 1.16×.
Reverberation 1305 dmg/s, **1.41×, met**. Reverberation is shared with the Minstrel and stronger
in the Wanderer's hands, so the Wanderer keeps 74 % of the Minstrel's factor.

## Genetic: frozen without changes

No single-target skill of its own. Kept Acid Terror 2820 dmg/s at 175, 2.17× the Creator's 1302.
Cart Cannon, Cart Tornado, Spore Explosion, Crazy Weed per target: 0.16 to 0.23 of that.
Not measured: Acid Demonstration (the Creator's real reference; its damage follows the target's VIT).

## Mechanic, Guillotine Cross, Shadow Chaser: frozen after round 2

| Class | Reference (dmg/s) | Own single-target skills at 175 | Kept at 175 | Target | Areas per target |
|---|---|---|---|---|---|
| Mechanic | Whitesmith Cart Termination 3816 | Power Swing 1.79×, Boost Knuckle 1.81×, Vulcan Arm 1.79× | 1.79× | 1.86× (1.67 to 2.05): met | 0.06 to 0.24 of single |
| Guillotine Cross | Assassin Cross Sonic Blow 604 | Cross Impact 1.45×, Rolling Cutter + Cross Ripper Slasher 1.35× | 1.41× | 1.5× (1.35 to 1.65): met | Rolling Cutter 0.49 |
| Shadow Chaser | Stalker Double Strafe 1444 | Triangle Shot 1.54× | 1.15× | 1.5×: met | Fatal Menace 0.37 |

Level tests: no differences on the patched build.

## Royal Guard: frozen after round 3

Reference: the Paladin's Rapid Smiting, 1045 dmg/s; kept at 175: 1.70×, target 1.77× (1.59 to 1.95).
Banishing Point 1877 dmg/s, **1.81×, met**. Overbrand, Earth Drive, Cannon Spear, Moon Slasher per
target: 0.40 to 0.45 of it.

## Pack of five, other classes

| Transcendent (99) | s | Third class (175) | s | As fast |
|---|---|---|---|---|
| Assassin Cross, Meteor Assault | 54.2 | Guillotine Cross, kept Meteor Assault | 34.8 | 1.56× (its own Rolling Cutter: 92.5 s) |
| Whitesmith, Cart Termination | about 51 (from 3816 dmg/s; the pack run had no loaded cart) | Mechanic, Axe Tornado | 31.8 (Arms Cannon 34.3) | about 1.6× |

Single-target skills (Sonic Blow, Cross Impact, Power Swing) do not finish the pack inside the
180 s limit; their time is the pack's HP over their dmg/s.
| Stalker, Double Strafe | over 180 (four of five down; about 215) | Shadow Chaser, Fatal Menace | 45.9 (kept Double Strafe 112.5) | about 4.7×: **over**. The Stalker has no area skill of its own, so any area skill beats it by far; Fatal Menace is 0.37 of Triangle Shot per target and was left |

Triangle Shot killed only two of the five in 180 s, far less than its 2218 dmg/s on the anchor
predicts; not explained.

## Warlock: frozen

Measured on the plain dummy and the plain pack (OPEN_QUESTIONS 20). Reference: the High Wizard's
amplified Jupitel Thunder, 2788 dmg/s; pack: Meteor Storm 31.4 s (Lord of Vermilion 48.4 s, Storm
Gust 59.3 s).

| At 175/70 | dmg/s | Ratio | Plain pack |
|---|---|---|---|
| Hell Inferno | 4236 | 1.52× | 59.0 s, single target (renewal's splash removed: it cleared the pack in 11.3 s) |
| Soul Expansion | 4113 | 1.48× | 78.6 s, single target (was 16.6 s) |
| Tetra Vortex | 3856 | 1.38× | |
| Chain Lightning, one target | 3874 | 1.39× | 32.1 s |
| Crimson Rock / Jack Frost / Frost Misty / Comet | 1915 / 1992 / 1828 per target | | 24.5 / 27.2 / 32.7 / 31.9 s: at most 1.28× the High Wizard (limit 1.25×) |
| kept Jupitel Thunder / Meteor Storm | 3442 / 2303 | 1.23× / 1.28× | Meteor Storm 24.4 s, Storm Gust 47.2 s |

Factors for Tetra Vortex and Chain Lightning sit on the skills that deal the hits
(WL_TETRAVORTEX_*, WL_CHAINLIGHTNING_ATK). Four measuring runs: the first was on the anchor, the
third had those two factors on the parent skills, where they do nothing.

## Minstrel: frozen after round 3

Reference: the Clown's Musical Strike, 1032 dmg/s (kept at 175: 1.19×). Reverberation 1452, 1.41×;
Metallic Sound 1502, 1.45×. Pack: Great Echo 99.1 s, Severe Rainstorm 104.7 s against about 127 s
one by one (calculated): at most 1.28×. The Wanderer measures 110.6 s and 105.0 s.

## Sorcerer: frozen

Measured on the plain dummy and the plain pack. Reference: the Professor's Fire Bolt under Double
Casting, 1830 to 2141 dmg/s over four runs (middle 1996); pack: Heaven's Drive 45.2 s.

| At 175/70 | dmg/s | Ratio | Plain pack |
|---|---|---|---|
| Varetyr Spear | 3188 to 3233 | 1.60× of the middle reference (1.62× and 1.74× in its own rounds) | 73.2 s, single target (renewal's 9×9 splash removed: 10.2 s) |
| Psychic Wave / Poison Buster / Cloud Kill, per target | 1041 / 1190 / 1067 | 0.33 to 0.37 of Varetyr Spear | 41.0 / 35.7 / 37.3 s: at most 1.27× the Professor (limit 1.25×) |
| kept Fire Bolt, Double Casting / Heaven's Drive | 2221 / 1146 | 1.21× / 1.28× | Heaven's Drive 36.0 s |

Not measured: Spell Fist (the run reads 219 dmg/s, which is the rod's auto-attack; the skill was
not active in it), Earth Grave, Diamond Dust. Level test: Varetyr Spear's three hits at level 175
read about 12 % under those at 100 with the same stats; no growth with level.

## Arch Bishop: frozen

Measured on the plain dummy and the plain pack. The High Priest's only general attack is Holy
Light, 610 to 636 dmg/s; the Arch Bishop keeps it and it grows to 1130 to 1198 at 175 (1.78× to
1.96×). The class has no single-target skill of its own: Adoramus hits 7×7, Judex 3×3.

| At 175/70 | Per target | Plain pack | |
|---|---|---|---|
| kept Holy Light | 1130 dmg/s | 244.8 s, one by one | |
| Adoramus (factor 5) | 257 dmg/s, 0.23 of Holy Light | 174.6 s | 1.40× as fast: met (limit 1.5×) |
| Judex (factor 8) | 289 dmg/s, 0.26 | 156.9 s | 1.56×: within a tenth of the limit |

The pack limit, not the 0.5 rule, decides here: at 0.47 of Holy Light per target both skills
cleared the pack about three times as fast as Holy Light does. OPEN_QUESTIONS 21 asks whether the
class should get a real attack. Healing is set in phase 4 (lua/heal_int.lua).

Rune Knight, pack of five with the final factors: Lord Knight Bowling Bash 15.2 s; Rune Knight kept
Bowling Bash 9.2 s (1.65×, a kept skill), Wind Cutter 30.3 s, Ignition Break 48.3 s, Sonic Wave one
by one 45.0 s. Its own area skills are slower than the Lord Knight's Bowling Bash.

## Kagerou and Oboro: frozen after round 2

The advancements aim at about 1.5× their base class at level 99, or just above a kept skill that
grows past that. References (Ninja 99): Throw Huuma 321, Throw Kunai 251, Ice Spear 2112 (plain
dummy), Exploding Dragon 1195 per target.

| At 175 | dmg/s | Ratio | |
|---|---|---|---|
| Cross Slash + Soul Cutter | 656 | 2.04× Throw Huuma | kept Throw Huuma 1.78×; band 1.67 to 2.04: met |
| Ice Spear, ten water charms (Kagerou) | 3579 | 1.69× | kept Ice Spear 1.42×; band to 1.73: met |
| Swirling Petal / Kunai Explosion, per target | 320 / 323 | 0.49 of Cross Slash | met |
| Kamaitachi, ten wind charms, per target | 3078 | 2.58× the Ninja's Exploding Dragon | exempt from the 0.5 rule (magical Kagerou) |

Charms keep 7 % of their bonus (it was 48 %; OPEN_QUESTIONS 22). Packs: Ninja Exploding Dragon
32.5 s, Kamaitachi 32.4 s (plain pack); Kagerou Kamaitachi 25.0 s without charms and 23.1 s with
ten, Exploding Dragon 26.3 s and 23.4 s: 1.30× by the kept spells alone, 1.40× with charms,
against a limit of 1.25×. **Over, and left:** the kept spells' growth is past the limit before a
charm is held. Swirling Petal 118.1 s and Kunai Explosion 112.9 s on the anchor pack (Cross Slash
one by one: about 275 s, calculated; the run did not finish).

Not measured: the Oboro's own magic. Its run cast Zangetsu on itself, which lowers MATK when HP
and SP have the wrong parity (1.10×, and the level test's only difference).

## Star Emperor: frozen after round 3

Reference: the Star Gladiator's kicks at 99, which read 132, 146 and 111 dmg/s in three rounds (the
kicks follow random stance procs; middle 132). Kept at 175: kicks 295, 299, 269 (middle 295,
2.2×), attacks 268. Target just above the kept kicks: about 2.3× (2.1 to 2.5).

| At 175 | dmg/s | Against 132 | |
|---|---|---|---|
| Prominence Kick + Solar Burst (factor 26) | 274 | 2.1× | met |
| Attacks under the stances, with Falling Star (factor 6) | 336 | 2.5× | at the top of the band. Falling Star itself adds about 8 dmg/s; at factor 15 it added about 45 (381, 2.9×). The gain is the stances on the auto-attack |
| New Moon + Full Moon Kick, per target | 127 | 0.46 of Prominence Kick | met |

All figures are low next to other classes (a Lord Knight's Bowling Bash is 3781): a hit is 112
with the test book (ATK 150). Not looked into; the ratios are within the class.

## Rebellion: frozen after round 3

Reference: the Gunslinger's Rapid Shower at 99, 1621 dmg/s (Tracking 782; Desperado 3198 per
target). Kept at 175: Rapid Shower 1.19×, Desperado 1.07×.

| At 175 | dmg/s | Ratio | |
|---|---|---|---|
| Rifle: Mass Spiral + Anti-Material Blast | 2399 to 2645 | 1.48× to 1.63× | met |
| Shotgun: Banishing Buster + Slug Shot + Shatter Storm | 2223 | 1.37× | met |
| Grenade launcher: Howling Mine + Dragon Tail (46) | 2501 | 1.54× | met (three single runs after the last change) |
| Fire Dance / Round Trip / Fire Rain / Shatter Storm, per target | 1239 / 1115 / 790 / 809 | 0.47 / 0.42 / 0.30 / 0.31 of the rifle | met |

Round Trip's second hit (RL_R_TRIP_PLUSATK, dealt when the target cannot be pushed back) has its
own factor: unscaled it was most of the skill on a monster that cannot be knocked back. The grenade
runs set STR 70: the DEX build could not carry the launcher and every cast was refused. No pack run:
the Gunslinger's Desperado deals 3198 per target, more than any Rebellion area skill.

## Pack limits, later timings (these replace the pack figures in the class records above)

The first class records used a flat 1.5× against the transcendent class. The plan's limits are:
at most 1.25× as fast as the transcendent class where it has a real area skill; where it has none,
at most 1.5× as fast as the same character killing the five one by one.

| Class | Skill, factor | Pack | Against | |
|---|---|---|---|---|
| Ranger | Arrow Storm 47 | 65.2 s | Sniper Arrow Shower 79.7 s | 1.22×: met (kept Arrow Shower at 175: 52.0 s) |
| Shadow Chaser | Fatal Menace 7 | 69.0 s | Triangle Shot one by one, about 88 s | 1.28×: met |
| Royal Guard | Overbrand 6 / Earth Drive 38 / Moon Slasher 62 / Cannon Spear 39 | 76.7 / 69.8 / 69.3 / 71.4 s | Paladin Grand Cross 87.0 s (Rapid Smiting one by one 178.9 s) | 1.13× to 1.26×: met |
| Minstrel | Great Echo 32 / Severe Rainstorm 26 | 99.1 / 104.7 s | one by one about 127 s (calculated) | 1.28× / 1.21×: met |
| Wanderer | Great Echo / Severe Rainstorm | 110.6 / 105.0 s | one by one about 139 s (calculated) | met |
| Guillotine Cross | kept Meteor Assault | 34.8 s | Assassin Cross Meteor Assault 54.2 s | kept; own Rolling Cutter 92.5 s |

Reverberation is one factor (25) for Minstrel and Wanderer; the 74 % share for the Wanderer
mentioned above was removed again (Wanderer 1.46×, Minstrel 1.41×).

## Soul Reaper: frozen after round 3

Reference: the Soul Linker's Estin + Esma at 99/50 on the plain dummy, 3632 dmg/s (Estun + Esma
3766). Target 1.5× (1.35 to 1.65).

| At 175 | dmg/s | Against 3632 | |
|---|---|---|---|
| Espa (factor 26) | 5083 | 1.40× | met |
| Espa + Eswhoo, soul energy refilled (Eswhoo 36) | 4921 | 1.35× | met, at the low edge |
| Estin + Esma, kept | 4448 | 1.22× | |
| Soul Curse + Curse Explosion, per target (13) | 1859 | 0.37 of Espa | |

Round 2 had Espa at 1.67× and was cut; round 3 landed lower than aimed (1.40×) and is inside the
band, so it stays. The Soul Linker has no area spell and its pack runs were unusable, so the 1.25×
pack limit cannot be measured; Curse Explosion is held to "five cursed monsters fall no faster than
to Espa one by one" (35.9 s against 35.2 s in round 2; OPEN_QUESTIONS 23). Level test: Espa 4148
at 99, 4618 at 130, 5025 at 150, 5083 at 175: stats, not level.

## Expanded Super Novice: frozen after round 3

Reference: the Super Novice at 99/99 on the plain dummy: Bash 1564, Fire Bolt 1110, attacks 589,
Thunderstorm 914 per target. Its own two skills are passives (Breakthrough: flat damage a hit and
MaxHP; Transcendence: MATK), which a hook cannot scale, so the kept skills pass 1.5× by
themselves: Bash 3470 (2.22×), Fire Bolt 1755 (1.58×), attacks 1666 (2.83×), Thunderstorm 1445
(1.58×). The second-class skills in its renewal tree are therefore set by the kept-skill rule:
single target just above the kept Bash (2.31×, 2.08 to 2.54), area just above the kept
Thunderstorm (at most 1.14× of it), with factors for this class only (`lua/super_novice.lua`).

| At 175 | before | factor | after | |
|---|---|---|---|---|
| Jupitel Thunder | 4107 | 88 | 3492 | 2.23× Bash: met |
| Holy Cross | 3860 | - | 3860 | 2.47×: met |
| Earth Spike Lv 5 | 1320 | - | | below the kept Fire Bolt, left |
| Meteor Storm, per target | 2355 | 61 | 1390 | 0.96 of Thunderstorm: met |
| Heaven's Drive, per target | 1711 | 84 | 1398 (0.97 of Thunderstorm) | met |
| Storm Gust, per target | 1043 | - | 1004 | 0.69: met |
| Lord of Vermilion, per target | 1089 | - | 1142 | 0.79: met |

Not measured: the pack of five (the per-target figures stand in for it), Back Stab and the other
second-class skills of the tree, and the class in a fight party. Its plain attacks at 2.83× are
left (OPEN_QUESTIONS 24).

## The order base < advancement < third class

Best own single-target figure at 175 against the base class at its cap: Kagerou Cross Slash 2.04×,
Rebellion 1.48× to 1.63×, Star Emperor 2.1× to 2.5×, Soul Reaper 1.40×, Expanded Super Novice
2.2× to 2.5×: every advancement is clearly above its base class. Against the third classes the
physical advancements are below (Rebellion 2645 dmg/s on the anchor against 5000 to 6900 for
Sura, Rune Knight, Mechanic); the casters on the plain dummy are not: Soul Reaper 5083 and a
charged Kagerou 3579 against Warlock 4236 and Sorcerer 3188, because a Soul Linker's Esma already
outdoes a High Wizard's Jupitel Thunder there (OPEN_QUESTIONS 25).

## Reopened rounds (2026-10-12; the owner lifted the three-round limit for the classes still off)

| Class | Change | Before | After | |
|---|---|---|---|---|
| Sura | Tiger Cannon 668 → 802 | 1.76× | 2.04× (4711 dmg/s) | aim 2.12×: met. Knuckle Arrow 2.21× as before |
| Mechanic | Power Swing 116 → 120, Boost Knuckle 94 → 97, Vulcan Arm 164 → 170 | 1.79 to 1.81× | 1.85×, 1.87×, 1.86× (7046, 7121, 7095 against 3816) | aim 1.86×: met. The reference run of this round had no loaded cart (207) and is not used; 3816 is round 1's |
| Guillotine Cross | Cross Impact 29 → 30, Rolling Cutter 17 → 19, Cross Ripper Slasher 9 → 10 | 1.45× / 1.35× | 1.51× / 1.53×; Rolling Cutter per target 0.50 | met |
| Kagerou / Oboro | area Ninja spells keep none of the charm bonus (single-target ones keep 7 %) | charged pack 1.40× a Ninja | Kamaitachi on the plain pack: Ninja 26.9 s, Kagerou 16.3 s without charms and 16.3 s with ten | the charms are out of it. What is left (1.65× on a pack without defence; 1.30× on the anchor pack earlier) is the kept spell growing with 76 levels of INT, which the kept-skill rule lets grow. Not met against 1.25×, and not lowered: OPEN_QUESTIONS 27 |
| Sorcerer | Spell Fist keeps 26 % → 17 % of the bolt; Varetyr Spear 116 → 98 | Spell Fist was never measured with the build that plays it: with AGI 130 / INT 130 it did 4216 dmg/s (2.43× the Professor's Fire Bolt); the INT-only run had shown 291. Varetyr Spear read 3299 and 3339 in two more runs (1.8× to 1.9×), so the frozen 1.60× was a low reading | Spell Fist 2756, Varetyr Spear 2809; the reference read 1738 to 1965 over four runs (mean about 1830): 1.5× each | met |

Measured for the first time in the same pass, no change: Genetic's kept Acid Demonstration 896
dmg/s on the anchor (Creator 260; its Acid Terror does 2820); Ranger's Cluster Bomb 1066 per
target (0.41 of Aimed Bolt; one good run of three, the trap did not always land) and Firing Trap
1550 per target (0.60 of Aimed Bolt: over 0.5, and its weapon part is already at 8 %; what is left
grows with DEX and INT and the hook cannot reach it. Open). Kagerou's Exploding Dragon on the
plain pack: 23.4 s with and without charms, Ninja 32.5 s (1.39×).

Expanded Super Novice, pack of five (plain pack, 2026-10-13): Super Novice Thunderstorm 46.2 s;
at 175 the kept Thunderstorm 28.4 s (1.63× by stats), Heaven's Drive 26.1 s, Lord of Vermilion
34.8 s, Meteor Storm 37.5 s, Storm Gust 46.0 s. No borrowed spell clears more than a tenth faster
than the kept Thunderstorm, which is the line the class was set to.

Rune Knight, buffs and runes (2026-10-13, first measurement, no change): Sonic Wave 6661 dmg/s;
with Enchant Blade 6660 (it only adds to plain attacks: 627 → 971); with Giant Growth 8251
(+24 %, for 30 s every 3 minutes: about +4 % over time; plain attacks 627 → 3816 while it lasts);
with the Fighting Spirit rune 8054 (+21 %, and that rune has no reuse limit here, so a Rune Knight
who carries them is at about 2.1× a Lord Knight rather than 1.76×. Consumables are not counted in
any class's figure, so it is left and noted). A Rune Knight at 99/70 does 0.92 of a Lord Knight's
Bowling Bash (3472 against 3774).

Ranger traps (2026-10-13): Firing Trap did 1550 per target, 0.60 of Aimed Bolt, with its weapon
part already at 8 %; the rest grows with DEX and INT and no factor reaches it. A cooldown instead
(Firing Trap and Icebound Trap): 2 s gave 568 (0.22), 1 s gives 1033 (0.40): kept at 1 s. Cluster
Bomb read 1066 in one run and nothing in five others (the test rarely lands the trap): not settled.

Kagerou and Oboro, the owner's rules of 2026-10-13: a Ninja spell is never weaker on them than on
a Ninja, and every charm of its element adds to it, as in renewal: renewal's per-spell points
scaled to 60 %. Measured at 175 on the plain dummy: Ice Spear 3197 without charms (Ninja 2140),
7315 with ten (Oboro 7111); Kamaitachi per target 2823 and 5730 (Ninja 1921); Exploding Dragon
1620 and 2686 (Ninja 1188). 16th Night doubled that again (14,162) by halving the cast time and
was always up; it is a 30 s burst every 3 minutes now (build.py). Release Ninja Spell as the only
attack: 920. Against the Warlock (Hell Inferno 4028, Soul Expansion 4073; Recognized Spell and
Amplification do not raise sustained damage) a charged Kagerou is ahead on one target; that is
accepted, the Warlock's place being area damage. Wide pack (eight plain monsters three cells
apart around the caster), seconds: High Wizard 99 Lord of Vermilion 54.2, Meteor Storm 110.8,
Storm Gust 263.1; Warlock 175 Comet 30.9, Chain Lightning 57.0, Jack Frost 85.8, Crimson Rock
95.0, kept Meteor Storm 101.8, kept Storm Gust 189.3, Frost Misty not finished (it freezes);
Kagerou with ten charms Kamaitachi 71.1 (Oboro 70.0), Exploding Dragon 125.5 (Oboro 121.7).
Ice Meteor with ten charms 132.3; without charms Kamaitachi 130.1, Exploding Dragon 191.6, Ice
Meteor 433.5; Ninja 99 Kamaitachi 199.6, Exploding Dragon 269.8, Ice Meteor 545.8 (these runs
need `carry#0` and 400 stones: `wide_long3.sh`). The Warlock's best clears it 2.3× as fast as the
charged Kagerou's best, so `CHARM_KEPT` stays at 60 and the class is closed.

Expanded Super Novice, the owner's rule of 2026-10-13: its second-class skills at 75 % of what the
third class keeping them does at 175/70 (runs: super_novice_owners.json; plain dummy, no Amplify).
Warlock Jupitel Thunder 3754, Storm Gust 980 a target, Lord of Vermilion 930, Meteor Storm 1894;
Royal Guard Holy Cross 3210; Sorcerer Heaven's Drive about 1130. The Expanded Super Novice had
3575 / 1033 / 1165 / 1410 / 3860 / 1440 (95, 105, 125, 74, 120, 127 %). Factors now Jupitel 71,
Holy Cross 60, Storm Gust 73, Lord of Vermilion 62, Meteor Storm 61, Heaven's Drive 51: 3003 / 769 /
697 / 1422 / 2450 / 802 (80, 78, 75, 75, 76, 71 %; Jupitel reads 5 % either way between runs).
At 99: High Wizard Jupitel Thunder 2983, Paladin Holy Cross 1538.

Soul Reaper, Curse Explosion (owner, 2026-10-13: an area skill must have an edge over the class's
single-target skill on a pack): factor 13 gave the cursed plain pack 35.9 s against Espa one by one
36.5-37.5 s; 19 gave 21.4 s; 16 gives 24.4 s (1.5x as fast as Espa; aim 1.4x). Kept at 16.


# transcendent-third-classes

Renewal's **third classes** in pre-renewal, as the step **after** the
transcendent classes, and level **175** for them.

A transcendent class at base level 99 and job level 70, with no skill
points left, advances to its third class at the Valkyrie's hall. It keeps
every skill it has (first, second and transcendent class) and adds the
third class's own. Its job level starts again at 1 and runs to 70, with
skill points of its own, and its base level, HP and SP go on from 99 to
175. There is no other way to a third class, and the step cannot be
undone.

rAthena's pre-renewal server already knows the third classes: the classes
and their skills are compiled in. What pre-renewal lacks is the data
(tables, a skill tree, renewal's skill entries) and a way to become one.
This mod supplies it.

> **Measured at 175/70.** The classes were first built as sidegrades,
> equal to their transcendent classes. They are upgrades now, and the
> figures in the class sections below are from the level 175 work: about
> 1.5 times the transcendent class's single-target damage at 175/70.

| Third class | Advances from | Changer |
|---|---|---|
| Guillotine Cross | Assassin Cross | `valkyrie 42 58` |
| Shadow Chaser | Stalker | `valkyrie 55 58` |
| Arch Bishop | High Priest | `valkyrie 42 42` |
| Rune Knight | Lord Knight | `valkyrie 42 39` |
| Royal Guard | Paladin | `valkyrie 55 39` |
| Warlock | High Wizard | `valkyrie 42 47` |
| Sura | Champion | `valkyrie 55 42` |
| Ranger | Sniper | `valkyrie 42 55` |
| Minstrel (male) | Clown | `valkyrie 55 54` (the Wandering Minstrel) |
| Wanderer (female) | Gypsy | `valkyrie 55 56` |
| Genetic | Creator | `valkyrie 55 50` |
| Mechanic | Whitesmith | `valkyrie 42 50` |
| Sorcerer | Professor | `valkyrie 55 47` |

Each third class's changer stands right beside its transcendent class's
stock changer, on the wall side.

The expanded advancements (Kagerou and Oboro, Rebellion, Star Emperor,
Soul Reaper, the Expanded Super Novice) are their own mod,
**expanded-classes**. Both need **level175-core**, which holds what they
share: the soft cap for base stats above 99 and the rule that keeps base
level out of skill damage.

### Level 175

Only these classes pass base level 99; every other class is untouched.
Above 99 a base stat counts for a third and base DEX gives no cast speed
(level175-core). Experience: 99 to 100 costs what a transcendent class's
98 to 99 costs, and the cost rises evenly to twice that at 174 to 175. The
new job levels cost 14 billion job EXP in all, which ends them at about
base level 150.

### Skill descriptions

Pre-renewal's English translation has only a name for most third-class
skills. The mod ships the descriptions of its skills
(`data/luafiles514/lua files/skillinfoz/skilldescript.lub`, 271 entries)
with this game's numbers, in the translation's colours plus bold and
italic; the app merges them into the client's table by skill, so it needs
an app that does (see `mod.json`).
`tools/transcendent-third-classes/build_skill_descriptions.py`
builds them from `skill_descriptions/*.lua` (`STYLE.md` there).

### Area damage

Renewal gave almost every third class area attacks it could spam, and
levelling became gathering a crowd and pressing one button. In
pre-renewal area damage belongs to a few classes. So here a **fighting
third class deals at most about half its best single-target damage to
each target of an area**: an area attack pays from about three targets,
and against one or two its single-target skills stay better. The casters
whose job area damage is (the Warlock, like the High Wizard; the Soul
Reaper; a magical Kagerou or Oboro) are exempt.

## Guillotine Cross

### The path

An **Assassin Cross at base level 99 and job level 70**, with no unspent
skill points, talks to the **Guillotine Cross** beside the Assassin Cross
changer in the Valkyrie's hall. The step cannot be undone, and you are
asked to confirm it.

The class's skill tree is renewal's Guillotine Cross tree with the
Assassin Cross's in it: it keeps every Novice, Thief, Assassin and
Assassin Cross skill it has learnt, and adds the Guillotine Cross's own
with the skill points of its 69 new job levels.

### How strong

- **HP and SP**: the Assassin Cross's tables, continued to level 175.
- **Job bonuses**: renewal's Guillotine Cross bonuses, topped up to +45,
  an Assassin Cross's total.
- **Gear**: everything an Assassin Cross wears, transcendent-only items
  included. Like an Assassin, it can carry a dagger in each hand.
- **Cast times**: 75% of each skill's renewal fixed cast becomes after-cast
  delay, which DEX does not reduce, and the rest is added to its cast time.
- **Skill damage**: scaled in `lua/third_classes.lua`, then measured at
  base level 175 and job level 70 against an Assassin Cross at 99/70:
  every stat point spent, a test weapon, no consumables, on a target with
  an Abysmal Knight's defences.

The Assassin Cross's reference is Sonic Blow, 604 dmg/s. The target for
the Guillotine Cross's own single-target skills is 1.5 times that, within
a tenth (1.35 to 1.65), and it is met. Only the ratios were recorded:

| At 175/70 | Against Sonic Blow at 99/70 |
|---|---|
| Cross Impact (own) | 1.51 |
| Rolling Cutter and Cross Ripper Slasher in turn (own) | 1.53 |
| Sonic Blow (kept) | 1.41 |
| Rolling Cutter alone, per target of its area | 0.49 of the class's single-target damage |

A pack of five such targets: the Assassin Cross clears it with Meteor
Assault in 54.2 s. The Guillotine Cross clears it with the Meteor Assault
it keeps in 34.8 s, 1.56 times as fast; a kept skill grows freely with the
character and is not held to the pack limit. Its own Rolling Cutter takes
92.5 s. The single-target skills (Sonic Blow, Cross Impact) do not finish
the pack within a run's 180 s.

With the same stats, the skills hit the same at base level 100 and at
175: base level counts in skill formulas only up to 99.

What the Guillotine Cross adds to the Assassin Cross's skills:

- **Rolling Cutter** builds up to ten counters; **Cross Ripper Slasher**,
  from up to 13 cells away, hits harder with each. The figure above needs
  the two alternated as fast as the server takes them.
- **Cross Impact** is the heavy hit. Renewal lets it fire twice a second;
  here its after-cast delay is 1.5 s at every level.
- **Dark Crow** marks a target for 20 s, once a minute: melee attacks on
  it, the party's included, deal 30% more per level (half on bosses).
  Cross Impact and Cross Ripper Slasher are ranged, so it does not raise
  them.
- **Weapon Blocking** parries a melee hit and opens **Counter Slash**
  (scaled like Cross Impact); **Hallucination Walk**, **Cloaking
  Exceed** and **Dark Illusion** are for survival and getting in.
- **Poisons**: the new poisons are brewed from herbs, as in renewal,
  and put on the blade with Poisoning Weapon. Venom Pressure is scaled
  to 40% from its ratio; it needs a poison on the blade.

Not measured at level 175: Counter Slash, Venom Pressure, Dark Crow's
bonus.

### Equipment

Two tiers, a katar and a kris each. Each raises two Guillotine Cross
skills and two Assassin Cross skills, so the weapon is worth carrying
before the change and after it. Transcendent classes only.

| Item | Level | Drops from |
|---|---|---|
| Venom Edge Katar | 70 | Medusa |
| Venom Edge Kris | 70 | Anubis |
| Guillotine Katar | 90 | Pharaoh |
| Guillotine Kris | 90 | Amon Ra |

The items borrow stock art, so the mod ships no sprites.

## Shadow Chaser

### The path

A **Stalker at base level 99 and job level 70**, with no unspent skill
points, talks to the **Shadow Chaser** beside the Stalker changer in the
Valkyrie's hall. The step cannot be undone, and you are asked to confirm
it.

The class's skill tree is renewal's Shadow Chaser tree with the Stalker's
in it: it keeps every Novice, Thief, Rogue and Stalker skill it has
learnt (Preserve, Full Strip, Reject Sword and Chase Walk among them),
and adds the Shadow Chaser's own with the skill points of its 69 new job
levels.

### Two stolen skills

A Stalker has one stolen skill, and Preserve to keep it for good. A
Shadow Chaser keeps both and gains a second slot:

- **Plagiarism**, as a Rogue's: every copyable skill that hits you
  replaces it.
- **Reproduce**: for five minutes after you cast it, a copyable skill that
  hits you goes into its own slot, at Reproduce's level (capped at what
  the caster used). Outside those five minutes nothing replaces it, so
  this is the slot you choose. It copies first and second class skills
  too, not only third class ones.

**Auto Shadow Spell** then casts a stolen spell by itself on your
attacks, at (its level + 5) / 2, no higher than the level you stole. It
takes Mage and Wizard spells and Heal, as in renewal, and this mod adds
**Turn Undead** and three ninjutsu: **Flaming Petals**, **Freezing
Spear** and **Wind Blade**. rAthena never auto-casts Holy Light or Magnus
Exorcismus, and the self-centred and catalyst ninjutsu would not place or
would cast for free, so those are left out.

### How strong

Measured at base level 175 and job level 70 against a Stalker at 99/70:
every stat point spent, a test weapon, no consumables, on a target with
an Abysmal Knight's defences.

The Stalker's reference is Double Strafe with a bow, 1444 dmg/s. The
target for the Shadow Chaser's own single-target skill is 1.5 times that,
within a tenth, and it is met:

| At 175/70 | Against Double Strafe at 99/70 |
|---|---|
| Triangle Shot (own) | 1.54 (2218 dmg/s) |
| Double Strafe (kept) | 1.15 |
| Fatal Menace, per target of its area | 0.37 of Triangle Shot |

A pack of five such targets:

| | Time |
|---|---|
| Stalker, Double Strafe one by one | over 180 s (four of five down when the run ended; about 215 s) |
| Shadow Chaser, Fatal Menace at 10% of renewal's ratio | 45.9 s |
| Shadow Chaser, Fatal Menace at 7% | 69.0 s |
| Shadow Chaser, kept Double Strafe one by one | 112.5 s |

The Stalker has no area skill of its own, so the limit is 1.5 times as
fast as the Shadow Chaser killing the five one by one with Triangle
Shot, about 88 s by its damage on one target. At 10% Fatal Menace was
1.9 times as fast as that; the mod ships it at 7%, where it is 1.28
times as fast. Its damage per target (0.37 of Triangle Shot at 10%) was
not measured again at 7%.

One result is not explained: Triangle Shot killed only two of the five
in 180 s, far fewer than its 2218 dmg/s on a single target predicts.

With the same stats, the skills hit the same at base level 100 and at
175.

- **Triangle Shot** is the main attack.
- **Fatal Menace** hits every target around the Shadow Chaser. A Stalker
  has nothing like it.
- **Feint Bomb** leaves a decoy that draws monsters off you, throws you
  back and blasts. It costs a Paint Brush and a Surface Paint. It was not
  measured at level 175.
- **Invisibility** lets you attack while hidden, but turns your attacks
  Ghost, so it is for Ghost-weak targets and escapes, not damage.
- The **Masquerades**, **Shadow Form**, **Strip Accessory**, **Body
  Painting** and the ground skills (**Man Hole**, **Dimension Door**,
  **Chaos Panic**, **Maelstrom**, **Bloody Lust**) are as in renewal.

Not measured at level 175: a dagger build, Feint Bomb, Auto Shadow
Spell.

### Equipment

Two tiers, a dagger and a bow each, for the Stalker and the Shadow
Chaser. Each raises Back Stab or Double Strafe for everyone, the same skill
further for a Stalker, and Fatal Menace or Triangle Shot for a Shadow
Chaser. Transcendent classes only.

| Item | Level | Drops from |
|---|---|---|
| Cutpurse's Stiletto | 70 | Ancient Mimic |
| Trickster's Bow | 70 | Raydric Archer |
| Nightshade Dirk | 90 | Nightmare Terror |
| Phantom Longbow | 90 | Banshee Master |

## Arch Bishop

### The path

A **High Priest at base level 99 and job level 70**, with no unspent
skill points, talks to the **Arch Bishop** beside the High Priest changer
in the Valkyrie's hall. The step cannot be undone, and you are asked to
confirm it.

The class's skill tree is renewal's Arch Bishop tree with the High
Priest's in it: it keeps every Novice, Acolyte, Priest and High Priest
skill it has learnt (Assumptio, Basilica, Meditatio and Mana Recharge
among them), and adds the Arch Bishop's own with the skill points of its
69 new job levels.

### From High Priest to Arch Bishop

- **It keeps** the guardian's skills: Assumptio halves the damage one
  person takes, Basilica shuts out attacks, Meditatio and Mana Recharge
  make its SP last.
- **It gains** the party leader's and the battle priest's: buffs for the
  whole party in one cast (Clementia: Blessing, Canto Candidus: Increase
  AGI, Praefatio: Kyrie Eleison, Expiatio, Sacrament), heals for the
  whole party (Coluceo Heal) and a big single heal (Highness Heal),
  Renovatio, Epiclesis, the Laudas, Silentium, Oratio, Clearance, and
  Holy magic (Adoramus, Judex) and Duple Light for fighting.

### How strong

**SP costs.** Renewal prices the Arch Bishop's own skills for renewal's
larger SP pools. This mod lowers those costs (the heal amounts and
durations are renewal's):

| | Renewal SP | Here |
|---|---|---|
| Clementia 3 | 360 | 256: what five Blessings cost a High Priest |
| Canto Candidus 3 | 240 | 192: five Increase AGIs |
| Praefatio 10 | 180 | 140: five Kyries |
| Highness Heal 5 | 190 | 80 |
| Coluceo Heal 3 | 240 | 110 |

Healing and SP upkeep were not part of the level-175 measurements.

**Damage.** Measured at base level 175 and job level 70 against a High
Priest at 99/70: every stat point spent, a test staff, no consumables. As
a caster, the Arch Bishop was measured on a plain dummy and a plain pack
of five, without the Abysmal Knight's defences the weapon classes hit.

A High Priest's only general attack is Holy Light, 610 to 636 dmg/s. The
Arch Bishop keeps it, and it grows with the character to 1130 to 1198
dmg/s at level 175 (1.78 to 1.96 times). The Arch Bishop has no
single-target skill of its own: Adoramus hits 7x7 cells and Judex 3x3.
So there is no 1.5 times target to meet here, and the two area skills
are set by how fast they clear a pack. The High Priest has no general
area skill, so the limit is 1.5 times as fast as the same Arch Bishop killing
the five one by one with Holy Light:

| At 175/70 | Per target | Pack of five | |
|---|---|---|---|
| Holy Light (kept) | 1130 dmg/s | 244.8 s, one by one | |
| Adoramus | 257 dmg/s, 0.23 of Holy Light | 174.6 s | 1.40 times as fast: within the limit |
| Judex | 289 dmg/s, 0.26 of Holy Light | 156.9 s | 1.56 times as fast: just over, within a tenth of the limit, and left |

The pack limit decides here, not the half rule: at 0.47 of Holy Light
per target, both skills cleared the pack about three times as fast as
Holy Light does. Adoramus also costs a Blue Gemstone.

Not measured at level 175: Duple Light, with either its magic strikes or
its melee strike. Whether the class should get a real single-target
attack is an open question.

### Equipment

Two tiers, a mace and a staff each, for the High Priest and the Arch
Bishop. Each mace raises damage against Undead and Demons for everyone, by
the same again for a High Priest, and Duple Light's melee strike for an
Arch Bishop; each staff raises MATK and healing for everyone, healing
again for a High Priest, and Adoramus for an Arch Bishop. Transcendent
classes only.

| Item | Level | Drops from |
|---|---|---|
| Censer Mace | 70 | Khalitzburg |
| Pilgrim's Rod | 70 | Evil Druid |
| Grand Censer | 90 | Dark Priest |
| Staff of Absolution | 90 | Necromancer |

## Rune Knight

### The path

A **Lord Knight at base level 99 and job level 70**, with no unspent
skill points, talks to the **Rune Knight** beside the Lord Knight changer
in the Valkyrie's hall. The step cannot be undone, and you are asked to
confirm it.

The class's skill tree is renewal's Rune Knight tree with the Lord
Knight's in it: it keeps every Novice, Swordman, Knight and Lord Knight
skill it has learnt (Spiral Pierce, Frenzy, Aura Blade, Concentration and
Parrying among them), and adds the Rune Knight's own with the skill
points of its 69 new job levels.

**The dragon.** Dragon Breath is cast from a dragon. Renewal's Dragon
Breeder is not on a pre-renewal server, and the Peco Peco Breeder gives a
Rune Knight a Peco Peco, so this mod adds a **Dragon Breeder** beside the
Knights' Peco Peco Breeder in Prontera (`prontera 55 353`). It is free,
and takes the dragon back when you talk to it again.

**Rune stones.** Rune Mastery cuts them from the materials pre-renewal
already has recipes for. Pre-renewal's rune items have no reuse delay;
the Raido (Crush Strike), Berkana (Millennium Shield) and Nauthiz
(Refresh) runes get renewal's back.

### From Lord Knight to Rune Knight

- **It keeps** the duellist's skills: Bowling Bash, Spiral Pierce,
  Frenzy, Aura Blade, Concentration, Parrying.
- **It gains** the dragon rider's: Sonic Wave and Hundred Spear for one
  target, Dragon Breath, Ignition Break and Wind Cutter for crowds, Death
  Bound, Dragon Howling, and the runes.

### How strong

Measured at base level 175 and job level 70 against a Lord Knight at
99/70: every stat point spent, a test weapon, no consumables, on a target
with an Abysmal Knight's defences. Each figure is the middle of three
runs.

The Lord Knight's reference is Bowling Bash, 3781 dmg/s (it hits a lone
target twice a cast); its Spiral Pierce does 1200. The Rune Knight keeps
Bowling Bash, which reaches 1.70 times that at level 175 through the
character's stats alone. A kept skill grows freely, so the Rune Knight's
own single-target skills are set just above it, at 1.76 times, and both
meet that:

| At 175/70 | dmg/s | Against Bowling Bash at 99/70 |
|---|---|---|
| Sonic Wave (own) | 6662 | 1.76 |
| Hundred Spear (own) | 6640 | 1.76 |
| Bowling Bash (kept) | 6427 | 1.70 |

Its own area skills stay far below the half rule:

| Area, per target | dmg/s | Of Sonic Wave |
|---|---|---|
| Wind Cutter | 1252 | 0.19 |
| Ignition Break | 762 | 0.11 |
| Dragon Breath | 287 | 0.04 |

A pack of five such targets: the Lord Knight clears it with Bowling Bash
in 15.2 s. The Rune Knight clears it with the Bowling Bash it keeps in
9.2 s, 1.65 times as fast; a kept skill grows freely and is not held to
the pack limit. Its own area skills are slower than the Lord Knight's
Bowling Bash: Wind Cutter 30.3 s, Ignition Break 48.3 s. Sonic Wave on
the five one by one takes 45.0 s.

With the same stats, Sonic Wave, Hundred Spear, Bowling Bash, Wind Cutter
and Ignition Break hit the same at base level 100 and at 175. Dragon
Breath does not (638 a hit and 1617): its formula no longer reads the
level, but it is built on HP and SP, which grow with the level.

- **Dragon Breath** is built on current HP and max SP, so it grows with
  the level's HP and SP tables and with VIT. It is scaled to 64%.
- **Giant Growth** (Thurisaz rune) gives STR +30, +250% on a Rune
  Knight's attacks and 2.5x damage on 30% of hits; renewal lets it run for
  15 minutes from one rune. Here it lasts **30 seconds and the rune can be
  used again after 3 minutes**: a burst like Enchant Deadly Poison, not a
  state.
- **Crush Strike** makes the next hit one heavy blow, once every 30
  seconds.
- **Storm Blast** (Wyrd rune) hits everything around the Rune Knight.
  Renewal lets a rune go every second; here **one rune every 10
  seconds**, a burst.
- The other runes (Millennium Shield, Stone Hard Skin, Fighting Spirit,
  Vitality Activation, Abundance, Refresh) are as in renewal.

Not measured at level 175: Enchant Blade, Giant Growth and the runes, and
the class right after the change, at job level 1.

### Equipment

Two tiers, a two-handed sword and a two-handed spear each, for the Lord
Knight and the Rune Knight. Each sword raises Bowling Bash for
everyone, again for a Lord Knight, and Sonic Wave for a Rune Knight; each
spear raises Brandish Spear for everyone, Spiral Pierce for a Lord Knight
and Hundred Spear for a Rune Knight. The spears are as heavy as a Lance,
for Spiral Pierce. The second tier cannot break, which Giant Growth would
otherwise risk. Transcendent classes only.

| Item | Level | Drops from |
|---|---|---|
| Runeblade | 70 | Raydric |
| Dragonfang Pike | 70 | Skeleton General |
| Rune Greatsword | 90 | Abysmal Knight |
| Wyrmguard Lance | 90 | Bloody Knight |

## Royal Guard

### The path

A **Paladin at base level 99 and job level 70**, with no unspent skill
points, talks to the **Royal Guard** beside the Paladin changer in the
Valkyrie's hall. The step cannot be undone, and you are asked to confirm
it.

The class's skill tree is renewal's Royal Guard tree with the Paladin's
in it: it keeps every Novice, Swordman, Crusader and Paladin skill it has
learnt (Rapid Smiting, Martyr's Reckoning, Gloria Domini and Battle Chant
among them), and adds the Royal Guard's own with the skill points of its
69 new job levels. A mounted Royal Guard rides a gryphon, from the
Crusaders' Peco Peco Breeder as before.

### From Paladin to Royal Guard

- **It keeps** the holy striker's and martyr's skills: Holy Cross, Grand
  Cross, Rapid Smiting, Martyr's Reckoning, Gloria Domini, Battle Chant.
- **It gains** the shield wall's: Banishing Point for one target, spear
  sweeps (Overbrand, Cannon Spear, Moon Slasher), shield blows (Shield
  Press, Earth Drive, Shield Spell), and protection (Reflect Damage,
  Prestige, King's Grace, Piety, Force of Vanguard). Inspiration is a
  large all-round buff that costs EXP, HP and SP. Banding, Ray of Genesis
  and Hesperus Lit want other Royal Guards beside it, as in renewal
  (Inspiration lets one cast Ray of Genesis alone).

### How strong

Measured at base level 175 and job level 70 against a Paladin at 99/70:
every stat point spent, a test spear and shield (Rapid Smiting and Shield
Press grow with the shield's weight), no consumables, on a target with an
Abysmal Knight's defences.

The Paladin's reference is Rapid Smiting, 1045 dmg/s. The Royal Guard
keeps it, and it reaches 1.70 times that at level 175 through the
character's stats alone. So the Royal Guard's own single-target skill is
set just above it: the target is 1.77 times (1.59 to 1.95), and it is
met.

| At 175/70 | dmg/s | Against Rapid Smiting at 99/70 |
|---|---|---|
| Banishing Point (own) | 1877 | 1.81 |
| Rapid Smiting (kept) | not recorded | 1.70 |

Overbrand, Earth Drive, Cannon Spear and Moon Slasher dealt 0.40 to 0.45
of Banishing Point to each target at first, inside the half rule, but
cleared a pack of five in 43.7 to 50.0 s against the Paladin's Grand
Cross at 87.0 s, far over the pack limit of 1.25 times as fast. They
were lowered by about a third, and Moon Slasher was given a factor of
its own. Timed again they take 76.7 s (Overbrand), 69.8 s (Earth Drive),
69.3 s (Moon Slasher) and 71.4 s (Cannon Spear): 1.13 to 1.26 times as
fast as the Paladin. Their damage per target was not measured again
after the change. Shield Press was not measured.

Banishing Point is scaled to 23% of renewal's ratio and Overbrand to 6%.
The defensive skills are as in renewal.

Hesperus Lit (three hits, castable every half second) was measured
later. In this server it hits one target only, so it is held like a
single-target skill: with renewal's ratio it dealt 17,783 dmg/s, 9.47
times Banishing Point; at 11% of the ratio 1800 dmg/s, 0.96 of it, so
Banishing Point stays the best. (At 12%: 1979 dmg/s, 1.05 times.)

### Equipment

Two tiers, a spear and a shield each, for the Paladin and the Royal
Guard. Each spear raises Holy Cross for everyone, again for
a Paladin, and Banishing Point for a Royal Guard; each shield raises
Shield Boomerang for everyone, Rapid Smiting for a Paladin and Shield
Press for a Royal Guard. The shields are heavy, since Rapid Smiting and
Shield Press grow with a shield's weight. Transcendent classes only.

| Item | Level | Drops from |
|---|---|---|
| Vanguard Spear | 70 | Zombie Master |
| Bulwark Shield | 70 | Ancient Mummy |
| Royal Partisan | 90 | Wraith Dead |
| Aegis of the Guard | 90 | Seyren Windsor |

## Warlock

### The path

A **High Wizard at base level 99 and job level 70**, with no unspent
skill points, talks to the **Warlock** beside the High Wizard changer in
the Valkyrie's hall. The step cannot be undone, and you are asked to
confirm it.

The class's skill tree is renewal's Warlock tree with the High Wizard's
in it: it keeps every Novice, Mage, Wizard and High Wizard skill it has
learnt (Mystical Amplification, Soul Drain, Gravitation Field and
Ganbantein among them), and adds the Warlock's own with the skill points
of its 69 new job levels.

### From High Wizard to Warlock

- **It keeps** the storm-caller's skills: the Wizard's spells, Mystical
  Amplification to make them greater, Soul Drain for SP, Gravitation
  Field and Ganbantein for bosses and sieges.
- **It gains** the elementalist's: spells of its own (Comet, Crimson
  Rock, Hell Inferno, Chain Lightning, Earth Strain, Tetra Vortex, Soul
  Expansion, Jack Frost, Frost Misty, Drain Life), control (White
  Imprison, Stasis, Marsh of Abyss, Sienna Execrate), and stored spells:
  elemental spheres and spellbooks that Release fires without a cast.

### Spellbooks

Reading Spellbook works renewal's way: use a **spellbook**, which reads it
(a 5 s cast), and the spell is stored; **Release** at level 1 casts it at
once. The books are sold by the **Spellbook Seller** in the Geffen magic
school (`geffen_in 175 112`), where renewal's Lea stands, at renewal's
prices: 100,000 zeny for Storm Gust, Lord of Vermilion and Meteor Storm,
500,000 for Drain Life, Jack Frost, Earth Strain, Crimson Rock and Chain
Lightning, 1,000,000 for Comet and Tetra Vortex. A book is not used up.
Pre-renewal has none of this (its own Reading Spellbook does nothing on
rAthena), so the books, the reading skill and the spellbook table come
from renewal.

### How strong

Measured at base level 175 and job level 70 against a High Wizard at
99/70: every stat point spent, a test staff, no consumables. As a
caster, the Warlock was measured on a plain dummy and a plain pack of
five, without the Abysmal Knight's defences the weapon classes hit.

The High Wizard's reference is Jupitel Thunder under Mystical
Amplification, 2788 dmg/s. The target for the Warlock's own
single-target spells is 1.5 times that, within a tenth (1.35 to 1.65),
and all four meet it:

| At 175/70 | dmg/s | Against amplified Jupitel Thunder at 99/70 |
|---|---|---|
| Hell Inferno (own) | 4236 | 1.52 |
| Soul Expansion (own) | 4113 | 1.48 |
| Chain Lightning on one target (own) | 3874 | 1.39 |
| Tetra Vortex (own) | 3856 | 1.38 |
| Jupitel Thunder (kept) | 3442 | 1.23 |

**Hell Inferno and Soul Expansion are single-target spells here.**
Renewal lets both splash, and with the splash they cleared a pack of
five in 11.3 s and 16.6 s; without it they take 59.0 s and 78.6 s.
Chain Lightning strikes at least four times, and on a lone target all
four land on it, so it is set as a single-target spell; in a pack its
strikes spread out.

Area is the Warlock's job, as it is the High Wizard's, so its area
spells are exempt from the half rule and held only by the pack limit:
at most 1.25 times as fast as the High Wizard, whose Meteor Storm clears
the pack in 31.4 s (Lord of Vermilion 48.4 s, Storm Gust 59.3 s).

| At 175/70 | Per target | Pack of five |
|---|---|---|
| Crimson Rock (own) | 1915 dmg/s | 24.5 s |
| Jack Frost (own) | 1992 dmg/s | 27.2 s |
| Frost Misty (own) | 1828 dmg/s | 32.7 s |
| Comet (own) | not recorded | 31.9 s |
| Chain Lightning (own) | | 32.1 s |
| Meteor Storm (kept) | 2303 dmg/s; 1.28 times the High Wizard's Meteor Storm | 24.4 s |
| Storm Gust (kept) | | 47.2 s |

The fastest of its own, Crimson Rock, is 1.28 times as fast as the High
Wizard's Meteor Storm, a little over the 1.25 limit, and was left. The
Meteor Storm it keeps is as fast.

- **SP.** At renewal's prices the Warlock's area spells ran a full SP
  bar dry three times faster than an amplified Meteor Storm, so their
  costs are lowered: Crimson Rock costs 42 SP at level 5, Jack Frost 39,
  Frost Misty 47, Soul Expansion 28, Hell Inferno 49, Chain Lightning 60.
  How long a bar lasts was not measured at level 175.
- **Comet** keeps pre-renewal's cost of **2 Red Gemstones** (an import
  entry cannot take an item cost away), with renewal's 20 second cooldown.

Not measured at level 175: Earth Strain, Drain Life, and spells fired
from spheres or spellbooks with Release.

### Equipment

Two tiers, a staff and a two-handed staff each, for the High Wizard and
the Warlock. Each staff raises Jupitel Thunder for everyone, again
for a High Wizard, and Chain Lightning for a Warlock; each two-handed
staff raises Lord of Vermilion for everyone, again for a High Wizard, and
Crimson Rock for a Warlock. All give MATK +15%. Transcendent classes only.

| Item | Level | Drops from |
|---|---|---|
| Elemental Rod | 70 | Elder |
| Ember Staff | 70 | Incubus |
| Arcane Conduit | 90 | Succubus |
| Staff of Starfall | 90 | Kathryne Keyron |

## Sura

### The path

A **Champion at base level 99 and job level 70**, with no unspent skill
points, talks to the **Sura** beside the Champion changer in the
Valkyrie's hall. The step cannot be undone, and you are asked to confirm
it.

The class's skill tree is renewal's Sura tree with the Champion's in it:
it keeps every Novice, Acolyte, Monk and Champion skill it has learnt
(Asura Strike, Zen, Raging Palm Strike, Glacier Fist and Chain Crush
Combo among them), and adds the Sura's own with the skill points of its
69 new job levels.

### From Champion to Sura

- **It keeps** the one blow: Zen fills its spheres at once, the combos
  run into Asura Strike, and Occult Impaction is its steady attack.
- **It gains** the endless chain: Dragon Combo, Knuckle Arrow and Tiger
  Cannon for steady damage, Gates of Hell as a second burst, sweeping
  blows (Sky Net Blow, Earth Shaker, Rampage Blast, Lightning Ride) for
  crowds, Raising Dragon for more spheres, and Gentle Touch to heal,
  steal SP or change its stats.

### How strong

Measured at base level 175 and job level 70 against a Champion at 99/70:
every stat point spent, a test knuckle, no consumables, on a target with
an Abysmal Knight's defences.

The Champion's reference is Occult Impaction under Zen, 2341 dmg/s. The
Sura keeps it, and it reaches 2.04 times that at level 175 through the
character's stats alone. So the Sura's own single-target skills are set
just above it: the target is 2.12 times (1.91 to 2.33).

| At 175/70 | dmg/s | Against Occult Impaction at 99/70 | |
|---|---|---|---|
| Knuckle Arrow (own) | 5092 | 2.20 | met |
| Dragon Combo (own) | 5294 | 2.28 | met |
| Tiger Cannon after Raising Dragon (own) | about 4730 | 2.04 | met |
| Occult Impaction under Zen (kept) | not recorded | 2.04 | |

**Tiger Cannon needs a large factor.** It spends HP and SP, and the
part of its damage built on them does not follow a factor: 668% of
renewal's ratio gave 1.76 times, 802% gives 2.04. Its cooldown is 7 s
instead of renewal's 3.

Earth Shaker, Sky Net Blow and Lightning Ride deal 326 to 455 dmg/s to
each target, 0.06 to 0.09 of the single-target damage, far inside the
half rule. Rampage Blast and Howling of Lion (10 s cooldown each) were as
low, and on a pack of five they were slower than Knuckle Arrow one by one
(72.2 s and 86.4 s against 41.1 s). At 250% of renewal's ratio they clear
it in 32.1 s and 33.7 s, 1.28 and 1.22 times as fast, at 0.22 and 0.20 of
the single-target damage a target. (Rampage Blast at 280% jumps to 22.0 s.)

Asura Strike is a burst built on SP and HP; it grows with the
character and is not held to a target. Gates of Hell, which renewal has
without a cooldown, has one of 10 s here. Cast whenever it is ready, it
dealt 1235 dmg/s with renewal's ratio, 0.53 times Occult Impaction; as
with Tiger Cannon, its HP and SP part does not follow a factor, and at
500% of renewal's ratio it deals 4556 dmg/s, 2.06 times: met.

A pack of five such targets: the Champion, with Occult Impaction under
Zen on one after another, takes 138.0 s. The Sura takes 37.2 s with
Dragon Combo and 41.1 s with Knuckle Arrow, 3.7 times as fast, although
it is only 2.2 times as strong on one target. The difference is not
explained: the Champion dealt 1309 dmg/s in the pack against 2341 on the
single target. The Sura was not tuned on the pack figure.

### Equipment

Two tiers, two knuckles each, for the Champion and the Sura.
Each raises a Sura skill and a Champion skill (Knuckle Arrow and Occult
Impaction, Dragon Combo and Chain Crush Combo, and so on). Transcendent
classes only.

| Item | Level | Drops from |
|---|---|---|
| Rakshasa Claw | 70 | Owl Baron |
| Iron Mantra Knuckle | 70 | Owl Duke |
| Asura Fang | 90 | Tao Gunka |
| Vajra Knuckle | 90 | Eddga |
## Ranger

### The path

A **Sniper at base level 99 and job level 70**, with no unspent skill
points, talks to the **Ranger** beside the Sniper changer in the
Valkyrie's hall. The step cannot be undone, and you are asked to confirm
it. You are given a **Wolf's Flute**: Warg Mastery needs one held, as in
renewal. Lost it? The Ranger gives another.

The class's skill tree is renewal's Ranger tree with the Sniper's in it:
it keeps every Novice, Archer, Hunter and Sniper skill it has learnt
(Falcon Assault, Sharp Shooting, True Sight and Wind Walk among them)
and its falcon, and adds the Ranger's own with the skill points of its
69 new job levels. The warg will not come while a falcon is out.

Its traps take renewal's **Special Alloy Trap**, which no pre-renewal
shop sells: the **Trap Seller** beside Payon's Tool Dealer
(`payon_in01 7 49`) does, with the plain Trap.

### From Sniper to Ranger

- **It keeps** bow and falcon at long range: Double Strafe, Arrow
  Shower, Falcon Assault, Sharp Shooting, True Sight, Wind Walk.
- **It gains** the wild: Aimed Bolt and Arrow Storm, a warg to fight
  with (Warg Strike, Warg Bite) and to ride, renewal's traps of fire, ice
  and steel, Camouflage, and Unlimit as a short burst window.

### How strong

Measured at base level 175 and job level 70 against a Sniper at 99/70:
every stat point spent, a test bow, no consumables, on a target with an
Abysmal Knight's defences.

The Sniper's reference is Double Strafe, 1588 dmg/s. The Ranger keeps
it, and it reaches 1.52 times that at level 175 through the character's
stats alone. So the Ranger's own single-target skills are set just above
it: the target is 1.58 times, and both meet it.

| At 175/70 | dmg/s | Against Double Strafe at 99/70 |
|---|---|---|
| Aimed Bolt (own) | 2576 | 1.62 |
| Warg Strike (own) | 2519 | 1.59 |
| Double Strafe (kept) | not recorded | 1.52 |

A pack of five such targets: the Sniper clears it with Arrow Shower in
79.7 s (with Double Strafe one by one, 117.3 s). The Ranger's Arrow Storm
was timed at three settings of renewal's ratio:

| Arrow Storm at | Per target | Pack of five | Against the Sniper's Arrow Shower |
|---|---|---|---|
| 65% | 863 dmg/s, 0.34 of the single-target damage | 46.7 s | 1.71 times as fast |
| 60% | not recorded | 50.4 s | 1.58 times as fast |
| 47% | not recorded | 65.2 s | 1.22 times as fast |

The Sniper has a real area skill, so the limit is 1.25 times as fast,
and the mod ships Arrow Storm at 47%. The Arrow Shower a Ranger keeps
clears the same pack in 52.0 s at 175: kept skills grow with the
character, so on a pack the kept skill is now the faster of the two. One by one, the
Ranger takes 78.4 s with the Double Strafe it keeps and 81.6 s with Aimed
Bolt.

- **Traps** do most of their damage from DEX and INT, outside what a
  factor reaches: Cluster Bomb's weapon part is scaled to 70%, Firing
  Trap's to 8%. Firing Trap still did 0.60 of Aimed
  Bolt to each target, so Firing Trap and Icebound Trap have a 1 s
  cooldown here, which brings it to 0.40. Icebound Trap deals 423 to
  each target, 0.16 of Aimed Bolt, but each burst hits a whole pack:
  at a 1 s cooldown it cleared five in 45.6 s, 1.75 times the Sniper's
  Arrow Shower. Its cooldown is 3 s: 68.6 s, 1.16 times, about Arrow
  Storm's 65.3 s. **Cluster Bomb is not
  settled**: the test landed the trap in one run of six (0.41 then).
- **Unlimit** more than triples ranged damage while it lasts, and
  renewal kept it up for 150 s of every 300; here it lasts 30 s, a burst
  window. The figures above are without it.

### Equipment

Two tiers, two bows each, for the Sniper and the Ranger.
Each raises a Ranger skill and a Sniper skill (Aimed Bolt and Double
Strafe, Warg Strike and Falcon Assault, and so on). Transcendent classes
only.

| Item | Level | Drops from |
|---|---|---|
| Warden Bow | 70 | Ancient Worm |
| Pack Leader Bow | 70 | Mini Demon |
| Wildheart Longbow | 90 | Atroce |
| Garm Fang Bow | 90 | Garm |
## Minstrel and Wanderer

### The path

A **Clown or Gypsy at base level 99 and job level 70**, with no unspent
skill points, talks to the **Wandering Minstrel** beside the Clown
changer, or the **Wanderer** beside the Gypsy changer, in the Valkyrie's
hall. (rAthena's own Clown changer is called "Minstrel", the class's
Korean name; the new one is the *Wandering* Minstrel.) The step cannot
be undone, and you are asked to confirm it.

Each class's tree is renewal's with the Clown's or Gypsy's in it: it
keeps every Novice, Archer, Bard or Dancer and Clown or Gypsy skill it
has learnt (Musical Strike, Slinging Arrow, the old songs and ensembles,
Arrow Vulcan, Tarot Card of Fate, Marionette Control and Longing for
Freedom), and adds the shared Minstrel/Wanderer skills and its own with
the skill points of its 69 new job levels.

Great Echo takes **Protect Neck Candy** and the sorrowful songs
**Regrettable Tears**, which no pre-renewal shop sells: renewal's candy
seller **Harive** is added where renewal has her (`comodo 196 162`).

### From Clown or Gypsy to Minstrel or Wanderer

- **It keeps** the old performer's skills: the Bard's and Dancer's songs
  and ensembles, Musical Strike or Slinging Arrow, Arrow Vulcan, Tarot
  Card of Fate, Marionette Control, Longing for Freedom.
- **It gains** the party performer's: renewal's songs and dances, alone
  (Echo Song, Swing Dance, ...) or as a duet, three-minute buffs and
  debuffs for the party; and damage when the song must hurt:
  Reverberation and Metallic Sound (magic) on one target, Severe
  Rainstorm and Great Echo over an area.

### How strong

Measured at base level 175 and job level 70 against a Clown or Gypsy at
99/70: every stat point spent, a test instrument or whip, no
consumables, on a target with an Abysmal Knight's defences.

The reference is the arrow skill both keep: the Clown's Musical Strike
and the Gypsy's Slinging Arrow. Neither grows past 1.5 times with the
character, so the target for the new single-target skills is 1.5 times
the reference, within a tenth (1.35 to 1.65), and it is met:

| | Minstrel | Wanderer |
|---|---|---|
| Reference at 99/70 | Musical Strike, 1032 dmg/s | Slinging Arrow with a whip, 928 dmg/s |
| The same skill, kept, at 175/70 | 1.19 times | 1.16 times |
| Reverberation (own) | 1452 dmg/s, 1.41 times | 1305 dmg/s, 1.41 times |
| Metallic Sound (own) | 1502 dmg/s, 1.45 times | not recorded |

A pack of five such targets. The area skills are compared with the same
character killing the five one by one, and may be at most 1.5 times as
fast. One by one takes the Minstrel about 127 s (calculated from the
single-target damage, not run):

| Pack of five | Minstrel | Wanderer |
|---|---|---|
| Great Echo | 99.1 s | 110.6 s |
| Severe Rainstorm | 104.7 s | 105.0 s |

For the Minstrel that is at most 1.28 times as fast, inside the limit.
The Wanderer's time one by one was not recorded, nor what the two area
skills deal to each target. Great Echo costs two
Protect Neck Candy a cast.

### Equipment

Two tiers, an instrument (Bards: Clown or Minstrel) and a whip (Dancers:
Gypsy or Wanderer) each. Each raises Reverberation and a Minstrel or
Wanderer skill, and Musical Strike or Slinging Arrow and Arrow Vulcan.
## Genetic

### The path

A **Creator at base level 99 and job level 70**, with no unspent skill
points, talks to the **Genetic** beside the Creator changer in the
Valkyrie's hall. The step cannot be undone, and you are asked to confirm
it.

The class's skill tree is renewal's Genetic tree with the Creator's in
it: it keeps every Novice, Merchant, Alchemist and Creator skill it has
learnt (Acid Demonstration, Full Chemical Protection, Plant Cultivation
and Slim Potion Pitcher among them) and its homunculus, and adds the
Genetic's own with the skill points of its 69 new job levels. Its cart
skills need a pushcart, from the Kafra as for any Merchant.

Pre-renewal sells nothing a Genetic's new skills consume, so two of
renewal's shops are added where renewal has them:
- the **Black Marketeer** in Einbroch (`einbroch 122 250`): cannonballs
  for Cart Cannon (and Magic Gear Fuel and Madogear parts);
- the **Genetic Bookseller** in the Alchemist guild (`alde_alche 40 184`,
  beside the Material Seller): renewal's craft books, 100,000 zeny each,
  for the bombs, plant seeds and spores (Spore Explosion, Crazy Weed),
  superior potions and cooking.

### From Creator to Genetic

- **It keeps** the flask: Acid Terror, and Acid Demonstration at a Fire
  Bottle and an Acid Bottle a throw, with Full Chemical Protection, Slim
  Potion Pitcher and the homunculus.
- **It gains** the cart and the garden: Cart Cannon (cannonballs) and
  Cart Tornado, man-eating plants (Crazy Weed, Hell's Plant, Thorn Trap,
  Blood Sucker), Spore Explosion and Demonic Fire, and renewal's potions
  and bombs from Special Pharmacy and Mix Cooking. Of renewal's Special
  Pharmacy recipes, the herb activators, the concentrated syrups and
  Golden X are not in pre-renewal's tables; the other 99 are.

### How strong

Measured at base level 175 and job level 70 against a Creator at 99/70:
every stat point spent, a test axe, a full cart (cart skills grow with
its weight), on a target with an Abysmal Knight's defences.

The Genetic has no single-target skill of its own. Cart Cannon splashes
over 7x7 cells, so it counts as an area skill. Its single-target damage
is what it keeps from the Creator, and that grows freely with the
character:

| At 175/70 | dmg/s | Against the Creator at 99/70 |
|---|---|---|
| Acid Terror (kept) | 2820 | 2.17 times the Creator's 1302 |
| Cart Cannon, Cart Tornado, Spore Explosion, Crazy Weed, per target | not recorded | 0.16 to 0.23 of the Genetic's Acid Terror |

The area skills are far inside the half rule, and their factors were
left as they were. No pack of five was timed for the Genetic.

**Acid Demonstration was not measured.** It is the Creator's real
weapon, and the Genetic keeps it, but its damage follows the target's
VIT and it spends two bottles a throw, so Acid Terror was taken as the
reference instead.

Hell's Plant and the traps only act on a monster that moves or attacks,
and are as in renewal.

### Equipment

Two tiers, two axes each, for the Creator and the Genetic.
Each raises Genetic skills, Acid Terror and Acid Demonstration.
Transcendent classes only.

| Item | Level | Drops from |
|---|---|---|
| Serenade Lute | 70 | Alice |
| Gypsy Lash | 70 | Headless Mule |
| Siren's Harp | 90 | Lady Tanee |
| Moonlit Whip | 90 | Mistress |
| Greenhouse Axe | 70 | Geographer |
| Cart Breaker | 70 | High Orc |
| Philosopher's Edge | 90 | Falling Bishop |
| Chimera Splitter | 90 | Dark Lord |
## Mechanic

### The path

A **Whitesmith at base level 99 and job level 70**, with no unspent
skill points, talks to the **Mechanic** beside the Whitesmith changer in
the Valkyrie's hall. The step cannot be undone, and you are asked to
confirm it.

The class's skill tree is renewal's Mechanic tree with the Whitesmith's
in it: it keeps every Novice, Merchant, Blacksmith and Whitesmith skill
it has learnt (the forge, Cart Termination, Meltdown, Maximum
Power-Thrust and Upgrade Weapon among them), and adds the Mechanic's own
with the skill points of its 69 new job levels.

Most of its skills need a **Madogear**. Pre-renewal has no one who gives
one, so two NPCs are added in Einbroch, where renewal has its Black
Marketeer:
- the **Mado Engineer** (`einbroch 124 250`) puts a Mechanic who has
  learnt Madogear License into a Madogear, or takes it back;
- the **Black Marketeer** beside him (`einbroch 122 250`) sells Magic
  Gear Fuel, which the Madogear's skills burn, cannonballs for Arms
  Cannon, Vulcan Bullets and the Madogear's parts and repair kits.

### From Whitesmith to Mechanic

- **It keeps** the cart and the forge: Mammonite, Cart Termination with
  a laden cart, Meltdown, Maximum Power-Thrust, Upgrade Weapon.
- **It gains** the machine: in the Madogear it swings axes (Power
  Swing, Axe Tornado, Axe Boomerang), punches (Boost Knuckle, Pile
  Bunker), fires (Vulcan Arm, Arms Cannon, Flame Launcher, Cold Slower),
  shields itself and its party (Neutral Barrier, Stealth Field), and
  builds turrets (Silver Sniper, Magic Decoy). Everything it fires costs
  fuel.

### How strong

Measured at base level 175 and job level 70 against a Whitesmith at
99/70: every stat point spent, a test axe, a full cart (Cart Termination
grows with the cart's weight), no consumables beyond the fuel and
ammunition the skills need, on a target with an Abysmal Knight's
defences.

The Whitesmith's reference is Cart Termination, 3816 dmg/s. The Mechanic
keeps it, and it reaches 1.79 times that at level 175 through the
character's stats alone. So the target for the Mechanic's own
single-target skills is just above it, 1.86 times (1.67 to 2.05), and
all three meet it. Only the ratios were recorded:

| At 175/70 | Against Cart Termination at 99/70 |
|---|---|
| Power Swing (own) | 1.85 |
| Boost Knuckle (own) | 1.87 |
| Vulcan Arm (own) | 1.86 |
| Cart Termination (kept) | 1.79 |
| Area skills, per target | 0.06 to 0.24 of the single-target damage |

A pack of five such targets: the Mechanic clears it with Axe Tornado in
31.8 s and with Arms Cannon (it splashes over 5x5 cells) in 34.3 s. The
Whitesmith's time is about 51 s, calculated from its 3816 dmg/s, because
its pack run had no loaded cart. That makes the Mechanic about 1.6 times
as fast. Single-target skills such as Power Swing do not finish the pack
within a run's 180 s.

**Magma Eruption** was measured later. Its lava is fixed damage (2 x 1800
a tick at level 5), which no factor reaches. With renewal's tick of half
a second one cast's lava killed a whole pack by itself: 6.9 s for five,
at a 6, 12 or 14 s cooldown alike, 3.7 to 7.4 times the Whitesmith and
Power Swing one by one. Here the lava ticks every second and the
cooldown is 12 s at every level: the pack in 18.8 s, 1.36 times Power
Swing one by one, and 0.28 of Power Swing on one target.

With the same stats, the skills hit the same at base level 100 and at
175.

### Equipment

Two tiers, two two-handed axes each, for the Whitesmith and the
Mechanic. Each raises Mechanic skills, Cart Termination and
Mammonite. Transcendent classes only.

| Item | Level | Drops from |
|---|---|---|
| Piston Axe | 70 | Explosion |
| Boiler Axe | 70 | Magmaring |
| Drill Breaker | 90 | Maya |
| Dragon Forge Axe | 90 | Detale |
## Sorcerer

### The path

A **Professor at base level 99 and job level 70**, with no unspent skill
points, talks to the **Sorcerer** beside the Professor changer in the
Valkyrie's hall. The step cannot be undone, and you are asked to confirm
it.

The class's skill tree is renewal's Sorcerer tree with the Professor's
in it: it keeps every Novice, Mage, Sage and Professor skill it has
learnt (Soul Change, Spider Web, Double Casting and Memorize among
them), and adds the Sorcerer's own with the skill points of its 69 new
job levels.

Its **elemental spirits** (Agni, Aqua, Ventus, Tera, three sizes each)
come from renewal's elemental table, which pre-renewal does not load;
the mod brings it, without the fourth class's spirits. A summon costs
the classic elemental stones (Red Blood and a Flame Heart, Crystal Blue
and Mystic Frozen, Wind of Verdure and Rough Wind, Yellow Live and Great
Nature), which monsters drop as before.

**A spirit fights beside the Sorcerer but does not strengthen it.** In
renewal a spirit's passive and assist skills put a status on its master
(more damage for the matching spells among them). Pre-renewal's skill
table gives those skills no status, and the mod does not bring them:
measured, they would make Diamond Dust 31%, Earth Grave 13% and Varetyr
Spear 42% stronger, past the limits, and a lower factor to make up for
it would leave the spells weak without a spirit. So the spirits attack,
take hits and use their own skills, and the Sorcerer's numbers are the
same with and without one.

### From Professor to Sorcerer

- **It keeps** magic bent to its will: the bolts under Double Casting,
  Heaven's Drive, Soul Change, Spider Web, Memorize.
- **It gains** the elements and their spirits: Varetyr Spear, Psychic
  Wave, Diamond Dust, Earth Grave, Poison Buster and Cloud Kill, the
  four elemental insignias, and Spell Fist, which holds a bolt in the
  fist and lets every blow after it strike with the bolt.

### How strong

Measured at base level 175 and job level 70 against a Professor at
99/70: every stat point spent, a test staff, no consumables. As a
caster, the Sorcerer was measured on a plain dummy and a plain pack of
five, without the Abysmal Knight's defences the weapon classes hit.

The Professor's reference is Fire Bolt under Double Casting. Single
readings scatter widely (about 1200 to 2150 dmg/s); three runs of the
spec on the current build gave 1688, 1793 and 1836, about 1770. The
target for the Sorcerer's own single-target spell is 1.5 times that,
within a tenth (1.35 to 1.65), and it is met:

| At 175/70 | dmg/s | Against Fire Bolt at 99/70 |
|---|---|---|
| Varetyr Spear (own) | 2694 to 2785 | 1.5 to 1.6 |
| Fire Bolt under Double Casting (kept) | 2414 | 1.36 |

(Varetyr Spear first read 3188 to 3233 at 116% of renewal's ratio and
was lowered to 98%. The Sorcerer's base INT above 99 counts for a
third, as for every class here.)

**Varetyr Spear is a single-target spell here.** Renewal lets it splash
over 9x9 cells, and with the splash it cleared a pack of five in 10.2 s;
without it, 73.2 s.

The Professor has a real area spell, Heaven's Drive, which clears the
pack in 36.6 s (813 dmg/s to each target). So the Sorcerer's area spells
may deal at most about half of Varetyr Spear to each target and clear
the pack at most 1.25 times as fast, so in no less than 29.3 s:

| At 175/70 | Per target | Of Varetyr Spear | Pack of five | Against Heaven's Drive |
|---|---|---|---|---|
| Psychic Wave (own) | 1074 dmg/s | 0.39 | 39.1 s | 0.94 |
| Poison Buster (own) | 1323 dmg/s | 0.48 | 33.4 s | 1.10 |
| Cloud Kill (own) | 1062 dmg/s | 0.39 | 36.0 s | 1.02 |

All three are within both limits; Poison Buster is the closest.
(An earlier timing of Heaven's Drive, 45.2 s, made Poison Buster look
1.27 times as fast. Timed again on the same build it is 1.10.)

With the same stats, Varetyr Spear's three hits read about 12% lower at
base level 175 than at 100; it does not grow with the level.

- **Spell Fist** makes every auto-attack a full bolt in renewal, for
  20 SP a hit. On an AGI and INT build that was 2.4 times the
  Professor's Fire Bolt, so the bolt is scaled to 17% for a Sorcerer
  under Spell Fist only (a Wizard's bolts and a Sorcerer's own are
  untouched): 2756 dmg/s, beside Varetyr Spear's 2809, both about 1.5
  times. An INT-only build gets almost nothing from it.
- **Earth Grave and Diamond Dust** grow with Seismic and Frost Weapon
  and INT. With renewal's ratio they dealt 1.03 and 0.94 of Varetyr
  Spear to each target; at 44% and 48% of it, 1258 and 1406 dmg/s, 0.44
  and 0.49. On the pack they take 31.5 s and 32.2 s, 1.16 and 1.14 times
  Heaven's Drive.
- Pre-renewal's **Cloud Kill** costs **2 Red Gemstones**, and keeps them
  (an import entry cannot take an item cost away).

### Equipment

Two tiers, two books each, for the Professor and the Sorcerer.
Each raises Sorcerer spells and Sage ones (bolts, Earth Spike, Heaven's
Drive). Transcendent classes only.

| Item | Level | Drops from |
|---|---|---|
| Grimoire of Spirits | 70 | Rideword |
| Codex of Elements | 70 | Deathword |
| Tome of Varetyr | 90 | Ktullanux |
| Shell of the Sage | 90 | Turtle General |

## Files

| | |
|---|---|
| `npc/guillotine_cross.txt` | the Guillotine Cross changer |
| `npc/shadow_chaser.txt` | the Shadow Chaser changer |
| `npc/arch_bishop.txt` | the Arch Bishop changer |
| `npc/rune_knight.txt` | the Rune Knight changer |
| `npc/dragon_breeder.txt` | the Dragon Breeder in Prontera |
| `npc/royal_guard.txt` | the Royal Guard changer |
| `npc/warlock.txt` | the Warlock changer |
| `npc/spellbook_seller.txt` | the Spellbook Seller in Geffen |
| `npc/sura.txt` | the Sura changer |
| `npc/ranger.txt` | the Ranger changer |
| `npc/trap_seller.txt` | the Trap Seller in Payon |
| `npc/minstrel.txt`, `npc/wanderer.txt` | the Minstrel and Wanderer changers |
| `npc/candy_seller.txt` | Harive, the candy seller in Comodo |
| `npc/genetic.txt` | the Genetic changer |
| `npc/genetic_books.txt` | the Genetic Bookseller in the Alchemist guild |
| `npc/black_marketeer.txt` | the Black Marketeer in Einbroch (cannonballs, Magic Gear Fuel) |
| `npc/mechanic.txt` | the Mechanic changer |
| `npc/mado_engineer.txt` | the Mado Engineer in Einbroch |
| `npc/black_marketeer.txt` | the Black Marketeer in Einbroch (Magic Gear Fuel, cannonballs) |
| `npc/sorcerer.txt` | the Sorcerer changer |
| `db/elemental_db.yml` | renewal's elemental spirits, without the fourth class's |
| `db/spellbook_db.yml` | renewal's spellbooks |
| `lua/third_classes.lua` | the third classes' skill damage scaling |
| `npc/kagerou_oboro.txt` | Kirikage and the Shadow Supplier |
| `lua/kagerou_oboro.lua` | the skill damage scaling |
| `npc/rebellion.txt` | Old Hand Jesse and the Gunsmith |
| `lua/rebellion.lua` | the skill damage scaling, with the measured table |
| `npc/star_emperor.txt` | Master Haneul |
| `lua/star_emperor.lua` | the skill damage scaling, with the measured table |
| `npc/soul_reaper.txt` | Shaman Seol |
| `lua/soul_reaper.lua` | the skill damage scaling, with the measured table |
| `npc/super_novice.txt` | Old Novice Nodor |
| `lua/super_novice.lua` | the factors for the second-class skills an Expanded Super Novice gains |
| `db/job_stats.yml` | HP, SP, EXP, bonuses, ASPD, weight |
| `db/skill_tree.yml` | renewal's trees, under the third classes |
| `db/skill_db.yml` | renewal's entries for the third-class skills, with the fixed cast times turned into delay, the Arch Bishop's lower SP costs, and the Auto Shadow Spell flag on four more spells |
| `db/item_db.yml` | the equipment, the rune stones' reuse delays, and renewal's spellbooks |
| `db/item_combos.yml` | the set bonuses (none yet) |
| `db/mob_db.yml` | the equipment's drops |
| `System/itemInfo.lua` | the equipment's names and descriptions |

Everything under `db/` and `System/` is generated by
`tools/transcendent-third-classes/build.py`, run by the shared
`tools/expanded_class/expanded_class.py`, from the pinned rAthena
and each class's three CSV files, in its own directory beside it
(`guillotine_cross/`, `shadow_chaser/`, `arch_bishop/`, `rune_knight/`,
`royal_guard/`, `warlock/`, `sura/`, `ranger/`, `minstrel/`, `wanderer/`,
`genetic/`, `mechanic/`, `sorcerer/`, `kagerou_oboro/`, `rebellion/`,
`star_emperor/`, `soul_reaper/`, `super_novice/`; the last five build expanded-classes):

```
python3 tools/transcendent-third-classes/build.py --rathena ../rathena
python3 tools/transcendent-third-classes/build.py --rathena ../rathena --check
```

The damage figures above come from the runs in
`tools/transcendent-third-classes/balance.json` (the third
classes) and `balance-<class>.json` beside it (the expanded classes); to
measure them again, see `tools/expanded_class/balance/README.md`:

```
python3 tools/expanded_class/balance/run_specs.py tools/transcendent-third-classes/balance.json
python3 tools/expanded_class/balance/run_specs.py tools/transcendent-third-classes/balance-kagerou-oboro.json
```

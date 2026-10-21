# expanded-classes

Renewal's **expanded advancements** in pre-renewal: each the next step of
its finished base class, which keeps every skill it has, levels to **175**
and job level 70.

| Advancement | Advances from | At | Where |
|---|---|---|---|
| Kagerou (male), Oboro (female) | Ninja | 99 / job 70 | Kirikage, Ninja guild (`que_ng 33 62`) |
| Rebellion | Gunslinger | 99 / job 70 | Old Hand Jesse, Gunslinger guild (`que_ng 156 167`) |
| Star Emperor | Star Gladiator | 99 / job 50 | Master Haneul, Payon (`payon 160 141`) |
| Soul Reaper | Soul Linker | 99 / job 50 | Shaman Seol, Payon (`payon 154 141`) |
| Expanded Super Novice | Super Novice | 99 / job 99 | Old Novice Nodor, Aldebaran (`aldeba_in 220 167`) |

Needs **level175-core** (the soft cap for base stats above 99, and the rule
that keeps base level out of skill damage). The third classes are their
own mod, **transcendent-third-classes**; the two work side by side.

### Level 175

Above 99 a base stat counts for a third and base DEX gives no cast speed
(level175-core). Experience as for the third classes: 99 to 100 costs what
a transcendent class's 98 to 99 costs, rising evenly to twice that at 174
to 175.

### Skill descriptions

Pre-renewal's English translation has no description for these classes'
skills. The mod ships them (`data/luafiles514/lua files/skillinfoz/skilldescript.lub`,
88 entries) with this game's numbers, in the translation's colours plus
bold and italic; the app merges them into the client's table by skill.

### Area damage

Renewal gave almost every third class area attacks it could spam, and
levelling became gathering a crowd and pressing one button. In
pre-renewal area damage belongs to a few classes. So here a **fighting
third class deals at most about half its best single-target damage to
each target of an area**: an area attack pays from about three targets,
and against one or two its single-target skills stay better. The casters
whose job area damage is (the Warlock, like the High Wizard; the Soul
Reaper; a magical Kagerou or Oboro) are exempt.

## Kagerou and Oboro

Kagerou and Oboro in pre-renewal, as the next step of a finished Ninja.

rAthena's server already knows both classes in a pre-renewal build: the job
ids, dual-wielding, the charms and every KO/OB skill are compiled in. What
pre-renewal lacks is the data: no HP, SP, EXP, ASPD or job-bonus tables for
them, no skill tree, item tables that let no Kagerou equip anything, skill
entries from an older revision, and no way to become one. This mod supplies
all of it, and changes nothing in rAthena or the app.

### The path

Talk to **Kirikage** in the Ninja guild (`que_ng`, beside Kuuga Gai) as a
**Ninja at base level 99 and job level 70**, with no unspent skill
points. There is no rebirth: the Ninja becomes a **Kagerou** (male) or
an **Oboro** (female) on the spot, keeps every Ninja skill, and its base
level goes on to 175. The step cannot be undone, and you are asked to
confirm it.

Kagerou and Oboro start again at job level 1 and go to 60. That gives 59
skill points on top of the Novice's 9 and the Ninja's 69, **137** in
all, ten below renewal's 147 (renewal's Kagerou goes to job 70).

### How strong

The aim is about 1.5 times a Ninja at level 99 on one target, or just
above a kept Ninja skill that grows past that; for a fighter, at most
half of that on each target of an area (see *Area damage* above):

- **HP**: the Assassin's table times 1.1. An Assassin Cross gets it times 1.25.
- **SP**: the Ninja's table times 1.1.
- **Job bonuses**: renewal's Kagerou bonuses to job 50, then five more, for
  +40 in all. A transcendent class gets +45.
- **EXP**: the transcendent base table to 99, and from there as under
  *Level 175 and the soft cap* above.
- **ASPD**: the Ninja's, with a quicker Huuma Shuriken (700 against 750).
- **Cast times**: pre-renewal has no fixed cast time, and DEX shortens every
  cast to nothing at 150. Of the Kagerou/Oboro skills, only Distorted
  Crescent and Ominous Moonlight had one in renewal (2 s); both have 30 s
  cooldowns, so the whole 2 s is added to their cast time, which DEX and
  Izayoi reduce, as renewal's fixed-cast reductions did.
- **Skill damage**: scaled in `lua/kagerou_oboro.lua`, and Kunai Splash
  slowed in `db/skill_db.yml`, then measured at base level 175 against a
  Ninja at level 99: every stat point spent, a test weapon, no
  consumables. The physical skills were measured on a target with an
  Abysmal Knight's defences, the spells on a plain dummy and a plain
  pack of five.

The Ninja's references at level 99: Throw Huuma Shuriken 321 dmg/s,
Throw Kunai 251, Ice Spear 2140, Kamaitachi 1921 and Exploding Dragon
1188 to each target.

| At 175 | dmg/s | Against the Ninja at 99 | |
|---|---|---|---|
| Cross Slash + Soul Cutter (own) | 656 | 2.04 times Throw Huuma Shuriken | met: the kept Throw Huuma Shuriken reaches 1.78, so the band is 1.67 to 2.04 |
| Swirling Petal, per target | 320 | 0.49 of Cross Slash + Soul Cutter | met |
| Kunai Explosion, per target | 323 | 0.49 of Cross Slash + Soul Cutter | met |

On the pack with an Abysmal Knight's defences Swirling Petal takes
118.1 s and Kunai Explosion 112.9 s.

#### Magic and charms

A magical build casts the Ninja's spells. Two rules hold for them:

- **A Ninja's spell is never weaker on a Kagerou or Oboro than on a
  Ninja.** Without a charm they are cast exactly as a Ninja casts them,
  and they grow with the character like every kept skill.
- **Every charm adds.** Charms (up to ten of one element, for five
  minutes, a cast and a charm item each) add to every ninjutsu of their
  element, by a different amount for each spell, as in renewal. A
  Kagerou or Oboro gets **60%** of renewal's amount
  (`lua/kagerou_oboro.lua`, `CHARM_KEPT`). With ten charms that is about
  2.2 times for Ice Spear, 1.6 for Wind Blade, 1.7 for Fire Petal and
  Exploding Dragon, 2.0 for Kamaitachi, 2.7 for Ice Meteor, 1.3 for
  Lightning Strike and 3.4 for Fire Formation.

Measured on a plain dummy, dmg/s (to each target for the area spells):

| | Ninja 99 | Kagerou 175, no charm | Kagerou 175, ten charms |
|---|---|---|---|
| Ice Spear | 2140 | 3197 | 7315 (Oboro 7111 to 7221) |
| Kamaitachi | 1921 | 2823 | 5730 |
| Exploding Dragon | 1188 | 1620 | 2686 |

A Warlock at 175 does 4028 with Hell Inferno and 4073 with Soul
Expansion, so a fully charged Kagerou or Oboro is ahead on one target.
That is accepted: the Warlock's place is area damage, and the Ninja's
areas are small. The two are compared on a **wide pack**: eight plain
monsters three cells apart around the caster. Seconds to clear it:

| | |
|---|---|
| Warlock 175: Comet | 30.9 |
| Warlock 175: Chain Lightning | 57.0 |
| Warlock 175: Jack Frost | 85.8 |
| Warlock 175: Crimson Rock | 95.0 |
| High Wizard 99: Lord of Vermilion | 54.2 |
| High Wizard 99: Meteor Storm | 110.8 |
| Kagerou 175, ten charms: Kamaitachi | 71.1 (Oboro 70.0) |
| Kagerou 175, ten charms: Exploding Dragon | 125.5 (Oboro 121.7) |
| Kagerou 175, ten charms: Ice Meteor | 132.3 |
| Kagerou 175, no charm: Kamaitachi | 130.1 |
| Kagerou 175, no charm: Exploding Dragon | 191.6 |
| Kagerou 175, no charm: Ice Meteor | 433.5 |
| Ninja 99: Kamaitachi | 199.6 |
| Ninja 99: Exploding Dragon | 269.8 |
| Ninja 99: Ice Meteor | 545.8 |

The Warlock's best spell clears it 2.3 times as fast as a fully charged
Kagerou's best, and a High Wizard at 99 is still faster than that
Kagerou. Without charms a Kagerou is 1.4 to 1.5 times as fast as a
Ninja; with ten, 2.1 to 4 times.

- **16th Night** halves cast times and was always up in renewal's
  numbers, which doubled all of the above again. Here it lasts 30 s and
  has a 3 minute cooldown: a burst.
- **Release Ninja Spell** as the only attack does 920 dmg/s.
- **Distorted Crescent** lowers MATK when HP and SP have the wrong
  parity (4578 instead of 7111 on Ice Spear); its good case was not
  measured. Shadow Warrior raises only physical damage.
- As a caster's, its area spells are not held to half of its single
  target. Kunai Splash was not measured at level 175.

The Kagerou dual-wields daggers. Cross Slash leaves a Cross Wound, and a
Cross Slash on a wounded target hits much harder. Renewal means that for
a Kagerou and an Oboro taking turns, but in rAthena your own wound
counts too, so the figure above already includes it. Other buffs (Shadow
Warrior, Enchant Deadly Poison) are not counted. The runs are recorded
in `tools/transcendent-third-classes/level175/README.md`.

### Equipment

Four tiers, Kagerou/Oboro only, each a Huuma Shuriken, a Kodachi (a dagger,
for dual-wielding), a mask, a garb, a scarf, tabi and a charm. Mask, garb,
scarf and tabi of one tier give a set bonus.

| Tier | Level | Drops from |
|---|---|---|
| Kagemaru | 50 | Kapha, Green Maiden, Nine Tail, Dryad, Yao Jun |
| Tsukikage | 65 | Shinobi, Tengu, Evil Nymph, Baby Hatii, Zealotus |
| Yamigarasu | 80 | Wanderer, Cat o' Nine Tails, Eremes Guile, Dark Illusion, White Lady |
| Oborozuki | 95 | Samurai Specter, Evil Snake Lord, Assassin Cross Eremes, White Lady (MVP) |

The items borrow stock art (the Kitsune, Assassin, Kabuki and Dragon Arhat
masks, stock Huuma and dagger looks), so the mod ships no sprites.

Every item a Ninja can wear or use, a Kagerou and Oboro can too: the
equipment, shuriken and kunai, and awakening potions.

The **Shadow Supplier** beside Kirikage sells what the skills consume and
pre-renewal has no other source for: the four charms, Makibishi, Explosive
Kunai and Shadow Orbs. Kunai for Kunai Splash come from the Kunai Merchant
as usual.

## Rebellion

The Gunslinger's renewal advancement, **Rebellion**, in pre-renewal, as the
next step of a finished Gunslinger.

rAthena's server already knows the class in a pre-renewal build: the job id
and every RL skill are compiled in. What pre-renewal lacks is the data: no
HP, SP, EXP, ASPD or job-bonus tables, no skill tree, item tables that let no
Rebellion use a gun, skill entries from an older revision, five consumables
the skills need, and no way to become one. This mod supplies all of it, and
changes nothing in rAthena or the app.

### The path

Talk to **Old Hand Jesse** beside Master Miller, the Gunslinger job master
(`que_ng`), as a **Gunslinger at base level 99 and job level 70**, with no
unspent skill points. There is no rebirth: the Gunslinger becomes a
**Rebellion** on the spot, keeps every Gunslinger skill, and its base
level goes on to 175. The step cannot be undone, and you are asked to
confirm it.

A Rebellion starts again at job level 1 and goes to 60. That gives 59
skill points on top of the Novice's 9 and the Gunslinger's 69, **137** in
all, ten below renewal's 147.

### How strong

The aim is about 1.5 times a Gunslinger at level 99 on one target, and
at most half of that on each target of an area (see *Area damage*
above):

- **HP**: the Hunter's table times 1.1. A Sniper gets it times 1.25.
- **SP**: the Gunslinger's table times 1.1.
- **Job bonuses**: renewal's Rebellion bonuses to job 60, then three more, for
  +40 in all. A transcendent class gets +45.
- **EXP**: the transcendent base table to 99, and from there as under
  *Level 175 and the soft cap* above.
- **ASPD and weight**: the Gunslinger's.
- **Cast times**: pre-renewal has no fixed cast time, and DEX shortens every
  cast to nothing at 150. 75% of each skill's renewal fixed cast becomes
  after-cast delay, which DEX does not reduce, and the rest is added to its
  cast time: Mass Spiral casts in 1.5 s (before DEX) and then waits 2.5 s.
- **Skill damage**: scaled in `lua/rebellion.lua`, then measured at base
  level 175 against a Gunslinger at level 99: every stat point spent, a
  test gun of each kind, no consumables, on a target with an Abysmal
  Knight's defences.

The Gunslinger's reference at level 99 is Rapid Shower, 1621 dmg/s
(Tracking does 782, and Desperado 3198 to each target). The Rebellion
keeps them: at 175 Rapid Shower reaches 1.19 times and Desperado 1.07
times. The target for each gun's own skills is 1.5 times Rapid Shower,
within a tenth (1.35 to 1.65):

| At 175 | dmg/s | Against Rapid Shower at 99 | |
|---|---|---|---|
| Rifle: Mass Spiral + Anti-Material Blast | 2399 to 2645 | 1.48 to 1.63 | met |
| Shotgun: Banishing Buster + Slug Shot + Shatter Storm | 2223 | 1.37 | met |
| Grenade launcher: Howling Mine + Dragon Tail | 2501 | 1.54 | met |

| Area, per target | dmg/s | Of the rifle | |
|---|---|---|---|
| Fire Dance | 1239 | 0.47 | met |
| Round Trip | 1115 | 0.42 | met |
| Fire Rain | 790 | 0.30 | met |
| Shatter Storm | 809 | 0.31 | met |

Skills of one gun are scaled together, since their cooldowns interleave.
Round Trip's second hit, which lands when the target cannot be pushed
back, has a factor of its own: unscaled it was most of the skill's
damage on a monster that cannot be knocked back.

What to know about these figures:

- The grenade launcher figure is from three single runs after its last
  change, on a build with STR 70: the DEX build could not carry the
  launcher, and every cast was refused.
- **No pack of five was timed.** The Gunslinger's Desperado deals 3198
  to each target, more than any Rebellion area skill, and the Rebellion
  keeps it.
- Buffs (Heat Barrel, Platinum Alter, Improve Concentration) and gear
  bonuses are not counted.

### Equipment

Four tiers, Rebellion only, each a Revolver, a Rifle, a Gatling Gun, a
Shotgun, a Grenade Launcher, a hat, a coat, a poncho, boots and a badge. Hat,
coat, poncho and boots of one tier give a set bonus. Each gun raises the
skills that gun type is for.

| Tier | Level | Drops from |
|---|---|---|
| Dustwalker | 50 | Orc Archer, Obsidian, Remover, Mineral, Breeze |
| Bounty Hunter's | 65 | Apocalypse, Gig, Goblin Leader, Frus, Skogul |
| Outlaw's | 80 | Venatu, Dimik, Archdam, Cecil Damon, Howard Alt-Eisen |
| Hellfire | 95 | Sniper Cecil, Kiel D-01, RSX-0806, Whitesmith Howard, Lord Knight Seyren |

No monster drops two classes' gear (the build script refuses it), so each
stays within rAthena's ten drops per monster.

The items borrow stock art (stock gun looks, the Western Grace, Cowboy Hat
and Pirate Bandana), so the mod ships no sprites.

Every item a Gunslinger can wear or use, a Rebellion can too: guns, bullets,
grenades and the Gunslinger's gear.

The **Gunsmith** beside Jesse sells what the skills consume and pre-renewal
has no other source for: Full Metal Jacket, Grenade Launcher mines, Dragon
Tail Missile, Slug Bullet and Special Alloy Trap. Bullets and Silver Bullets
(for Platinum Alter) come from the stock gun shops.

## Star Emperor

**Star Emperor** in pre-renewal, as the next step of a finished Star
Gladiator.

rAthena's server already knows the Star Emperor in a pre-renewal build: the
class and every SJ skill are compiled in, and it already lets the class wear
what a Star Gladiator wears and, as a third class, the transcendent-only
items. What pre-renewal lacks is the data: no HP, SP, EXP, ASPD or job-bonus
tables, no skill tree, skill entries from an older revision, and no way to
become one. This mod supplies it, and changes nothing in rAthena or the app.

### The path

Talk to **Master Haneul** beside Phoenix, the Taekwon master in Payon
(`payon 160 141`), as a **Star Gladiator at base level 99 and job level
50**, with no unspent skill points. There is no rebirth: the Star
Gladiator becomes a **Star Emperor** on the spot, keeps every Taekwon and
Star Gladiator skill, and its base level goes on to 175. The step cannot
be undone, and you are asked to confirm it.

A Star Emperor starts again at job level 1 and goes to 70. That gives 69
skill points on top of the Novice's 9, the Taekwon's 49 and the Star
Gladiator's 49, **176** in all, as many as renewal's Star Emperor has.

### How strong

As the Star Gladiator's advancement, measured at 175/70. Its own kicks sit
just above what the Star Gladiator's kept kicks reach at 175, and an area
kick deals about half of that to each target (see *Area damage* above):

- **HP and SP**: the Star Gladiator's tables times 1.1. A transcendent class
  gets its second class's table times 1.25.
- **Job bonuses**: renewal's Star Emperor bonuses, less the last three, for
  +40. A transcendent class gets +45.
- **EXP**: the transcendent base table to 99, and from there as under
  *Level 175 and the soft cap* above. The 70 job levels cost 14 billion
  job EXP in all.
- **ASPD and weight**: the Star Gladiator's.
- **Cast times**: pre-renewal has no fixed cast time, and DEX shortens every
  cast to nothing at 150. 75% of each skill's renewal fixed cast becomes
  after-cast delay, which DEX does not reduce, and the rest is added to its
  cast time: New Moon Kick casts in 1.25 s (before DEX) and then waits 0.75 s.
  A skill with a cooldown of 10 s or more cannot be spammed anyway, so its
  whole fixed cast goes into the cast time, where DEX reduces it: Nova
  Explosion, Star Emperor Advent, Book of Creating Star.
- **Gear**: everything a Star Gladiator wears, and the transcendent-only
  items (rAthena allows third classes those in pre-renewal).
- **Skill damage**: scaled in `lua/star_emperor.lua`, then measured on a
  pre-renewal server against a Star Gladiator at 99/50 with the same stats
  and weapon, on the same target:

  | At 175/70 | Star Emperor | Against the Star Gladiator's kicks (132 dmg/s) |
  |---|---|---|
  | The Star Gladiator's kicks, kept | 295 dmg/s | 2.2 times |
  | Prominence Kick (+ Solar Burst) | 274 | 2.1 times |
  | Attacks under the stances, with Falling Star | 336 | 2.5 times |
  | New Moon Kick + Full Moon Kick (area, each target) | 127 | 0.46 of Prominence Kick |

  The kept kicks already pass 1.5 times with the levels alone, so the Star
  Emperor's own kicks are set beside them instead of at 1.5 times. The
  Star Gladiator's kicks follow random stance procs and read 111 to 146 in
  three rounds; 132 is the middle one. All of these numbers are low next to
  other classes: the dummy stands still, and the kicks are counters.

  Nova Explosion, Star Emperor Advent, Gravity Control and the two Books work
  only on PvP and GvG maps, as in renewal, and are left as they are. Buffs
  and gear bonuses are not counted.

### Equipment

Four tiers, Star Emperor only, each a book, a hat, a dobok, a mantle, shoes
and a talisman. Hat, dobok, mantle and shoes of one tier give a set bonus;
the books raise the kicks.

| Tier | Level | Drops from |
|---|---|---|
| Dawn | 50 | Nightmare, Gargoyle, Knocker |
| Zenith | 65 | False Angel, Arc Angeling, Harpy |
| Eclipse | 80 | Fire Imp, Kasa, Gryphon |
| Celestial | 95 | Ifrit, Moonlight Flower, Valkyrie Randgris |

No monster drops two classes' gear (the build script refuses it), so each
stays within rAthena's ten drops per monster. The items borrow stock art (the Solar Hat, Crescent Helm, Moonlight
Flower Hat and Hat of the Sun God), so the mod ships no sprites.

## Soul Reaper

**Soul Reaper** in pre-renewal, as the next step of a finished Soul
Linker.

rAthena's server already knows the Soul Reaper in a pre-renewal build: the
class and every SP skill are compiled in, and it already lets the class wear
what a Soul Linker wears and, as a third class, the transcendent-only items.
What pre-renewal lacks is the data: no HP, SP, EXP, ASPD or job-bonus
tables, no skill tree, skill entries from an older revision, and no way to
become one. This mod supplies it, and changes nothing in rAthena or the app.

### The path

Talk to **Shaman Seol** beside Phoenix, the Taekwon master in Payon
(`payon 154 141`), as a **Soul Linker at base level 99 and job level
50**, with no unspent skill points. There is no rebirth: the Soul Linker
becomes a **Soul Reaper** on the spot, keeps every Taekwon and Soul
Linker skill (the spirits), and its base level goes on to 175. The step
cannot be undone, and you are asked to confirm it.

A Soul Reaper starts again at job level 1 and goes to 70. That gives 69
skill points on top of the Novice's 9, the Taekwon's 49 and the Soul
Linker's 49, **176** in all.

### How strong

As the Soul Linker's advancement, measured at 175/70: about 1.4 times a
Soul Linker at 99/50 on one target.

- **HP and SP**: the Soul Linker's tables times 1.1. A transcendent class
  gets its second class's table times 1.25.
- **Job bonuses**: renewal's Soul Reaper bonuses, less the last three, for
  +40. A transcendent class gets +45.
- **EXP**: the transcendent base table to 99, and from there as under
  *Level 175 and the soft cap* above. The 70 job levels cost 14 billion
  job EXP in all.
- **Gear**: everything a Soul Linker wears, and the transcendent-only items.
- **Cast times**: pre-renewal has no fixed cast time, and DEX shortens every
  cast to nothing at 150. 75% of each skill's renewal fixed cast becomes
  after-cast delay, which DEX does not reduce, and the rest is added to its
  cast time: Espa casts in 0.75 s (before DEX) and then waits 0.75 s. A
  skill (or level) with a cooldown of 10 s or more cannot be spammed anyway,
  so its whole fixed cast goes into the cast time, where DEX reduces it: Soul
  Explosion, the Soul Reaper buff, Soul Unity from level 2.
- **Skill damage**: scaled in `lua/soul_reaper.lua`, then measured on a
  pre-renewal server against a Soul Linker at 99/50 with the same stats and
  staff, on the same target without defence or element:

  | At 175/70 | Soul Reaper | Against the Soul Linker's Estin + Esma (3632 dmg/s) |
  |---|---|---|
  | Espa | 5083 dmg/s | 1.40 times |
  | Espa + Eswhoo, soul energy refilled | 4921 | 1.35 times |
  | The Soul Linker's Estin + Esma, kept | 4448 | 1.22 times |

  The aim is 1.5 times the base class, met within a tenth.

  The Soul Linker has no area spell, so Curse Explosion is measured
  against the class's own Espa on a pack of five: an area skill has to
  clear a pack faster than the single-target skill cast on each, or it
  has no use. Espa one by one takes 36.5 s; Soul Curse on each and then
  Curse Explosion takes 24.4 s, 1.5 times as fast. On one target Espa is
  the better skill.

  Soul energy comes from Soul Collect (one every 20 s at level 5); the Soul
  Reaper buff only gains it against players. Espa costs none at level 10 and
  carries the damage; Eswhoo and Curse Explosion are bursts that spend it.
  Soul Division and Soul Explosion work only on PvP and GvG maps, as in
  renewal, and are left as they are.

### Equipment

Four tiers, Soul Reaper only, each a staff, a hood, a robe, a shawl, shoes
and a bell. Hood, robe, shawl and shoes of one tier give a set bonus; the
staves raise Espa, Eswhoo and Curse Explosion.

| Tier | Level | Drops from |
|---|---|---|
| Wisp | 50 | Wraith, Wind Ghost, Injustice |
| Shade | 65 | Gibbet, Dullahan, Disguise |
| Revenant | 80 | Loli Ruri, Bloody Murderer, Baroness of Retribution |
| Reaper's | 95 | Lord of the Dead, Dracula, Memory of Thanatos |

No monster drops two classes' gear (the build script refuses it), so each
stays within rAthena's ten drops per monster. The items borrow stock art (Morpheus's Hood, Whisper
Mask, Necromancer's Hood, Skull Hood), so the mod ships no sprites.

## Expanded Super Novice

The Super Novice's renewal advancement, the **Expanded Super Novice**, in
pre-renewal, as the next step of a finished Super Novice.

rAthena's server already knows the class in a pre-renewal build. What
pre-renewal lacks is the data: no HP, SP, EXP, ASPD or job-bonus tables,
no skill tree, only one-level stubs of the class's two own skills, and no
way to become one. This mod supplies it, and changes nothing in rAthena
or the app.

### The path

Talk to **Old Novice Nodor** beside Tzerero, the Super Novice job changer
in Aldebaran (`aldeba_in 220 167`), as a **Super Novice at base level 99
and job level 99**, with no unspent skill points. There is no rebirth:
the Super Novice becomes an **Expanded Super Novice** on the spot, keeps
every skill it has, and its base level goes on to 175. The step cannot be
undone, and you are asked to confirm it.

An Expanded Super Novice starts again at job level 1 and goes to 70. That
gives 69 skill points on top of the Novice's 9 and the Super Novice's 98,
**176** in all.

The new points buy renewal's tree for the class: two passives of its own,
**Breakthrough** and **Transcendence** (five levels each), and a share of
the second classes' skills:

| From | Skills |
|---|---|
| Priest | Impositio Manus, Aspersio, Sanctuary, Status Recovery, Magnificat, Gloria |
| Wizard | Jupitel Thunder, Lord of Vermilion, Storm Gust, Meteor Storm, Heaven's Drive, Earth Spike, Water Ball, Fire Pillar, Sightrasher, Frost Nova, Ice Wall, Quagmire, Sense |
| Crusader | Faith, Auto Guard, Shield Charge, Shield Boomerang, Holy Cross |
| Monk | Iron Fists, Summon Spirit Sphere, Absorb Spirit Sphere, Fury |
| Assassin | Enchant Poison, Poison React, Venom Dust, Venom Splasher |
| Rogue | Gank, Mug, Back Stab, Tunnel Drive, Sightless Mind |
| Hunter | Skid Trap, Land Mine, Beast Bane |
| Blacksmith | Hilt Binding, Weapon Research, Weapon Repair |
| Alchemist | Axe Mastery |
| Transcendent classes | Magic Crasher, Zen |

### How strong

The aim is the same as for the other advancements: about 1.5 times a
Super Novice at 99/99 on one target, or just above a kept skill that
grows past that.

- **HP and SP**: the Super Novice's tables times 1.1. A transcendent class
  gets its second class's table times 1.25.
- **Job bonuses**: renewal's Expanded Super Novice bonuses, less the last
  four, for +40. A transcendent class gets +45.
- **EXP**: the transcendent base table to 99, and from there as under
  *Level 175 and the soft cap* above. The 70 job levels cost 14 billion
  job EXP in all.
- **ASPD and weight**: the Super Novice's.
- **Skill damage**: measured at base level 175 and job level 70 against
  a Super Novice at 99/99 with the same stats and weapon, on the same
  target without defence or element:

  | At 175/70, one target | dmg/s | Against the Super Novice at 99/99 |
  |---|---|---|
  | Bash, kept | 3470 | 2.2 times its Bash (1564) |
  | Fire Bolt, kept | 1755 | 1.6 times its Fire Bolt (1110) |
  | Plain attacks | 1666 | 2.8 times its plain attacks (589) |

  | Area, each target | dmg/s |
  |---|---|
  | Thunderstorm, kept | 1445 |

  The class's own two skills are passives, so nothing of its own is
  scaled. Breakthrough adds flat damage to every hit, which is why plain
  attacks gain the most. With the passives and the levels, the skills it
  keeps from the Super Novice already pass 1.5 times by themselves.

  **The second-class skills it gains** are held below the classes they
  belong to: it may be strong with them, but its edge is the size of its
  skill pool, not being a better Wizard or Crusader. Each is set to about
  75 % of what the third class keeping that skill does with it at 175/70
  (same target, no Amplify Magic Power):

  | | That class at 175/70 | Expanded Super Novice | |
  |---|---|---|---|
  | Jupitel Thunder | Warlock 3754 | 3003 | 80 % |
  | Holy Cross | Royal Guard 3210 | 2450 | 76 % |
  | Storm Gust, each target | Warlock 980 | 769 | 78 % |
  | Lord of Vermilion, each target | Warlock 930 | 697 | 75 % |
  | Meteor Storm, each target | Warlock 1894 | 1422 | 75 % |
  | Heaven's Drive, each target | Sorcerer about 1130 | 802 | 71 % |

  Untouched, five of the six were level with those classes or above them
  (Holy Cross 120 %, Heaven's Drive 127 %). For scale, a High Wizard at
  99/70 does 2983 with Jupitel Thunder and a Paladin 1538 with Holy
  Cross.

  The factors are in `lua/super_novice.lua` and apply only when the
  caster is an Expanded Super Novice. A Wizard's Jupitel Thunder, Meteor
  Storm and Heaven's Drive and a Crusader's Holy Cross are unchanged.
  The runs are recorded in
  `tools/transcendent-third-classes/level175/super_novice.json`.

### Equipment

Four tiers, Expanded Super Novice only, each a knife (a dagger), a cap, a
plate, a manteau, boots and a badge. Cap, plate, manteau and boots of one
tier give a set bonus: all stats and MaxHP, and MaxSP too from the third
tier.

| Tier | Level | Drops from |
|---|---|---|
| Greenhorn's | 50 | Carat, Alarm, Clock |
| Wayfarer's | 65 | Sting, Gajomart, Majoruros |
| Veteran's | 80 | Chimera, Mysteltainn, Executioner |
| Paragon's | 95 | Gloom Under Night, Doppelganger, Orc Hero |

No monster drops two classes' gear (the build script refuses it), so each
stays within rAthena's ten drops per monster. The items borrow stock art
(the Novice and Angel sets, the Super Novice Hat, Helm of Angel, stock
dagger looks), so the mod ships no sprites.

## Files

Everything under `db/`, `System/` and `data/` is generated, together with
transcendent-third-classes, by `tools/transcendent-third-classes/build.py`
(and `build_skill_descriptions.py`), from the pinned rAthena and each
class's CSV files (`kagerou_oboro/`, `rebellion/`, `star_emperor/`,
`soul_reaper/`, `super_novice/` there). `lua/` and `npc/` are written by hand.
The damage figures come from `balance-<class>.json` beside the build;
`tools/expanded_class/balance/README.md` says how to measure them.

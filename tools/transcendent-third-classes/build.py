#!/usr/bin/env python3
"""Regenerate the transcendent-third-classes and expanded-classes mods' tables from rAthena and CSV files.

    python3 tools/transcendent-third-classes/build.py --rathena ../rathena            # rewrite them
    python3 tools/transcendent-third-classes/build.py --rathena ../rathena --check    # fail if stale

The work is done by tools/expanded_class/expanded_class.py; this file
only describes the classes. docs/EXPANDED_CLASS_REBIRTH.md is the guide.

A renewal third class here is the UPGRADE of the transcendent second class: a
transcendent character at base 99 / job 70 advances to it, keeps every skill it
has, starts its job level again at 1 (to 70) and goes on to base level 175. The
skill tree is renewal's third-class tree on top of the inherited ones; HP, SP
and EXP continue from the transcendent class's tables; damage is measured at
175/70 against the transcendent class at 99/70 (level175/README.md).

The thirteen: Guillotine Cross (Assassin Cross), Shadow Chaser (Stalker), Arch
Bishop (High Priest), Rune Knight (Lord Knight), Royal Guard (Paladin), Warlock
(High Wizard), Sura (Champion), Ranger (Sniper), Minstrel and Wanderer (Clown
and Gypsy), Genetic (Creator), Mechanic (Whitesmith), Sorcerer (Professor).
Each class keeps its CSV files in its own directory.

The expanded advancements are a mod of their own, expanded-classes, built here
too: each the step after its finished base class, Kagerou and Oboro (Ninja),
Rebellion (Gunslinger), Star Emperor (Star Gladiator), Soul Reaper (Soul Linker)
and the Expanded Super Novice (Super Novice). Both mods need level175-core, which
holds what they share: the soft cap for base stats and the level rule.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "expanded_class"))
import expanded_class as ec  # noqa: E402

WEAPONS = {
    "katar":  dict(type="Weapon", sub="Katar",  loc=["Both_Hand"],  label="Katar",  unid="Katar"),
    "dagger": dict(type="Weapon", sub="Dagger", loc=["Right_Hand"], label="Dagger", unid="Dagger"),
    "bow":    dict(type="Weapon", sub="Bow",    loc=["Both_Hand"],  label="Bow",    unid="Bow"),
    "mace":   dict(type="Weapon", sub="Mace",   loc=["Right_Hand"], label="Mace",   unid="Mace"),
    "staff":  dict(type="Weapon", sub="Staff",  loc=["Right_Hand"], label="Staff",  unid="Rod"),
    "sword2": dict(type="Weapon", sub="2hSword", loc=["Both_Hand"], label="Two-Handed Sword", unid="Sword"),
    "spear2": dict(type="Weapon", sub="2hSpear", loc=["Both_Hand"], label="Two-Handed Spear", unid="Spear"),
    "spear1": dict(type="Weapon", sub="1hSpear", loc=["Right_Hand"], label="Spear", unid="Spear"),
    "staff2": dict(type="Weapon", sub="2hStaff", loc=["Both_Hand"], label="Two-Handed Staff", unid="Rod"),
    "shield": dict(type="Armor",  sub=None,      loc=["Left_Hand"],  label="Shield", unid="Shield", view=True),
    "knuckle": dict(type="Weapon", sub="Knuckle", loc=["Right_Hand"], label="Knuckle", unid="Knuckle"),
    "musical": dict(type="Weapon", sub="Musical", loc=["Right_Hand"], label="Instrument", unid="Instrument", gender="Male"),
    "whip":   dict(type="Weapon", sub="Whip",    loc=["Right_Hand"], label="Whip", unid="Whip", gender="Female"),
    "axe1":   dict(type="Weapon", sub="1hAxe",   loc=["Right_Hand"], label="Axe", unid="Axe"),
    "axe2":   dict(type="Weapon", sub="2hAxe",   loc=["Both_Hand"],  label="Two-Handed Axe", unid="Axe"),
    "book":   dict(type="Weapon", sub="Book",    loc=["Right_Hand"], label="Book", unid="Book"),
}

def base_exp_above(level, last):
    """EXP from `level` to the next, for 99..174. `last` is the EXP of 98 to 99
    on the class's stock table. The first step above the old cap costs what
    the last one below it did, and the cost rises evenly to twice that at
    174 to 175: with monsters that pay the same EXP an hour at every level
    step, a level takes as long as 98 to 99 at first and twice as long at
    the end."""
    return round(last * (1 + (level - 99) / 75) / 1000) * 1000


# The classes' own job levels (1 to their cap, starting again after the change) are meant to be
# finished at about base level 150 by a character levelling in content of its own level. Base EXP
# from 99 to 150 is 23.34 billion (base_exp_above); the endgame monsters pay 0.6 job EXP for each
# base EXP, as pre-renewal's own high monsters roughly do.
JOB_EXP_TOTAL = round(0.6 * sum(343210000 * (1 + (l - 99) / 75) for l in range(99, 150)) / 1e6) * 1000000


# Shared by every class: the transcendent class's job levels and bonus total,
# the fixed cast time rule (docs/EXPANDED_CLASS_REBIRTH.md, section 7),
# and level 175 with base stats to 150, for these classes only.
COMMON = dict(MOD_NAME="transcendent-third-classes", BONUS_TOTAL=45, MAX_JOB_LEVEL=70,
              EQUIP_CLASSES=["Upper"], FIXED_CAST_TO_DELAY=0.75, WEAPON_KINDS=WEAPONS,
              MAX_BASE_LEVEL=175, BASE_EXP_ABOVE=base_exp_above, MAX_STATS=150, JOB_EXP_TOTAL=JOB_EXP_TOTAL,
              TREE_KEEPS_UPPER=True)

guillotine_cross = ec.config(
    __file__, **COMMON,
    JOBS=("Guillotine_Cross_T",),
    # Renewal's Guillotine Cross tree: Novice, Thief, Assassin and the 19 GC
    # skills; renewal's transcendent one also inherits Assassin Cross.
    TREE_FROM={"Guillotine_Cross_T": "Guillotine_Cross"},
    BASE="Assassin_Cross",
    # Full Throttle is in every third class's tree; it is written once, here.
    # Pre-renewal's entry starts no status (renewal's starts Full_Throttle).
    SKILL_PREFIX=("GC_", "ALL_FULL_THROTTLE"),
    # Parity with the Assassin Cross: its own HP, SP and EXP tables. The class
    # is transcendent in rAthena, so it gets the same 125% HP bonus.
    HP_FROM="Assassin_Cross", HP_SCALE=1.0,
    SP_FROM="Assassin_Cross", SP_SCALE=1.0,
    EXP_FROM="Assassin_Cross",
    # Renewal's Guillotine Cross bonuses come to +43 by job 70; two more make
    # a transcendent class's +45.
    EXTRA_BONUS=[(68, "Agi"), (70, "Str")],
    # Its weapons suit both of the Assassin's transcendent paths: an
    # Assassin's Jobs: key and Classes: Upper, which a third class also meets.
    EQUIP_JOBS=["Assassin"],
    EQUIP_LABEL="Assassin Cross or Guillotine Cross",
    ITEMS_ABOUT="The Guillotine Cross's weapons, from guillotine_cross/equipment.csv.",
    CSV_DIR="guillotine_cross",
    # Cross Impact: renewal spams it twice a second; here it is the heavy hit.
    # Full Throttle keeps pre-renewal's 30-minute cooldown (renewal's is 50).
    SKILL_OVERRIDES={"GC_CROSSIMPACT": {"AfterCastActDelay": "1500"},
                     "ALL_FULL_THROTTLE": {"Cooldown": "1800000"}},
)

shadow_chaser = ec.config(
    __file__, **COMMON,
    JOBS=("Shadow_Chaser_T",),
    # Renewal's Shadow Chaser tree: Novice, Thief, Rogue and the SC skills;
    # renewal's transcendent one also inherits Stalker (Preserve, Full Strip).
    TREE_FROM={"Shadow_Chaser_T": "Shadow_Chaser"},
    BASE="Stalker",
    SKILL_PREFIX="SC_",
    HP_FROM="Stalker", HP_SCALE=1.0,
    SP_FROM="Stalker", SP_SCALE=1.0,
    EXP_FROM="Stalker",
    # Renewal's Shadow Chaser bonuses come to +43 by job 70; two more make +45.
    EXTRA_BONUS=[(68, "Dex"), (70, "Agi")],
    EQUIP_JOBS=["Rogue"],
    EQUIP_LABEL="Stalker or Shadow Chaser",
    ITEMS_ABOUT="The Shadow Chaser's weapons, from shadow_chaser/equipment.csv.",
    CSV_DIR="shadow_chaser",
    # Auto Shadow Spell casts copied Mage and Wizard spells. These four more
    # can be copied, aim at the target and cost no item; rAthena skips Holy
    # Light and Magnus Exorcismus in auto-casts, and the self-centred and
    # catalyst ninjutsu would not place or would cast for free.
    SKILL_FLAGS_ADD={"IsAutoShadowSpell": ["PR_TURNUNDEAD", "NJ_KOUENKA", "NJ_HYOUSENSOU", "NJ_HUUJIN"]},
)

arch_bishop = ec.config(
    __file__, **COMMON,
    # Sacrament only shortens fixed cast time, which pre-renewal does not have (owner, 2026-10-18).
    TREE_LEAVE_OUT=["AB_SECRAMENT"],
    JOBS=("Arch_Bishop_T",),
    # Renewal's Arch Bishop tree: Novice, Acolyte, Priest and the AB skills;
    # renewal's transcendent one also inherits High Priest (Assumptio,
    # Basilica, Meditatio, Mana Recharge).
    TREE_FROM={"Arch_Bishop_T": "Arch_Bishop"},
    BASE="High_Priest",
    SKILL_PREFIX="AB_",
    HP_FROM="High_Priest", HP_SCALE=1.0,
    SP_FROM="High_Priest", SP_SCALE=1.0,
    EXP_FROM="High_Priest",
    # Renewal's Arch Bishop bonuses come to +43 by job 70; two more make +45.
    EXTRA_BONUS=[(68, "Int"), (70, "Dex")],
    EQUIP_JOBS=["Priest"],
    EQUIP_LABEL="High Priest or Arch Bishop",
    # Renewal prices the Arch Bishop's own skills for renewal's SP pools and
    # SP gear. On a High Priest's pool and without Meditatio or Mana
    # Recharge they sustained half a High Priest's healing in a party. The
    # party buffs now cost what a High Priest pays to give five people the
    # single buff; the heals give about a High Priest's Heal per SP
    # (Highness Heal) or more across a party (Coluceo Heal).
    SKILL_OVERRIDES={
        "AB_CLEMENTIA":    {"Requires.SpCost": [200, 228, 256]},
        "AB_CANTO":        {"Requires.SpCost": [160, 176, 192]},
        "AB_PRAEFATIO":    {"Requires.SpCost": [70, 78, 86, 94, 102, 109, 117, 125, 132, 140]},
        "AB_HIGHNESSHEAL": {"Requires.SpCost": [30, 43, 55, 68, 80]},
        "AB_CHEAL":        {"Requires.SpCost": [90, 100, 110]},
    },
    # The Ancilla Ancilla makes restores SP and should also start its buff (healing received
    # +15 %), which neither era's item script does (owner, 2026-10-18).
    ITEM_FIELDS={"Ansila": {"Script": "percentheal 0,6; sc_start SC_ANCILLA,300000,0;"}},
    ITEMS_ABOUT="The Arch Bishop's weapons, from arch_bishop/equipment.csv.",
    CSV_DIR="arch_bishop",
)

rune_knight = ec.config(
    __file__, **COMMON,
    JOBS=("Rune_Knight_T",),
    # Renewal's Rune Knight tree: Novice, Swordman, Knight and the RK skills;
    # renewal's transcendent one also inherits Lord Knight (Aura Blade,
    # Berserk, Spiral Pierce, ...).
    TREE_FROM={"Rune_Knight_T": "Rune_Knight"},
    BASE="Lord_Knight",
    SKILL_PREFIX="RK_",
    HP_FROM="Lord_Knight", HP_SCALE=1.0,
    SP_FROM="Lord_Knight", SP_SCALE=1.0,
    EXP_FROM="Lord_Knight",
    # Renewal's Rune Knight bonuses come to +43 by job 70; two more make +45.
    EXTRA_BONUS=[(68, "Str"), (70, "Vit")],
    EQUIP_JOBS=["Knight"],
    EQUIP_LABEL="Lord Knight or Rune Knight",
    ITEMS_ABOUT="The Rune Knight's weapons, from rune_knight/equipment.csv.",
    CSV_DIR="rune_knight",
    # Rune stones. Pre-renewal's rune items have no reuse delay; renewal's
    # Crush Strike, Millennium Shield and Refresh runes have one, and get it
    # back. Giant Growth (STR +30, +250% on a Rune Knight's attacks, 30% of
    # hits 2.5x) lasts 15 minutes in renewal: here it is a burst, 30 seconds
    # once every 3 minutes, like Enchant Deadly Poison. Storm Blast hits
    # everything around for about 4400 a target; renewal lets a rune go
    # every second, about 2200 dmg/s a target from a stack of runes: here
    # one every 10 seconds, a burst well inside the area cap.
    ITEM_FIELDS={
        "Runstone_Rhydo": {"Delay": "renewal"},
        "Runstone_Verkana": {"Delay": "renewal"},
        "Runstone_Nosiege": {"Delay": "renewal"},
        "Runstone_Pertz": {"Delay": {"Duration": 10000, "Status": "Reuse_Stormblast"}},
        "Runstone_Turisus": {"Delay": {"Duration": 180000}},
    },
    # Hundred Spear: the mod's ratio factor would land on its 3x3-7x7 splash too (9126 %
    # over 7x7 at level 10): single target, as Varetyr Spear and Hell Inferno (owner, 2026-10-18).
    SKILL_OVERRIDES={"RK_GIANTGROWTH": {"Duration1": 30000}, "RK_HUNDREDSPEAR": {"SplashArea": "0"}},
    # What the rune stones' own descriptions do not say, or no longer get
    # right, after the delays above.
    ITEM_DESCRIPTIONS={
        "Runstone_Turisus": ["^FF0000Giant Growth lasts 30 seconds. The rune can be used again after 3 minutes.^000000"],
        "Runstone_Rhydo": ["^FF0000The rune can be used again after 30 seconds.^000000"],
        "Runstone_Verkana": ["^FF0000The rune can be used again after 60 seconds.^000000"],
        "Runstone_Nosiege": ["^FF0000The rune can be used again after 2 minutes.^000000"],
        "Runstone_Pertz": ["^FF0000The rune can be used again after 10 seconds.^000000"],
    },
)

royal_guard = ec.config(
    __file__, **COMMON,
    JOBS=("Royal_Guard_T",),
    # Renewal's Royal Guard tree: Novice, Swordman, Crusader and the LG
    # skills; renewal's transcendent one also inherits Paladin (Gloria
    # Domini, Martyr's Reckoning, Battle Chant, Rapid Smiting).
    TREE_FROM={"Royal_Guard_T": "Royal_Guard"},
    BASE="Paladin",
    SKILL_PREFIX="LG_",
    HP_FROM="Paladin", HP_SCALE=1.0,
    SP_FROM="Paladin", SP_SCALE=1.0,
    EXP_FROM="Paladin",
    # Renewal's Royal Guard bonuses come to +43 by job 70; two more make +45.
    EXTRA_BONUS=[(68, "Vit"), (70, "Str")],
    EQUIP_JOBS=["Crusader"],
    EQUIP_LABEL="Paladin or Royal Guard",
    # Moon Slasher readies Overbrand's stronger hit; pre-renewal has no such status.
    STATUSES_FROM_RENEWAL=["OverBrandReady"],
    ITEMS_ABOUT="The Royal Guard's weapons and shields, from royal_guard/equipment.csv.",
    CSV_DIR="royal_guard",
)

warlock = ec.config(
    __file__, **COMMON,
    JOBS=("Warlock_T",),
    # Renewal's Warlock tree: Novice, Mage, Wizard and the WL skills;
    # renewal's transcendent one also inherits High Wizard (Mystical
    # Amplification, Napalm Vulcan, Gravitation Field, ...).
    TREE_FROM={"Warlock_T": "Warlock"},
    BASE="High_Wizard",
    SKILL_PREFIX="WL_",
    HP_FROM="High_Wizard", HP_SCALE=1.0,
    SP_FROM="High_Wizard", SP_SCALE=1.0,
    EXP_FROM="High_Wizard",
    # Renewal's Warlock bonuses come to +43 by job 70; two more make +45.
    EXTRA_BONUS=[(68, "Int"), (70, "Dex")],
    EQUIP_JOBS=["Wizard"],
    EQUIP_LABEL="High Wizard or Warlock",
    ITEMS_ABOUT="The Warlock's weapons, from warlock/equipment.csv.",
    CSV_DIR="warlock",
    # Spellbooks. rAthena reads a book only renewal's way: a WL_MB_ book
    # casts Reading Spellbook (Reading), which needs the passive Reading
    # Spellbook. Pre-renewal has the active skill, neither of the others,
    # no such books and no spellbook_db rows, so all of it comes from
    # renewal. The books are sold in Geffen (npc/spellbook_seller.txt).
    NEW_SKILLS_FROM_RENEWAL=["WL_READING_SB_READING"],
    NEW_FROM_RENEWAL=["WL_MB_SG", "WL_MB_LOV", "WL_MB_MS", "WL_MB_DL", "WL_MB_JF",
                      "WL_MB_ES", "WL_MB_CR", "WL_MB_CL", "WL_MB_CM", "WL_MB_TV"],
    COPY_TABLES={"db/spellbook_db.yml": ("db/re/spellbook_db.yml", "READING_SPELLBOOK_DB", 1)},
    # Pre-renewal's Comet costs 2 Red Gemstones and renewal's none; an import
    # entry cannot take an item cost away, so pre-renewal's stays. Fitting for
    # the Warlock's biggest spell, and the README says so.
    ITEMCOST_KEPT=["WL_COMET"],
    # SP. Without Soul Drain (+20% max SP, SP back on single-target kills)
    # and at renewal's prices, the Warlock's area spells ran a full SP bar
    # dry three times faster than a High Wizard's amplified Meteor Storm at
    # the same damage, and Soul Expansion in about a minute. These costs
    # give its area spells about 0.8x the damage a High Wizard deals with a
    # full SP bar of amplified Meteor Storm, and its single-target spells about
    # 0.9x that of amplified Jupitel Thunder (README.md has the measurements).
    SKILL_OVERRIDES={
        "WL_CRIMSONROCK": {"Requires.SpCost": [25, 29, 34, 38, 42]},
        "WL_JACKFROST": {"Requires.SpCost": [22, 26, 30, 35, 39]},
        "WL_FROSTMISTY": {"Requires.SpCost": [26, 31, 37, 42, 47]},
        # Soul Expansion and Hell Inferno are single-target spells here: renewal's splash made them
        # the Warlock's fastest pack clearers (16.6 s and 11.3 s against a High Wizard's 31.4 s).
        "WL_SOULEXPANSION": {"Requires.SpCost": [17, 20, 22, 25, 28], "SplashArea": "0"},
        "WL_HELLINFERNO": {"Requires.SpCost": [36, 39, 43, 46, 49], "SplashArea": "0"},
        # Chain Lightning strikes at least four times, all on a lone target:
        # scaled as single-target damage, its cost scaled with it.
        "WL_CHAINLIGHTNING": {"Requires.SpCost": [40, 45, 50, 55, 60]},
        "WL_TETRAVORTEX": {"Requires.SpCost": [108, 135, 162, 189, 216, 180, 216, 252, 288, 324]},
    },
)

sura = ec.config(
    __file__, **COMMON,
    JOBS=("Sura_T",),
    # Renewal's Sura tree: Novice, Acolyte, Monk and the SR skills; renewal's
    # transcendent one also inherits Champion (Zen, the Champion combos).
    TREE_FROM={"Sura_T": "Sura"},
    BASE="Champion",
    SKILL_PREFIX="SR_",
    HP_FROM="Champion", HP_SCALE=1.0,
    SP_FROM="Champion", SP_SCALE=1.0,
    EXP_FROM="Champion",
    # Renewal's Sura bonuses come to +43 by job 70; two more make +45.
    EXTRA_BONUS=[(68, "Str"), (70, "Agi")],
    EQUIP_JOBS=["Monk"],
    EQUIP_LABEL="Champion or Sura",
    ITEMS_ABOUT="The Sura's knuckles, from sura/equipment.csv.",
    CSV_DIR="sura",
    # Gates of Hell is the Sura's burst, as Asura Strike is the Champion's;
    # with no cooldown it could be cast every 2.5 s.
    # Tiger Cannon's damage comes mostly from HP and SP, outside the skill's
    # percentage, so a Lua factor barely moves it: a longer cooldown does.
    SKILL_OVERRIDES={"SR_GATEOFHELL": {"Cooldown": "10000"},
                     "SR_TIGERCANNON": {"Cooldown": "7000"}},
)

ranger = ec.config(
    __file__, **COMMON,
    JOBS=("Ranger_T",),
    # Renewal's Ranger tree: Novice, Archer, Hunter and the RA skills;
    # renewal's transcendent one also inherits Sniper (Falcon Assault,
    # Sharp Shooting, True Sight, Wind Walk). The Warg comes with the
    # Ranger's own Warg Mastery, as in renewal: no NPC.
    TREE_FROM={"Ranger_T": "Ranger"},
    BASE="Sniper",
    SKILL_PREFIX="RA_",
    HP_FROM="Sniper", HP_SCALE=1.0,
    SP_FROM="Sniper", SP_SCALE=1.0,
    EXP_FROM="Sniper",
    # Renewal's Ranger bonuses come to +43 by job 70; two more make +45.
    EXTRA_BONUS=[(68, "Dex"), (70, "Agi")],
    EQUIP_JOBS=["Hunter"],
    EQUIP_LABEL="Sniper or Ranger",
    ITEMS_ABOUT="The Ranger's bows, from ranger/equipment.csv.",
    CSV_DIR="ranger",
    # Unlimit more than triples ranged damage; renewal kept it up for 150 s
    # of every 300. Here it is a 30 s burst window.
    # Firing Trap and Icebound Trap: most of their damage comes from DEX and INT, which no
    # factor reaches, and at 175 one did 0.60 of Aimed Bolt to every monster on it. A cooldown
    # holds them to the area limit instead. Icebound Trap hits all of a pack at once, and at
    # 1 s it cleared five 1.75x as fast as a Sniper's Arrow Shower; at 3 s, 1.16x.
    SKILL_OVERRIDES={"RA_UNLIMIT": {"Duration1": "30000"},
                     "RA_FIRINGTRAP": {"Cooldown": "1000"}, "RA_ICEBOUNDTRAP": {"Cooldown": "3000"}},
)

minstrel = ec.config(
    __file__, **COMMON,
    JOBS=("Minstrel_T",),
    # Renewal's Minstrel tree: Novice, Archer, Bard, the shared WM skills and
    # the Minstrel's MI ones; renewal's transcendent one also inherits Clown
    # (Arrow Vulcan, Tarot, Marionette Control, Longing for Freedom).
    TREE_FROM={"Minstrel_T": "Minstrel"},
    BASE="Clown",
    # The WM skills both share are written here once; the Wanderer's
    # config takes only its own WA ones.
    SKILL_PREFIX=("WM_", "MI_"),
    HP_FROM="Clown", HP_SCALE=1.0,
    SP_FROM="Clown", SP_SCALE=1.0,
    EXP_FROM="Clown",
    # Renewal's bonuses come to +43 by job 70; two more make +45.
    EXTRA_BONUS=[(68, "Dex"), (70, "Int")],
    EQUIP_JOBS=["BardDancer"],     # one item_db key for both; instruments are male-only, whips female-only
    EQUIP_LABEL="Clown or Minstrel",
    ITEMS_ABOUT="The Minstrel's instruments, from minstrel/equipment.csv.",
    CSV_DIR="minstrel",
    # Pre-renewal's Reverberation was a ground trap; the skill class now
    # strikes a target (castendDamageId) and never places the unit.
    UNIT_KEPT=["WM_REVERBERATION"],
)

wanderer = ec.config(
    __file__, **COMMON,
    JOBS=("Wanderer_T",),
    TREE_FROM={"Wanderer_T": "Wanderer"},
    BASE="Gypsy",
    SKILL_PREFIX="WA_",
    HP_FROM="Gypsy", HP_SCALE=1.0,
    SP_FROM="Gypsy", SP_SCALE=1.0,
    EXP_FROM="Gypsy",
    # Renewal's bonuses come to +43 by job 70; two more make +45.
    EXTRA_BONUS=[(68, "Dex"), (70, "Int")],
    EQUIP_JOBS=["BardDancer"],
    EQUIP_LABEL="Gypsy or Wanderer",
    ITEMS_ABOUT="The Wanderer's whips, from wanderer/equipment.csv.",
    CSV_DIR="wanderer",
)

genetic = ec.config(
    __file__, **COMMON,
    JOBS=("Genetic_T",),
    # Renewal's Genetic tree: Novice, Merchant, Alchemist and the GN skills;
    # renewal's transcendent one also inherits Creator (Acid Demonstration,
    # Full Chemical Protection, Plant Cultivation, Slim Potion Pitcher).
    TREE_FROM={"Genetic_T": "Genetic"},
    BASE="Creator",
    SKILL_PREFIX="GN_",
    HP_FROM="Creator", HP_SCALE=1.0,
    SP_FROM="Creator", SP_SCALE=1.0,
    EXP_FROM="Creator",
    # Renewal's Genetic bonuses come to +43 by job 70; two more make +45.
    EXTRA_BONUS=[(68, "Str"), (70, "Int")],
    EQUIP_JOBS=["Alchemist"],
    EQUIP_LABEL="Creator or Genetic",
    ITEMS_ABOUT="The Genetic's axes, from genetic/equipment.csv.",
    CSV_DIR="genetic",
    # Pre-renewal's Hell's Plant was a ground unit; renewal's is a status on
    # the caster that sets off GN_HELLS_PLANT_ATK, and places none.
    UNIT_KEPT=["GN_HELLS_PLANT"],
)

mechanic = ec.config(
    __file__, **COMMON,
    JOBS=("Mechanic_T",),
    # Renewal's Mechanic tree: Novice, Merchant, Blacksmith and the NC
    # skills; renewal's transcendent one also inherits Whitesmith (Cart
    # Termination, Meltdown, Maximum Power-Thrust, Upgrade Weapon). The
    # Madogear comes from the Mado Engineer (npc/mado_engineer.txt).
    TREE_FROM={"Mechanic_T": "Mechanic"},
    BASE="Whitesmith",
    SKILL_PREFIX="NC_",
    HP_FROM="Whitesmith", HP_SCALE=1.0,
    SP_FROM="Whitesmith", SP_SCALE=1.0,
    EXP_FROM="Whitesmith",
    # Renewal's Mechanic bonuses come to +43 by job 70; two more make +45.
    EXTRA_BONUS=[(68, "Str"), (70, "Dex")],
    EQUIP_JOBS=["Blacksmith"],
    EQUIP_LABEL="Whitesmith or Mechanic",
    ITEMS_ABOUT="The Mechanic's axes, from mechanic/equipment.csv.",
    CSV_DIR="mechanic",
    # Magma Eruption's lava is fixed damage (800 + 200 per level, twice a
    # tick), which no Lua factor reaches. At renewal's 0.5 s tick one cast's
    # lava killed a whole pack by itself (6.9 s for five, at any cooldown).
    # A tick every second and a 12 s cooldown: a pack in 18.8 s, 1.36x Power
    # Swing one by one, and 0.28 of Power Swing on one target.
    SKILL_OVERRIDES={"NC_MAGMA_ERUPTION": {"Cooldown": "12000", "Unit.Interval": "1000"}},
)

sorcerer = ec.config(
    __file__, **COMMON,
    JOBS=("Sorcerer_T",),
    # Renewal's Sorcerer tree: Novice, Mage, Sage and the SO skills;
    # renewal's transcendent one also inherits Professor (Soul Change,
    # Spider Web, Double Casting, Memorize).
    TREE_FROM={"Sorcerer_T": "Sorcerer"},
    BASE="Professor",
    SKILL_PREFIX="SO_",
    HP_FROM="Professor", HP_SCALE=1.0,
    SP_FROM="Professor", SP_SCALE=1.0,
    EXP_FROM="Professor",
    # Renewal's Sorcerer bonuses come to +43 by job 70; two more make +45.
    EXTRA_BONUS=[(68, "Int"), (70, "Dex")],
    EQUIP_JOBS=["Sage"],
    EQUIP_LABEL="Professor or Sorcerer",
    ITEMS_ABOUT="The Sorcerer's books, from sorcerer/equipment.csv.",
    CSV_DIR="sorcerer",
    # The elemental spirits: pre-renewal loads only the import layer's
    # elemental_db, so renewal's table comes with the mod, without the five
    # spirits of the fourth class (Elemental Master), whose EM_ skills
    # pre-renewal lacks.
    COPY_TABLES={"db/elemental_db.yml": ("db/re/elemental_db.yml", "ELEMENTAL_DB", 2, r"\bEM_EL_")},
    # Pre-renewal's Cloud Kill costs 2 Red Gemstones and renewal's none; an
    # import entry cannot take an item cost away, so pre-renewal's stays.
    ITEMCOST_KEPT=["SO_CLOUD_KILL"],
    # Cloud Kill leaves its targets taking more poison damage; pre-renewal has no such status.
    STATUSES_FROM_RENEWAL=["Cloud_Poison"],
    # Varetyr Spear is the Sorcerer's single-target spell here. Renewal's hits up to a 9x9 area
    # at level 10, which cleared a pack of five in a quarter of the Professor's time (level 175
    # work, pack limits); its other spells are the area skills.
    SKILL_OVERRIDES={"SO_VARETYR_SPEAR": {"SplashArea": "0"}},
)

# The expanded classes, the step after the finished base class: a Ninja becomes a Kagerou
# or Oboro, a Gunslinger a Rebellion, a Star Gladiator a Star
# Emperor, a Soul Linker a Soul Reaper, a Super Novice an Expanded Super Novice. They are the
# expanded-classes mod, with their own NPCs and Lua; docs/EXPANDED_CLASS_REBIRTH.md §1-§11.

kagerou_oboro = ec.config(
    __file__, MAX_BASE_LEVEL=175, BASE_EXP_ABOVE=base_exp_above, MAX_STATS=150, JOB_EXP_TOTAL=JOB_EXP_TOTAL,
    MOD_NAME="expanded-classes",
    JOBS=("Kagerou", "Oboro"),
    ITEM_JOB="KagerouOboro",          # the item_db Jobs: key (EAJ_KAGEROUOBORO)
    BASE="Ninja",
    SKILL_PREFIX=("KO_", "OB_", "KG_"),
    # Kagerou and Oboro sit a little below a transcendent class. Pre-renewal's
    # Assassin Cross gets the Assassin HP table times 1.25; these get it times
    # 1.1. SP follows the Ninja's table, which is already the deeper one.
    HP_FROM="Assassin_Cross", HP_SCALE=1.10,
    SP_FROM="Ninja", SP_SCALE=1.10,
    EXP_FROM="Assassin_Cross",
    # Renewal's job bonuses stop at job level 50; these continue them to 60 and
    # total +40, five below a transcendent class's +45.
    EXTRA_BONUS=[(52, "Str"), (54, "Agi"), (56, "Dex"), (58, "Luk"), (60, "Int")],
    BONUS_TOTAL=40,
    MAX_JOB_LEVEL=60,
    ASPD={"Fist": 400, "Dagger": 500, "Huuma": 700},   # the Ninja's, with a quicker Huuma
    # Kunai Splash's damage is added outside the skill's percentage
    # (battle.cpp, KO_HAPPOKUNAI), so the Lua ratio hook cannot scale it; with
    # renewal's 0.5 s delay it did about four times Sonic Blow's damage per
    # second, to everything around. A 3.5 s delay brings it to about half of
    # the Kagerou's single-target damage per target, the area rule the third
    # classes follow.
    # 16th Night halves the cast time (and adds MATK). Renewal has a fixed cast it cannot touch;
    # pre-renewal has none, so here it doubles a magic build's damage for as long as it lasts, and
    # at 90 s every 60 s it always lasts: a charged Ice Spear measured 14,162 dmg/s under it,
    # 7,326 without, a Warlock 4,050. Here it is a burst, 30 seconds every 3 minutes, like the
    # Rune Knight's Giant Growth.
    SKILL_OVERRIDES={"KO_HAPPOKUNAI": {"AfterCastActDelay": "3500"},
                     "KO_IZAYOI": {"Duration1": 30000, "Cooldown": "180000"}},
    # Pre-renewal has no fixed cast time and DEX shortens every cast to
    # nothing at 150; 75% of renewal's fixed cast becomes after-cast delay,
    # which DEX does not touch, and the rest is added to the cast time. Skills
    # with a 10 s+ cooldown keep it all as cast time (Izayoi halves it).
    FIXED_CAST_TO_DELAY=0.75,
    WEAPON_KINDS={
        "huuma":  dict(type="Weapon", sub="Huuma",  loc=["Both_Hand"],  label="Huuma Shuriken", unid="Huuma Shuriken"),
        "dagger": dict(type="Weapon", sub="Dagger", loc=["Right_Hand"], label="Dagger",         unid="Dagger"),
    },
    ITEMS_ABOUT="The Kagerou's and Oboro's gear, from kagerou_oboro/equipment.csv.",
    CSV_DIR="kagerou_oboro",
    # Illusion - Shadow summons this clone, which pre-renewal's mob_db lacks. The skill sets its
    # HP (3000 + 3000 a level); it does not attack. Renewal's Defense 100 takes about 18% off a
    # hit; pre-renewal's Defense is a percentage.
    MOBS_FROM_RENEWAL={"KO_KAGE": {
        "Level": (99, "renewal's is 140; 99, the pre-renewal cap, so monsters hit it as they would a player"),
        "Defense": (18, "renewal's 100 takes about 18% off a hit; pre-renewal's Defense is that percentage"),
    }},
)

rebellion = ec.config(
    __file__, MAX_BASE_LEVEL=175, BASE_EXP_ABOVE=base_exp_above, MAX_STATS=150, JOB_EXP_TOTAL=JOB_EXP_TOTAL,
    MOD_NAME="expanded-classes",
    JOBS=("Rebellion",),
    ITEM_JOB="Rebellion",             # the item_db Jobs: key (EAJ_REBELLION)
    BASE="Gunslinger",
    SKILL_PREFIX="RL_",
    # Rebellion sits a little below a transcendent class. Pre-renewal's Sniper
    # gets the Hunter HP table times 1.25; Rebellion gets it times 1.1. SP
    # follows the Gunslinger's table.
    HP_FROM="Sniper", HP_SCALE=1.10,
    SP_FROM="Gunslinger", SP_SCALE=1.10,
    EXP_FROM="Sniper",
    # Renewal's job bonuses come to +37 by job 60. These three more make +40,
    # five below a transcendent class's +45.
    EXTRA_BONUS=[(56, "Dex"), (58, "Agi"), (60, "Luk")],
    BONUS_TOTAL=40,
    MAX_JOB_LEVEL=60,
    # Renewal's skills consume these, and pre-renewal's item tables do not
    # have them. Sanctified_Bullet and Silver_Bullet_ are bullets Platinum
    # Alter names as required equipment; one missing item makes rAthena reject
    # the whole entry.
    NEW_FROM_RENEWAL=["Full_Metal_Jacket", "Shooting_Mine", "Dragon_Tail_Missile", "Slug_Bullet",
                      "Sanctified_Bullet", "Silver_Bullet_"],
    # Pre-renewal has no fixed cast time and DEX shortens every cast to
    # nothing at 150; 75% of renewal's fixed cast becomes after-cast delay,
    # which DEX does not touch, and the rest is added to the cast time.
    FIXED_CAST_TO_DELAY=0.75,
    WEAPON_KINDS={
        "revolver": dict(type="Weapon", sub="Revolver", loc=["Right_Hand"], label="Revolver", unid="Gun"),
        "rifle":    dict(type="Weapon", sub="Rifle",    loc=["Both_Hand"],  label="Rifle", unid="Gun"),
        "gatling":  dict(type="Weapon", sub="Gatling",  loc=["Both_Hand"],  label="Gatling Gun", unid="Gun"),
        "shotgun":  dict(type="Weapon", sub="Shotgun",  loc=["Both_Hand"],  label="Shotgun", unid="Gun"),
        "grenade":  dict(type="Weapon", sub="Grenade",  loc=["Both_Hand"],  label="Grenade Launcher", unid="Gun"),
    },
    ITEMS_ABOUT="The Rebellion's gear, from rebellion/equipment.csv.",
    CSV_DIR="rebellion",
)

star_emperor = ec.config(
    __file__, MAX_BASE_LEVEL=175, BASE_EXP_ABOVE=base_exp_above, MAX_STATS=150, JOB_EXP_TOTAL=JOB_EXP_TOTAL,
    # Purify has no code in rAthena in either era (owner, 2026-10-18).
    TREE_LEAVE_OUT=["SJ_PURIFY"],
    MOD_NAME="expanded-classes",
    # Star_Emperor2 is the Union (SG_FUSION) form, with its own tree.
    JOBS=("Star_Emperor", "Star_Emperor2"),
    BASE="Star_Gladiator",
    SKILL_PREFIX="SJ_",
    # A little below a transcendent class: a transcendent class gets its
    # second class's HP table times 1.25 (its upper flag); this gets the Star
    # Gladiator's times 1.1.
    HP_FROM="Star_Gladiator", HP_SCALE=1.10,
    SP_FROM="Star_Gladiator", SP_SCALE=1.10,
    EXP_FROM="Sniper",                # the transcendent base and job EXP tables
    # Renewal's bonuses come to +43 by job 70; its last three are dropped for
    # +40, five below a transcendent class's +45.
    BONUS_TOTAL=40,
    MAX_JOB_LEVEL=70,
    # The equipment is for Star Emperors only: a Star Gladiator's Jobs: key,
    # and Classes: Third, which a Star Gladiator is not.
    EQUIP_JOBS=["StarGladiator"], EQUIP_CLASSES=["Third"],
    # Pre-renewal has no fixed cast time and DEX shortens every cast to
    # nothing at 150; 75% of renewal's fixed cast becomes after-cast delay,
    # which DEX does not touch, and the rest is added to the cast time.
    FIXED_CAST_TO_DELAY=0.75,
    WEAPON_KINDS={
        "book": dict(type="Weapon", sub="Book", loc=["Right_Hand"], label="Book", unid="Book"),
    },
    ITEMS_ABOUT="The Star Emperor's gear, from star_emperor/equipment.csv.",
    CSV_DIR="star_emperor",
)

soul_reaper = ec.config(
    __file__, MAX_BASE_LEVEL=175, BASE_EXP_ABOVE=base_exp_above, MAX_STATS=150, JOB_EXP_TOTAL=JOB_EXP_TOTAL,
    # Soul Division's status is read nowhere in rAthena (owner, 2026-10-18).
    TREE_LEAVE_OUT=["SP_SOULDIVISION"],
    MOD_NAME="expanded-classes",
    JOBS=("Soul_Reaper",),
    BASE="Soul_Linker",
    SKILL_PREFIX="SP_",
    # A little below a transcendent class: a transcendent class gets its
    # second class's HP table times 1.25 (its upper flag); this gets the Soul
    # Linker's times 1.1.
    HP_FROM="Soul_Linker", HP_SCALE=1.10,
    SP_FROM="Soul_Linker", SP_SCALE=1.10,
    EXP_FROM="Sniper",                # the transcendent base and job EXP tables
    # Renewal's bonuses come to +43 by job 70; its last three are dropped for
    # +40, five below a transcendent class's +45.
    BONUS_TOTAL=40,
    MAX_JOB_LEVEL=70,
    # The equipment is for Soul Reapers only: a Soul Linker's Jobs: key, and
    # Classes: Third, which a Soul Linker is not.
    EQUIP_JOBS=["SoulLinker"], EQUIP_CLASSES=["Third"],
    # Pre-renewal has no fixed cast time and DEX shortens every cast to
    # nothing at 150; 75% of renewal's fixed cast becomes after-cast delay,
    # which DEX does not touch, and the rest is added to the cast time.
    FIXED_CAST_TO_DELAY=0.75,
    WEAPON_KINDS={
        "staff": dict(type="Weapon", sub="Staff", loc=["Right_Hand"], label="Staff", unid="Rod"),
    },
    ITEMS_ABOUT="The Soul Reaper's gear, from soul_reaper/equipment.csv.",
    CSV_DIR="soul_reaper",
)

# The Expanded Super Novice: the Super Novice's advancement (base 99, job 99). Its tree is
# renewal's: the Super Novice's skills, a share of the second classes', and two passives of its own.
super_novice = ec.config(
    __file__, MAX_BASE_LEVEL=175, BASE_EXP_ABOVE=base_exp_above, MAX_STATS=150, JOB_EXP_TOTAL=JOB_EXP_TOTAL,
    MOD_NAME="expanded-classes",
    JOBS=("Super_Novice_E",),
    BASE="Supernovice", ASPD_FROM="Super_Novice",   # rAthena's two spellings of the job
    # Its two own skills, passives pre-renewal's skill_db only has stubs of (one level), and Help
    # Angel, a stub there too, with the status it starts.
    SKILL_PREFIX=("NV_BREAKTHROUGH", "NV_TRANSCENDENCE", "NV_HELPANGEL"),
    STATUSES_FROM_RENEWAL=["HelpAngel"],
    # A little below a transcendent class, like the other advancements: the
    # Super Novice's tables times 1.1.
    HP_FROM="Supernovice", HP_SCALE=1.10,
    SP_FROM="Supernovice", SP_SCALE=1.10,
    EXP_FROM="Sniper",                # the transcendent base and job EXP tables
    # Renewal's bonuses come to +44 by job 70; its last four are dropped for
    # +40, five below a transcendent class's +45.
    BONUS_TOTAL=40,
    MAX_JOB_LEVEL=70,
    # The equipment is for the Expanded Super Novice only: the Super Novice's
    # Jobs: key, and Classes: Third, which a Super Novice is not.
    EQUIP_JOBS=["SuperNovice"], EQUIP_CLASSES=["Third"],
    WEAPON_KINDS={
        "dagger": dict(type="Weapon", sub="Dagger", loc=["Right_Hand"], label="Dagger", unid="Dagger"),
    },
    ITEMS_ABOUT="The Expanded Super Novice's gear, from super_novice/equipment.csv.",
    CSV_DIR="super_novice",
)

# Two mods from one build: the third classes, and the expanded classes. Both need
# level175-core (the soft cap and the level rule, mods/level175-core).
ec.run([guillotine_cross, shadow_chaser, arch_bishop, rune_knight, royal_guard, warlock,
        sura, ranger, minstrel, wanderer, genetic, mechanic, sorcerer])
ec.run([kagerou_oboro, rebellion, star_emperor, soul_reaper, super_novice])

# The two mods load side by side, and an entry one of them ships for a monster, an
# item or a skill the other also ships would replace it whole: they must not share any.
import re  # noqa: E402
MODS = Path(__file__).resolve().parents[1] / "mods"
for table, key in (("mob_db.yml", r"^  - Id: (\d+)"), ("item_db.yml", r"^  - Id: (\d+)"),
                   ("skill_db.yml", r"^    Name: (\S+)"), ("status.yml", r"^  - Status: (\S+)")):
    keys = []
    for mod in ("transcendent-third-classes", "expanded-classes"):
        path = MODS / mod / "db" / table
        keys.append(set(re.findall(key, path.read_text(encoding="utf-8"), re.M)) if path.exists() else set())
    if keys[0] & keys[1]:
        sys.exit(f"build.py: both mods ship {table} entries for {', '.join(sorted(keys[0] & keys[1]))}")

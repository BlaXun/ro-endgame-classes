-- transcendent-third-classes: third-class skill damage, as upgrades of the transcendent classes.
-- Percent of each skill's own damage. Each factor was set by measurement at
-- 175/70 against the transcendent class at 99/70 with the same stats and
-- weapon: a class's own single-target skills at about 1.5 times its
-- transcendent class (or just above its kept skills, where those pass 1.5
-- times with the levels alone), a fighting class's area attacks at no more
-- than half of that per target, and every class's pack time within the limit
-- for packs of five. Warlock areas are held by the pack limit alone.
-- The measured tables are in README.md, class by class; the runs, rounds and
-- frozen records are in tools/transcendent-third-classes/level175/.
-- A factor sits on the skill id that deals the hit (WL_TETRAVORTEX_FIRE, not
-- WL_TETRAVORTEX). Base level counts in skill damage only up to 99: level_rule.lua.
local FACTOR = {
  WL_SOULEXPANSION      = 147,
  SR_TIGERCANNON        = 802,
  SR_GATEOFHELL         = 500,  -- 10 s cooldown; its HP/SP part is outside the factor: 0.53 -> 2.06x Occult Impaction
  GC_CROSSIMPACT        = 30,
  GC_ROLLINGCUTTER      = 19,
  GC_CROSSRIPPERSLASHER = 10,
  GC_COUNTERSLASH       = 30,
  GC_VENOMPRESSURE      = 40,
  SC_TRIANGLESHOT       = 17,
  SC_FATALMENACE        = 7,
  SC_FEINTBOMB          = 25,
  AB_ADORAMUS           = 5,
  AB_JUDEX              = 8,
  AB_DUPLELIGHT_MAGIC   = 50,
  RK_SONICWAVE          = 78,
  RK_HUNDREDSPEAR       = 351,
  RK_WINDCUTTER         = 5,
  RK_IGNITIONBREAK      = 40,
  RK_DRAGONBREATH       = 64,
  RK_DRAGONBREATH_WATER = 64,
  LG_BANISHINGPOINT     = 23,
  LG_OVERBRAND          = 6,
  LG_CANNONSPEAR        = 39,
  LG_EARTHDRIVE         = 38,
  LG_MOONSLASHER        = 62,
  LG_HESPERUSLIT        = 11,  -- one target in this server: 0.96 of Banishing Point, which stays the best
  WL_HELLINFERNO        = 48,
  WL_TETRAVORTEX_FIRE   = 47,
  WL_TETRAVORTEX_WATER  = 47,
  WL_TETRAVORTEX_WIND   = 47,
  WL_TETRAVORTEX_GROUND = 47,
  WL_CRIMSONROCK        = 47,
  WL_JACKFROST          = 61,
  WL_FROSTMISTY         = 56,
  WL_CHAINLIGHTNING_ATK = 52,
  WL_COMET              = 85,
  SR_DRAGONCOMBO        = 98,
  SR_KNUCKLEARROW       = 206,
  SR_EARTHSHAKER        = 32,
  SR_SKYNETBLOW         = 12,
  SR_RAMPAGEBLASTER     = 250, -- a pack of five 1.28x Knuckle Arrow one by one; 0.22 of it a target
  SR_HOWLINGOFLION      = 250, -- a pack 1.22x Knuckle Arrow one by one; 0.20 a target
  SR_RIDEINLIGHTNING    = 10,
  RA_AIMEDBOLT          = 102,
  RA_WUGSTRIKE          = 27,
  RA_ARROWSTORM         = 47,
  RA_CLUSTERBOMB        = 70,
  RA_FIRINGTRAP         = 8,   -- its weapon part; the DEX/INT part and the burn are out of reach
  WM_REVERBERATION      = 25,
  WM_METALICSOUND       = 48,
  WM_SEVERE_RAINSTORM_MELEE = 26,
  WM_GREAT_ECHO         = 32,
  GN_CART_TORNADO       = 9,
  GN_CARTCANNON         = 55,   -- it splashes over 7x7: an area skill
  GN_SPORE_EXPLOSION    = 68,
  GN_CRAZYWEED_ATK      = 38,
  NC_POWERSWING         = 120,
  NC_BOOSTKNUCKLE       = 97,
  NC_VULCANARM          = 170,
  NC_FLAMELAUNCHER      = 80,
  NC_ARMSCANNON         = 48,   -- it splashes over 5x5: an area skill
  SO_PSYCHIC_WAVE       = 13,
  SO_POISON_BUSTER      = 25,
  SO_CLOUD_KILL         = 16,
  SO_VARETYR_SPEAR      = 98,
  SO_DIAMONDDUST        = 48,   -- area: 0.94 -> 0.49 of Varetyr Spear a target
  SO_EARTHGRAVE         = 44,   -- area: 1.03 -> 0.44 of Varetyr Spear a target
}

-- Windmill's ratio is base level + DEX. The base level counts up to 99 and no
-- further (lua/level_rule.lua has the rule; this term sits in the ratio,
-- where the level hook does not reach, so it is capped here).
local function windmill(c, stock)
  if c.caster.level > 99 then
    return stock - (c.caster.level - 99)
  end
  return stock
end

for name, percent in pairs(FACTOR) do
  skill(name, {
    ratio = function(c, stock)
      return stock * percent // 100
    end,
  })
end
if not FACTOR.SR_WINDMILL then
  skill("SR_WINDMILL", { ratio = windmill })
end

-- Spell Fist (Sorcerer): cast while a bolt is being cast, it cancels the
-- bolt and turns every auto-attack after it into that bolt's magic damage,
-- for 20 SP a hit, until the SP or the three minutes run out. In renewal
-- that was about 7,300 a second here, three times a High Wizard's
-- amplified Jupitel Thunder. The hit is computed through the bolt's own
-- skill, so the bolt is scaled only for a Sorcerer under Spell Fist; a
-- Wizard's or a Sorcerer's ordinary bolt is untouched.
local SORCERER_T = 4074
local SPELLFIST_KEPT = 17   -- percent of the bolt a Spell Fist hit keeps

for _, name in ipairs({ "MG_FIREBOLT", "MG_COLDBOLT", "MG_LIGHTNINGBOLT", "WZ_EARTHSPIKE" }) do
  skill(name, {
    ratio = function(c, stock)
      if c.caster.job == SORCERER_T and c.caster:has_status("SC_SPELLFIST") then
        return stock * SPELLFIST_KEPT // 100
      end
      return stock
    end,
  })
end

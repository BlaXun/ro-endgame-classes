-- transcendent-third-classes: skill output does not grow with level 175.
-- The rule (owner, 2026-10-11): the base level counts up to 99 and no further;
-- a character at or below 99 is untouched; the job level is left alone (its
-- cap stays 70, or 60). Bonuses beyond that belong on cards, buffs and gear.
-- Needs a server with the level hook (skill_lua.hpp); the skills are the ones
-- whose formulas read the base level outside the skill ratio.
local CLASSIC_LEVEL = 99

local CAPPED = {
  -- third classes and expanded advancements
  "RK_DRAGONBREATH", "RK_DRAGONBREATH_WATER", "RK_ENCHANTBLADE",
  "NC_SELFDESTRUCTION", "SR_GATEOFHELL", "SR_CRESCENTELBOW",
  "AB_RENOVATIO", "AB_HIGHNESSHEAL", "LG_EXEEDBREAK",
  "OB_ZANGETSU", "KO_JYUMONJIKIRI", "SJ_GRAVITYCONTROL",
  -- what these skills give, not their damage: Prestige's DEF and magic evasion, Freezing
  -- Spell's capacity, Deep Sleep Lullaby's chance (owner, 2026-10-18)
  "LG_PRESTIGE", "WL_FREEZE_SP", "WM_LULLABY_DEEPSLEEP",
  -- kept from earlier jobs (AL_HEAL also covers Coluceo Heal)
  "AL_HEAL", "AL_DEMONBANE", "PR_TURNUNDEAD", "SL_SMA", "TK_JUMPKICK",
  "SG_SUN_ANGER", "SG_MOON_ANGER", "SG_STAR_ANGER",
}

for _, name in ipairs(CAPPED) do
  skill(name, {
    level = function(c, stock)
      return math.min(stock, CLASSIC_LEVEL)
    end,
  })
end

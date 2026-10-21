-- transcendent-third-classes: the soft cap for base stats.
-- Third classes and the expanded advancements raise base stats to 150
-- (db/job_stats.yml). Above 99 a point counts for a third (150 counts as 116),
-- and base DEX above 99 does not shorten cast time at all: instant cast needs
-- the same DEX from job, gear and buffs as at level 99. A character whose base
-- stats are 99 or less computes exactly as without the mod.
-- Needs a server with the player hooks (skill_lua.hpp).
local CAP = 99
local DIVISOR = 3

local function counted(value)
  if value <= CAP then
    return value
  end
  return CAP + (value - CAP) // DIVISOR
end

player({
  base_stat = function(c, stock)
    return counted(stock)
  end,
  cast_dex = function(c, stock)
    -- what base DEX above the cap adds comes off again: it gives no cast speed
    return stock - (counted(c.caster.base_dex) - math.min(c.caster.base_dex, CAP))
  end,
})

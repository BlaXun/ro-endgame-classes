-- transcendent-third-classes: INT invested past 99 pays into healing.
-- Above 99 a base stat counts for a third (the soft cap), and a heal reads the
-- base level only up to 99, so a level-175 Arch Bishop with INT 150 healed
-- 8 % more than a High Priest at 99 while the HP it has to fill tripled.
-- For the Arch Bishop every point of base INT above 99 adds PER_POINT percent
-- to what Heal and Highness Heal restore (Coluceo Heal: coluceo_heal.lua). At
-- INT 99 or below nothing changes, so the class heals as its High Priest did
-- on the day it changes. No level is read. (Owner, 2026-10-11.)
-- Needs a server whose hooks carry c.caster.base_int (skill_lua.hpp).
local ARCH_BISHOP = 4063
local PER_POINT = 1

-- Highness Heal's own factor on top, in percent of what the server computes
-- (3.2 times the Heal base at level 5). 100 until phase 4 sets it against
-- the fights: the aim is the High Priest's share of the tank's HP a second.
local HIGHNESS = 100

local function invested(c)
  if c.caster.job ~= ARCH_BISHOP then
    return 0
  end
  local over = (c.caster.base_int or 0) - 99
  if over <= 0 then
    return 0
  end
  return over * PER_POINT
end

skill("AL_HEAL", {
  heal = function(c, stock)
    return stock * (100 + invested(c)) // 100
  end,
})

skill("AB_HIGHNESSHEAL", {
  heal = function(c, stock)
    return stock * (100 + invested(c)) // 100 * HIGHNESS // 100
  end,
})

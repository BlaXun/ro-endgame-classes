-- transcendent-third-classes: Coluceo Heal heals the party for a share of the
-- caster's own Heal, by its level, and has no bonus per party member.
-- (Owner, 2026-10-11: too strong as renewal has it. The shares are his choice,
-- not measured.) Needs a server with the heal hook (skill_lua.hpp).
local SHARE = { 70, 85, 100 }   -- percent of a normal Heal, by Coluceo Heal level

-- The caster's normal Heal includes what its INT past 99 adds (heal_int.lua).
local ARCH_BISHOP = 4063
local PER_POINT = 1

skill("AB_CHEAL", {
  heal = function(c, stock)
    local percent = SHARE[c.skill_lv] or 100
    local over = 0
    if c.caster.job == ARCH_BISHOP then
      over = math.max(0, (c.caster.base_int or 0) - 99) * PER_POINT
    end
    -- c.base is the Heal amount without the party bonus: building on it drops the bonus.
    return c.base * percent // 100 * (100 + over) // 100
  end,
})

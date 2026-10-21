-- transcendent-third-classes: renewal's flat DEF buffs, as pre-renewal DEF.
-- Renewal's DEF cuts damage by 1 - (4000 + DEF) / (4000 + 10 x DEF), so +100 DEF is a few
-- percent there. Pre-renewal's DEF is the percent itself (at most 99), so renewal's numbers
-- copied over make a near-immune tank. Each buff here gives what it gives in renewal at a
-- typical DEF of 300 (owner, 2026-10-18): Prestige up to +5, Echo Song up to +4, Remodel
-- Mainframe +3 to +6.
-- A server status's on_start runs before the server works out its values, so each hook
-- works out the stock DEF with the server's formula (status.cpp) and puts the converted
-- one in its place once the status is on.
local TYPICAL = 300

local function cut(def)
  return 9 * def / (4000 + 10 * def)
end

-- renewal's flat DEF bonus -> the pre-renewal DEF that cuts as much more
local function as_pre_renewal(bonus)
  if bonus <= 0 then return bonus end
  return math.floor(100 * (cut(TYPICAL + bonus) - cut(TYPICAL)) + 0.5)
end

-- val3: (15 x level + 10 x Defending Aura) x base level / 100, the level counted to 99 as
-- level175-core counts it
status("SC_PRESTIGE", {
  on_start = function(c)
    local u = c.target
    local stock = (15 * c.val1 + 10 * u:skill_lv("CR_DEFENDER")) * math.min(u.level, 99) // 100
    c:status_val("SC_PRESTIGE", 3, as_pre_renewal(stock))
  end,
})

-- val3: 6 x level + Lesson level + the target's job level / 4
status("SC_ECHOSONG", {
  on_start = function(c)
    local stock = 6 * c.val1 + c.val2 + (c.target.job_level or 50) // 4
    c:status_val("SC_ECHOSONG", 3, as_pre_renewal(stock))
  end,
})

-- Remodel Mainframe adds 20 + 20 x level DEF on a Madogear; this takes back the difference.
skill("NC_MAINFRAME", {
  bonus = function(c)
    if c.caster.riding ~= "mado" then return end
    local stock = 20 + 20 * c.skill_lv
    c:bonus("bDef", as_pre_renewal(stock) - stock)
  end,
})

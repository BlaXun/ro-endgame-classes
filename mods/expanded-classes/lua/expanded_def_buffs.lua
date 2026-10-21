-- expanded-classes: renewal's flat DEF and MDEF buffs, as pre-renewal DEF and MDEF.
-- Renewal's DEF cuts damage by 1 - (4000 + DEF) / (4000 + 10 x DEF) and its MDEF by
-- 1 - (1000 + MDEF) / (1000 + 10 x MDEF); pre-renewal's are the percent itself. Golem's Soul
-- gives what it gives in renewal at a typical DEF of 300 and MDEF of 100 (owner, 2026-10-18):
-- DEF +4 to +15, MDEF +4 to +8.
-- A server status's on_start runs before the server works out its values, so the hook
-- works out the stock ones with the server's formula (status.cpp) and puts the converted
-- ones in their place once the status is on.
local function cut(def, k)
  return 9 * def / (k + 10 * def)
end

local function as_pre_renewal(bonus, typical, k)
  if bonus <= 0 then return bonus end
  return math.floor(100 * (cut(typical + bonus, k) - cut(typical, k)) + 0.5)
end

-- val2: DEF, 60 x level; val3: MDEF, 15 + 5 x level
status("SC_SOULGOLEM", {
  on_start = function(c)
    c:status_val("SC_SOULGOLEM", 2, as_pre_renewal(60 * c.val1, 300, 4000))
    c:status_val("SC_SOULGOLEM", 3, as_pre_renewal(15 + 5 * c.val1, 100, 1000))
  end,
})

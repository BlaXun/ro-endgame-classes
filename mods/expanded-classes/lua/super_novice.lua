-- transcendent-third-classes: the Expanded Super Novice's share of second-class
-- skills.
--
-- Its tree is renewal's: the Super Novice's skills, a share of the second
-- classes' and two passives. The owner's rule (2026-10-13): it may use those
-- second-class skills and be strong with them, but not as strong as the class
-- they belong to; its edge is the size of its skill pool. So each is set to
-- about 75 % of what the third class that keeps the skill does with it at
-- 175/70 (Warlock, Sorcerer, Royal Guard), measured on the plain dummy without
-- Amplify Magic Power. Only an Expanded Super Novice is touched: a Wizard's
-- Jupitel Thunder is as it was.
--
-- Damage per second at 175/70 (runs:
-- tools/transcendent-third-classes/level175/super_novice_owners.json;
-- record: level175/README.md there), area spells to each target:
--
--                      its owner at 175   untouched   factor
--   Jupitel Thunder     Warlock 3754        4060        71
--   Holy Cross          Royal Guard 3210    3860        60
--   Storm Gust          Warlock 980         1033        73
--   Lord of Vermilion   Warlock 930         1165        62
--   Meteor Storm        Warlock 1894        2310        61
--   Heaven's Drive      Sorcerer 1130       1715        51
local EXPANDED = { [4190] = true, [4191] = true }   -- Super_Novice_E, Super_Baby_E
local FACTOR = {
  WZ_JUPITEL = 71,
  CR_HOLYCROSS = 60,
  WZ_STORMGUST = 73,
  WZ_VERMILION = 62,
  WZ_METEOR = 61,
  WZ_HEAVENDRIVE = 51,
}

for name, percent in pairs(FACTOR) do
  skill(name, { ratio = function(c, stock)
    if EXPANDED[c.caster.job] then return stock * percent // 100 end
    return stock
  end })
end

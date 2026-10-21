# Renewal endgame: classes

Mods for [Ragnarok Offline](https://github.com/Flux159/ragnarokoffline.app) that take pre-renewal characters past level 99, to 175, through renewal's third classes and expanded advancements. Each class is the step after the one you know, keeps every skill it had, and is balanced against pre-renewal rather than copied from renewal.

| Mod | What it is | Needs |
|---|---|---|
| [`level175-core`](mods/level175-core) | The rules every class past 99 shares: above 99 a base stat counts for a third, base DEX gives no cast speed, and skills that read the base level read at most 99. | — |
| [`transcendent-third-classes`](mods/transcendent-third-classes) | Renewal's 13 third classes, each the step after its transcendent class (99/70). They level to 175 and keep every earlier skill. | level175-core |
| [`expanded-classes`](mods/expanded-classes) | Kagerou/Oboro, Rebellion, Star Emperor, Soul Reaper and an Expanded Super Novice, each the next step of its finished class. | level175-core |

Pre-renewal only. The monsters, bosses, gear and cards for levels 99–175 are in [ro-endgame-world](https://github.com/BlaXun/ro-endgame-world).

## Installing

In the app: **Settings → Mods → Find Mods**, then install `level175-core` and the class mods you want. Each mod's README has its rules and numbers.

The class mods need **app 1.6.7** or later. Prestige, Freezing Spell and Deep Sleep Lullaby follow the level rule from the first release whose rAthena includes [rathena#66](https://github.com/Flux159/rathena/pull/66); before that they read the real level.

## How it's built

No table in these mods is written by hand. The scripts in [`tools/`](tools) generate them from rAthena's renewal tables and the CSVs beside them, and each has `--check`:

```sh
python3 tools/transcendent-third-classes/build.py --rathena ../rathena --check
python3 tools/expanded_class/expanded_class.py --rathena ../rathena --check
python3 tools/transcendent-third-classes/build_skill_descriptions.py --check
```

They read the rAthena commit and the translation from a [ragnarokoffline.app](https://github.com/Flux159/ragnarokoffline.app) checkout with its `vendor/` fetched: the one beside this repository, or wherever `RO_APP` points. `--rathena` is any rAthena checkout that has that commit. The balance rig and its specs are in [`tools/expanded_class/balance`](tools/expanded_class/balance).

[docs/RENEWAL_ENDGAME.md](docs/RENEWAL_ENDGAME.md) is the record of how all eight mods of the endgame were made, the rules they follow, and what is open. Read it before changing a number.

## Releasing

The three mods are released together and always carry the same version.

1. `python3 tools/package.py --set-version X.Y.Z`
2. Add a `## X.Y.Z` section to [CHANGELOG.md](CHANGELOG.md). It becomes the release notes players read.
3. Commit, then tag `vX.Y.Z` and push the tag.

The [release workflow](.github/workflows/release.yml) builds `<mod>-X.Y.Z.zip` for each mod from the tagged commit and publishes the release. It refuses a tag that doesn't match the mods' version. `python3 tools/package.py` builds the same zips into `dist/` locally.

## Licence

[GPL-3.0](LICENSE), like the app and rAthena, whose tables these are generated from.

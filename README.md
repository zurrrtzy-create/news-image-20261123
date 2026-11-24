# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/zurrrtzy-create/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/zurrrtzy-create/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A newspaper front page summing up the world news of Monday 23 November
2026: 30 stories, from Ukraine sinking the Russian corvette Merkury off
Benghazi with seven sea drones (Zelenskyy confirms Monday), to Nvidia
reinstating Jensen Huang as CEO with shares up 31% - the biggest gain since
2003 - and Iran vowing to use "all means" against the US naval blockade as
31 tankers mass beyond Hormuz; plus the Dymer toll rising to 11, NATO
meeting on the three Russian Kh-101 missiles in Poland, CrowdStrike buying
Zscaler for $43.9bn, the Kospi falling 3.31%, an UNRWA worker killed in
Jabalia, Ukraine hitting the Perm refinery 1,500 km inside Russia, and 18
more stories on a numbered world map - with a date check box that honestly
notes what was left out (COP31's collapse, the EU-Indonesia deal and
BepiColombo all belong to earlier days).

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png` (1024x1024, deterministic - two runs write identical
bytes). The image itself was rendered by `render.py` (Pillow + the real
EB Garamond and Playfair Display fonts in `fonts/`, SIL OFL). No network,
no randomness, no wall-clock time.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

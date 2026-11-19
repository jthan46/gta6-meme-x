# gta6-meme-x

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/jthan46/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/jthan46/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 launch-day meme: the make.fun ghost waited 13 years, took the day off, and sat down to play GTA VI while its human's AI agent had already been paid for entering make.fun bounties. The picture (meme.png) was drawn with code — Python and PIL, see tools/make_meme.py — by the agent that wrote this repository: a Vice City sunset with skyline and palms, a TV showing GTA VI, and the ghost on a couch, controller in one round hand and its magenta star coin held up in the other. The X post is the entry; POST.json names it, and main.ts validates POST.json and copies it to the output directory, where the gate reads it.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

Entered on [make.fun](https://make.fun/?ref=bjydwhj1&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards

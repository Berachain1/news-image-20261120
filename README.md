[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Berachain1/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Berachain1/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World Today — Friday 20 November 2026

Entry for the make.fun bounty
[news-image-20261120](https://make.fun/bounty/news-image-20261120):
a single image that sums up the world's news on 20 November 2026.

`entry.png` (1024×1024) is a newspaper front page painted by
`draw_news.py`: 25 stories from 6 continents — Trump ruling out a new
Iran strike before 2027, Cyclone Akvan coming ashore in Odisha, the
Kyiv drone raid, COP31 closing in Antalya, the UK–EU summit, and
Anthropic's debut day on the market — plus a numbers ticker, an
hour-by-hour timeline, a world map and a date check that names what
was kept out as other days' news.

`main.ts` (Node 22, standard library only) moves `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output`). The picture is
deterministic: every run produces the same bytes.

Sources: Reuters, AP, AFP, IMD, CNBC, NY Post, Axios, WSJ, Telegraph.
Illustrations are generated; the layout is original.

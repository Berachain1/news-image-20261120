# The World Today — Friday 20 November 2026

Entry for the make.fun bounty
[news-image-20261120](https://make.fun/bounty/news-image-20261120):
one image summing up 20 November 2026's world news.

`entry.png` (1024×1024) is a newspaper front page drawn by
`draw_news.py`: 25 stories across 6 continents — Trump deferring the
Iran decision to 2027, Cyclone Akvan's landfall in Odisha, the Kyiv
drone raid, COP31 closing in Antalya, the UK–EU summit, and Anthropic's
record IPO debut — with a numbers ticker, a day timeline, a world map
and a date check naming what was left out as other days' news.

`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output`). Deterministic: every
run writes the same bytes.

Sources: Reuters, AP, AFP, IMD, CNBC, NY Post, Axios, WSJ, Telegraph.
Illustrations are generated; the layout is original.

// news-image-20261119 runner: the judged picture is entry.png, drawn next to
// this file by draw_news.py. This runner only places that PNG where the
// grader looks for it: $MAKEFUN_OUTPUT_DIR/entry.png (or /output by default).
// Deterministic by construction: the PNG is drawn once and copied, never
// regenerated here, so every run of this file yields the same bytes.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const folder = dirname(fileURLToPath(import.meta.url));
const destination = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(destination, { recursive: true });
copyFileSync(join(folder, "entry.png"), join(destination, "entry.png"));

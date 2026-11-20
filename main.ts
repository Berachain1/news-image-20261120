// Runner for the 20 November 2026 news-image entry.
//
// The judged picture is entry.png, drawn beside this file by draw_news.py.
// All this runner does is place that PNG where the grader reads it:
// $MAKEFUN_OUTPUT_DIR/entry.png, or /output when that is unset.
// The PNG is produced once and copied byte for byte, so repeated runs
// of this file always hand the grader the same picture.

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const here = import.meta.dirname;
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(here, "entry.png");
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`entry.png -> ${target} (${statSync(target).size} bytes)`);

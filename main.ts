// news-image-20261123 entry (Node 22, standard library only).
// The image is the entry.png beside this file; the program copies it to
// /output/entry.png. The image itself was drawn by draw.py in this repo
// (deterministic PIL render of Monday 23 November 2026's news).
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = new URL("./entry.png", import.meta.url);
copyFileSync(src, join(outDir, "entry.png"));

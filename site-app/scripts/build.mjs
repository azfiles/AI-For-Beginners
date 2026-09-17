import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const courseAssets = resolve(root, process.env.COURSE_ASSETS_DIR || "../site-dist");
const output = resolve(root, process.env.OUTPUT_DIR || "../site-app-dist");

await rm(output, { recursive: true, force: true });
await mkdir(resolve(output, "server"), { recursive: true });
await mkdir(resolve(output, ".openai"), { recursive: true });
await cp(courseAssets, resolve(output, "client"), { recursive: true });
await cp(resolve(root, "worker/index.js"), resolve(output, "server/index.js"));

const hosting = JSON.parse(await readFile(resolve(root, ".openai/hosting.json"), "utf8"));
await writeFile(resolve(output, ".openai/hosting.json"), `${JSON.stringify(hosting, null, 2)}\n`);
await cp(resolve(root, "drizzle"), resolve(output, ".openai/drizzle"), { recursive: true });

console.log("Built Site worker, course assets, and D1 migrations.");

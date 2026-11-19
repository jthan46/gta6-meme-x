// Entry program for the gta6-meme-x-01 bounty (Node 22, standard library
// only). The entry itself is a post on X; this repository's one job is to
// hand the post's address to the grader. POST.json at the repository root
// holds that address, so this program checks that POST.json is well formed
// and then copies it, byte for byte, into the output directory.
//
// Directories come from the environment, as the grader sets them:
//   MAKEFUN_BOT_DIR    the repository (default /bot)
//   MAKEFUN_OUTPUT_DIR where POST.json goes (default /output)
// The program touches nothing outside those two places, uses no network
// and no clock, and writes the same bytes on every run.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const repoDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const postPath = join(repoDir, "POST.json");

// The shape of an X post address: https://x.com/<handle>/status/<id>, or
// the same on twitter.com, with an optional www. or mobile. prefix. The
// handle is 1 to 15 letters, digits or underscores (the characters X
// allows), the id is digits only, and the address ends there: no query or
// fragment, so the file names one post and nothing else.
const POST_ADDRESS =
  /^https:\/\/(?:www\.|mobile\.)?(?:x\.com|twitter\.com)\/[A-Za-z0-9_]{1,15}\/status\/\d+$/;

// The gate reads POST.json as an object of at most 16384 bytes; hold the
// file to the same cap here so an oversized file fails at home first.
const MAX_POST_BYTES = 16384;

function stop(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

// Read POST.json. A missing or unreadable file ends the run: there is no
// address to hand over. The bytes are kept as a buffer so the size guard
// below measures the file itself, not its decoded text.
let bytes: Buffer;
try {
  bytes = readFileSync(postPath);
} catch {
  stop(`POST.json could not be read at ${postPath}`);
}
if (bytes.byteLength > MAX_POST_BYTES) {
  stop(`POST.json is ${bytes.byteLength} bytes; the limit is ${MAX_POST_BYTES}`);
}
const raw = bytes.toString("utf8");

// Parse it and pull out the url. Anything that is not a JSON object with a
// string url is rejected here rather than passed on to the gate.
let address: unknown;
try {
  const data: unknown = JSON.parse(raw);
  if (typeof data !== "object" || data === null || Array.isArray(data)) {
    stop("POST.json must hold a JSON object");
  }
  address = (data as { url?: unknown }).url;
} catch (err) {
  if (err instanceof SyntaxError) {
    stop("POST.json is not valid JSON");
  }
  throw err;
}

if (typeof address !== "string" || !POST_ADDRESS.test(address)) {
  stop(
    'POST.json\'s "url" is not an X post address ' +
      "(want https://x.com/<handle>/status/<id>)",
  );
}

// Hand it over: create the output directory if needed, write the file
// exactly as it stands in the repository, then read it back and compare
// bytes, so a short or torn write is caught here instead of at the gate.
mkdirSync(outputDir, { recursive: true });
const targetPath = join(outputDir, "POST.json");
writeFileSync(targetPath, bytes);
if (!readFileSync(targetPath).equals(bytes)) {
  stop("the copied POST.json does not match the repository's");
}

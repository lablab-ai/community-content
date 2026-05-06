#!/usr/bin/env node
/**
 * Migrates all Cloudinary image URLs to Cloudflare Images.
 * Downloads the already-transformed image from Cloudinary, uploads to Cloudflare,
 * and records the old→new URL mapping in scripts/image-mapping.json.
 * Idempotent: skips URLs already present in the mapping file.
 *
 * Usage:
 *   CLOUDFLARE_IMAGES_TOKEN=<token> node scripts/migrate-cloudinary.mjs
 *   node scripts/migrate-cloudinary.mjs --dry-run   (scan only, no uploads)
 */

import { readFileSync, writeFileSync, existsSync, readdirSync, statSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

const ACCOUNT_ID = 'df2eef4c5a85afb0880466202079da1b';
const ACCOUNT_HASH = 'K11gkZF3xaVyYzFESMdWIQ';
const VARIANT = 'public';
const MAPPING_FILE = join(__dirname, 'image-mapping.json');
const DRY_RUN = process.argv.includes('--dry-run');

const API_TOKEN = process.env.CLOUDFLARE_IMAGES_TOKEN;
if (!API_TOKEN && !DRY_RUN) {
  console.error('Error: CLOUDFLARE_IMAGES_TOKEN env var is required.');
  process.exit(1);
}

// --- helpers ---

function walkMdx(dir, results = []) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) walkMdx(full, results);
    else if (entry.endsWith('.mdx') || entry.endsWith('.md')) results.push(full);
  }
  return results;
}

function extractCloudinaryUrls(files) {
  const set = new Set();
  const pattern = /https:\/\/res\.cloudinary\.com\/[^\s"')>]+/g;
  for (const file of files) {
    const content = readFileSync(file, 'utf8');
    for (const match of content.matchAll(pattern)) set.add(match[0]);
  }
  return [...set];
}

function extractFilename(url) {
  const last = url.split('/').pop().split('?')[0];
  return last || 'image.png';
}

async function downloadImage(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return Buffer.from(await res.arrayBuffer());
}

async function uploadToCloudflare(buffer, filename, sourceUrl) {
  const form = new FormData();
  form.append('file', new Blob([buffer]), filename);
  form.append('metadata', JSON.stringify({ sourceUrl }));

  const res = await fetch(
    `https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/images/v1`,
    { method: 'POST', headers: { Authorization: `Bearer ${API_TOKEN}` }, body: form }
  );
  const data = await res.json();
  if (!data.success) throw new Error(JSON.stringify(data.errors));
  return `https://imagedelivery.net/${ACCOUNT_HASH}/${data.result.id}/${VARIANT}`;
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// --- main ---

const files = [
  ...walkMdx(join(ROOT, 'blog/en')),
  ...walkMdx(join(ROOT, 'tutorials')),
];
const allUrls = extractCloudinaryUrls(files);
console.log(`Found ${allUrls.length} unique Cloudinary URLs across ${files.length} files\n`);

let mapping = {};
if (existsSync(MAPPING_FILE)) {
  mapping = JSON.parse(readFileSync(MAPPING_FILE, 'utf8'));
  console.log(`Loaded ${Object.keys(mapping).length} existing mappings (will skip these)\n`);
}

if (DRY_RUN) {
  const todo = allUrls.filter(u => !mapping[u]);
  console.log(`[dry-run] Would upload ${todo.length} images, skip ${allUrls.length - todo.length}`);
  console.log('\nSample URLs:');
  todo.slice(0, 5).forEach(u => console.log(' ', u));
  process.exit(0);
}

let uploaded = 0, skipped = 0, failed = 0;
const failures = [];

for (const url of allUrls) {
  if (mapping[url]) { skipped++; continue; }

  const filename = extractFilename(url);
  process.stdout.write(`[${uploaded + skipped + failed + 1}/${allUrls.length}] ${filename} ... `);

  try {
    const buffer = await downloadImage(url);
    const cfUrl = await uploadToCloudflare(buffer, filename, url);
    mapping[url] = cfUrl;
    uploaded++;
    console.log(`OK`);
    writeFileSync(MAPPING_FILE, JSON.stringify(mapping, null, 2));
    await sleep(150);
  } catch (err) {
    failed++;
    failures.push({ url, error: err.message });
    console.log(`FAILED: ${err.message}`);
  }
}

console.log(`\n✓ ${uploaded} uploaded  ·  ${skipped} skipped  ·  ${failed} failed`);
if (failures.length > 0) {
  console.log('\nFailed URLs:');
  failures.forEach(f => console.log(`  ${f.url}\n    → ${f.error}`));
}

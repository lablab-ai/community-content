#!/usr/bin/env node
/**
 * Applies the Cloudinary → Cloudflare URL mapping to all MDX/MD files.
 * Reads scripts/image-mapping.json and replaces every Cloudinary URL
 * in blog/en/ and tutorials/ with its Cloudflare Images equivalent.
 *
 * Usage:
 *   node scripts/apply-image-mapping.mjs             (writes changes)
 *   node scripts/apply-image-mapping.mjs --dry-run   (preview only)
 */

import { readFileSync, writeFileSync, readdirSync, statSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const MAPPING_FILE = join(__dirname, 'image-mapping.json');
const DRY_RUN = process.argv.includes('--dry-run');

if (!existsSync(MAPPING_FILE)) {
  console.error('image-mapping.json not found. Run migrate-cloudinary.mjs first.');
  process.exit(1);
}

const mapping = JSON.parse(readFileSync(MAPPING_FILE, 'utf8'));
const totalMapped = Object.keys(mapping).length;
console.log(`Loaded ${totalMapped} URL mappings\n`);

function walkMdx(dir, results = []) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) walkMdx(full, results);
    else if (entry.endsWith('.mdx') || entry.endsWith('.md')) results.push(full);
  }
  return results;
}

const files = [
  ...walkMdx(join(ROOT, 'blog/en')),
  ...walkMdx(join(ROOT, 'tutorials')),
];

let filesChanged = 0;
let totalReplacements = 0;

for (const file of files) {
  const original = readFileSync(file, 'utf8');
  let updated = original;
  let replacements = 0;

  for (const [cloudinaryUrl, cfUrl] of Object.entries(mapping)) {
    if (updated.includes(cloudinaryUrl)) {
      const count = (updated.split(cloudinaryUrl).length - 1);
      updated = updated.replaceAll(cloudinaryUrl, cfUrl);
      replacements += count;
    }
  }

  if (replacements > 0) {
    filesChanged++;
    totalReplacements += replacements;
    const relPath = file.replace(ROOT + '/', '');
    console.log(`${DRY_RUN ? '[dry-run] ' : ''}${relPath}: ${replacements} replacement(s)`);
    if (!DRY_RUN) writeFileSync(file, updated, 'utf8');
  }
}

console.log(`\n${DRY_RUN ? '[dry-run] ' : ''}✓ ${totalReplacements} replacements across ${filesChanged} files`);
if (DRY_RUN) console.log('Run without --dry-run to apply changes.');

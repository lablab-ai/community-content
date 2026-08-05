---
name: tutorial-gap-scan
description: Scan lablab's hackathon technology partners against published tutorials to find coverage gaps — partners with zero tutorial coverage, and partners with only stale (not-this-year) coverage. Use when you don't have a specific source or hackathon page yet and want to find what to write about next. Outputs a ranked gap list and hands off to content-ideate or hackathon-tutorial.
compatibility: Designed for Claude Code. Requires WebSearch/WebFetch. lablab.ai pages often return Cloudflare challenges to automated fetches — fall back to web search plus grepping this repo's tutorials/ and blog/en/ directories.
---

## When to use

Run this skill first when the ask is open-ended — "what should we write next," "find us a tutorial gap," "what partners don't we cover yet" — and there is no source, idea, or hackathon page already in hand.

Do NOT use this for a specific hackathon page already provided (use `hackathon-tutorial`) or a specific tweet/article/idea already in hand (use `content-ideate`). This skill's only job is finding the candidate; it does not generate titles, run the deep uniqueness check, or post to Notion — that's the next skill's job.

---

## Steps

### 1. Gather the partner list

Fetch `https://lablab.ai/ai-hackathons` for the hackathons in scope (default: current calendar year, or a range the user specifies).

If the direct fetch is blocked (Cloudflare challenge/403 — common), fall back to:
- Web search: `site:lablab.ai/event [year] hackathon`
- Cross-check against any prior gap-scan results already in memory

For each hackathon, extract the technology partner(s) sponsoring it.

### 2. Gather existing coverage

Fetch `https://lablab.ai/ai-tutorials`. If blocked, grep this repo instead:
- `tutorials/` and `blog/en/` — search actual title/description/body content for each partner name, not just filenames. A partner can be mentioned in passing without a dedicated tutorial; only count real coverage.
- For every match, note the publish year (from the filename date, frontmatter, or `git log` on the file).

### 3. Cross-reference and classify

For each partner technology:
- **Net-new gap** — zero tutorial coverage anywhere
- **Stale coverage** — tutorial(s) exist, but none published in the current calendar year
- **Covered** — a tutorial published this year exists → drop from the list

### 4. Filter for feasibility

Before presenting, exclude partners that cannot actually be tutorial subjects, and say why:
- Not yet publicly released — no public API/SDK access
- Physical/hardware-bound — requires owning specific hardware with no cloud/simulator path

Flag these explicitly rather than silently dropping them — a feasibility call can be wrong (e.g., a simulator or waitlist access might exist). Let the user confirm or override.

### 5. Rank by urgency

1. Partner has an active or upcoming hackathon (within ~2 weeks) — a gap-filling tutorial published during a live hackathon is far more valuable than one published after
2. Net-new gaps rank above stale coverage
3. Within a tier, rank by how many hackathons have featured that partner — more exposure means more reader demand

### 6. Present the ranked list

```
NET-NEW GAPS (no tutorial coverage)
1. [Partner] — featured in [N] hackathons, most recent [date]. [urgency note if any]
2. ...

STALE COVERAGE (tutorial exists, nothing published this year)
1. [Partner] — [N] tutorials, most recent [year]. [urgency note if any]
2. ...

EXCLUDED (feasibility)
- [Partner] — [reason: unreleased / hardware-bound / other]
```

Wait for the user to pick one or more partners. Do not proceed to research or drafting concepts yourself.

### 7. Hand off

- Partner tied to a specific live/upcoming hackathon page → hand off to `hackathon-tutorial` with that hackathon's URL
- Otherwise → hand off to `content-ideate`, passing the partner name and gap classification (net-new vs stale) as the source/context

## Gotchas

- lablab.ai pages frequently return Cloudflare challenges to automated fetches — don't stall on a 403, go straight to the WebSearch + repo-grep fallback
- "Stale coverage" is judged against the current calendar year, not a rolling 12 months — recompute the cutoff each time this skill runs, don't reuse a hardcoded year
- A partner appearing in multiple hackathons is listed once; the hackathon count is only an urgency/demand signal, not a separate entry

---
name: content-ideate
description: Generate an article or tutorial concept from a source (tweet, article, or raw idea). Use when you have a piece of content or an idea and want to turn it into a lablab content concept — outputs a working title and brief ready to hand off to content-start.
compatibility: Designed for Claude Code. Requires WebSearch or Brave Search MCP for uniqueness check, WebFetch for URL sources, and uv for the Notion script.
---

## Steps

### 1. Parse the source

Accept a tweet URL/text, article URL/text, or raw idea. Fetch URLs. Extract the core claim, tools mentioned, and implied audience.

### 2. Identify the angle

- **Tutorial** if there's something to build; **Article** if it's a trend, comparison, or opinion.
- Pick one reader level: Beginner / Intermediate / Advanced.

### 3. Quick uniqueness check

- `site:lablab.ai [topic]` — already covered? Suggest a fresher angle.
- One broader search (Medium, dev.to, Hashnode) — note the gap we're filling.

### 4. Generate titles

Produce 3 options — beginner-friendly, outcome-focused, comparison/contrast. Avoid: "A Guide to X", "Everything About X", "The Ultimate X Tutorial".

### 5. Present the brief

```
Type: [Article / Tutorial]
Recommended title: [title]
Alternative titles:
  - [option 2]
  - [option 3]

Hook: [one sentence — what makes this different from what already exists]
Target reader: [Beginner / Intermediate / Advanced]
Angle: [2-3 sentences — what the piece covers, what the reader walks away with]

Suggested file path: [blog/en/slug.mdx or tutorials/en/slug/article.mdx]
```

Wait for the user to confirm title and angle.

### 6. Post to Notion

Once confirmed, run:

```bash
uv run scripts/post_to_notion.py \
  --title "confirmed title" \
  --type "Article" \
  --hook "hook sentence" \
  --reader "Beginner" \
  --angle "angle summary" \
  --path "suggested/path.mdx"
```

Share the returned Notion URL with the user.

## Gotchas

- If the script exits with a 404, the database isn't shared with the integration yet. Ask the user to open the database in Notion → "..." → "Add connections" → "Claude Automation".
- `--type` must be exactly `Article` or `Tutorial`; `--reader` must be `Beginner`, `Intermediate`, or `Advanced`.

## Hand off

Tell the user to run `content-start` with the confirmed title to begin the full pre-writing protocol.

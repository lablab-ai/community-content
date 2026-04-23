---
name: content-ideate
description: Generate an article or tutorial concept from a source (tweet, article, or raw idea). Use when you have a piece of content or an idea and want to turn it into a lablab content concept — outputs a working title and brief ready to hand off to content-start.
compatibility: Designed for Claude Code. Requires WebSearch or Brave Search MCP for uniqueness check, WebFetch for URL sources, and python3 with requests installed.
---

## Steps

### 1. Parse the source

Accept a tweet URL/text, article URL/text, or raw idea. Fetch URLs. Extract the core claim, tools mentioned, and implied audience.

### 2. Identify the angle

- **Tutorial** if there's something to build; **Article** if it's a trend, comparison, or opinion.
- Pick one reader level: Beginner / Intermediate / Advanced.

### 3. Deep uniqueness check

The goal is to find an angle **no one has written yet**. Run all of these:

1. `site:lablab.ai [topic]` — if covered, the angle must be meaningfully different
2. `[topic] tutorial` — broad web search, scan top 10 results across all platforms
3. `[topic] site:medium.com OR site:dev.to OR site:hashnode.com OR site:towardsdatascience.com`
4. `[topic] site:youtube.com` — video coverage signals a saturated angle; find what they missed
5. `[specific tool/API combo] tutorial [current year]` — check for recency gaps

After all searches, answer:
- What exact angles already exist? (list titles + platforms)
- What angle is **missing entirely** — a combination of tools, a use case, or a reader level no one has addressed?
- Is there a recency gap — old tutorials on a rapidly-changing tool?

Only proceed with an angle that passes: **"I could not find this written anywhere."** If everything is covered, reframe around the gap rather than retreading existing ground.

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
python3 scripts/post_to_notion.py \
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

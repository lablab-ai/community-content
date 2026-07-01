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

### 7. Create a design request for Damian

Immediately after posting to Notion, create a cover image request in the design database so Damian can start work in parallel.

**Design database ID:** `3485a26f46938097b6a9f4165323e8ce`
**Assigned by (Stephen Kimoi):** `2bed872b-594c-81d6-a2d4-0002487dc95b`
**Default due date:** 7 days from today

```bash
NOTION_TOKEN=$(grep NOTION_TOKEN /Users/steve/Lablab-AI/community-content/.agents/skills/.env | cut -d= -f2 | tr -d '"' | tr -d "'" | tr -d ' ')

curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  --data '{
    "parent": {"database_id": "3485a26f46938097b6a9f4165323e8ce"},
    "properties": {
      "Task name": {"title": [{"text": {"content": "<confirmed title>"}}]},
      "Status": {"status": {"name": "Ready for review"}},
      "Assigned by": {"people": [{"id": "2bed872b-594c-81d6-a2d4-0002487dc95b"}]},
      "Due date": {"date": {"start": "<YYYY-MM-DD>"}}
    },
    "children": [
      {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":"Type: <Article or Tutorial>"}}]}},
      {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":"Hook: <hook sentence>"}}]}},
      {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":"Angle: <2-3 sentence angle summary>"}}]}},
      {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":"Target reader: <Beginner / Intermediate / Advanced>"}}]}},
      {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":"Suggested file path: <path>"}}]}},
      {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":"Design notes: Cover image for lablab.ai article. Follow existing article cover style — clean, Lablab-branded, topic-relevant visual. Image will be uploaded to Cloudflare Images and added to the article frontmatter before publishing."}}]}}
    ]
  }'
```

Parse the `url` field from the response and share it with the user alongside the Notion content task URL.

If the API returns an error, report it clearly — do not silently skip this step.

## Gotchas

- If the post_to_notion script exits with a 404, the database isn't shared with the integration yet. Ask the user to open the database in Notion → "..." → "Add connections" → "Claude Automation".
- `--type` must be exactly `Article` or `Tutorial`; `--reader` must be `Beginner`, `Intermediate`, or `Advanced`.
- Valid status for the design database is `"Ready for review"` — do not use `"Not started"` or `"In Progress"`, they don't exist in that DB.

## Hand off

Tell the user to run `content-start` with the confirmed title to begin the full pre-writing protocol.

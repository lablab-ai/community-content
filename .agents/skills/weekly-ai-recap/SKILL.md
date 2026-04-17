---
name: weekly-ai-recap
description: Research, write, and publish the weekly "What happened in AI this week" article for Lablab. Run every Monday — searches for the past week's top AI news, writes a skimmable recap article, and produces a social post brief for Gosia/Soto. Updates the Notion task on completion.
compatibility: Designed for Claude Code. Requires Exa MCP or Brave Search MCP (WebSearch fallback), Cloudinary for images, and Notion token in ~/claude-workspace-automation/.env (NOTION_TOKEN).
---

## Steps

### 1. Confirm the publication date

Ask the user (if not already clear):
- What Monday is this for? (default: today's date)
- Any specific stories, launches, or topics to definitely include?

Derive:
- `WEEK_END` = publication date (the Monday)
- `WEEK_START` = 7 days prior (the previous Monday)
- `SLUG` = `this-week-in-ai-YYYY-MM-DD` (using the publication date)
- `FILE_PATH` = `blog/en/this-week-in-ai-YYYY-MM-DD.mdx`
- `BRANCH` = `add-this-week-in-ai-YYYY-MM-DD`

### 2. Create a feature branch

Per the git workflow in CLAUDE.md, all new content goes on a feature branch:

```bash
git checkout -b add-this-week-in-ai-YYYY-MM-DD
```

Never write directly to `main`.

### 3. Check Notion for the task

Fetch the matching task from DB `2cab4088-66ca-4d1f-aeb9-8fe29dafb470`:
- Use the workspace automation token from `~/claude-workspace-automation/.env` (`NOTION_TOKEN`)
- Filter: `Workspace = Lablab`, `Category = Content`, title contains "AI News Recap" or "AI recap"
- If found: read the Notes field for any pre-captured story ideas or instructions
- If not found: create a task using the `notion-task` global skill before continuing

### 4. Research — find the top AI news of the week

Search for major AI news from `WEEK_START` to `WEEK_END`. Run all available search tools in parallel:

**Priority queries (always run):**
- `"AI news this week" [WEEK_END date]`
- `new AI model release [month year]`
- `AI breakthrough announcement [month year]`
- `major AI company update [month year]`
- `AI funding round [month year]`

**Supplementary queries (run if time allows):**
- `OpenAI GPT announcement [month year]`
- `Anthropic Claude update [month year]`
- `Google Gemini news [month year]`
- `Meta AI [month year]`
- `open source AI model release [month year]`

**Curate:** Select the **5–8 most significant stories**. Prioritise:
1. New model releases or major version updates
2. Big-company announcements (OpenAI, Anthropic, Google, Meta, xAI, Mistral)
3. Genuine AI breakthroughs or research with real-world implications
4. Significant funding / acquisitions
5. Notable open-source releases

Discard: minor blog posts, opinion pieces, redundant coverage of the same story.

### 5. Write the article

Write to `blog/en/this-week-in-ai-YYYY-MM-DD.mdx`. The file must start with MDX frontmatter:

```mdx
---
title: "[Story 1], [Story 2], [Story 3]"
description: "[2-sentence SEO summary naming key companies and the month/year. No hype words.]"
image: "https://res.cloudinary.com/dygkv9gam/image/upload/v1/lablab-static/this-week-in-ai-cover.jpg"
authorUsername: "stevekimoi"
---
```

Then the article body:

```markdown
# [Story 1], [Story 2], [Story 3]

*This Week in AI — [Month Day–Day, Year]*

[2–3 sentence thematic intro. Capture the mood and the thread connecting this week's stories —
not a list of headlines, but a single observation about what the week meant. No "In this article..." openers.]

## Key Takeaways

- **[Company/topic]:** [1–2 sentences: what happened + the direct implication for builders or
  the industry. Write it as if explaining to a smart friend, not a press release.]
- **[Company/topic]:** [same]
- **[Company/topic]:** [same]
- [3–5 bullet points total — only the stories with a clear "so what"]

---

## [Thematic Section Title — groups 2–3 related stories, e.g. "The Open-Source Race" or "OpenAI vs. Everyone"]

### [Story Headline]
[2–3 sentences: what happened, why it matters, any concrete numbers. Source linked inline on
the most important claim. End with the implication — one sentence, no hedging.]

### [Story Headline]
[same]

---

## [Next Thematic Section]

### [Story Headline]
[same format]

### [Story Headline]
[same format]

---

## Quick Hits

- **[Company/topic]:** [One sentence. Source linked.]
- **[Company/topic]:** [One sentence. Source linked.]
- [4–6 bullet points for smaller stories that don't need a full breakdown]

---

*This Week in AI is published every Monday by the [Lablab](https://lablab.ai) team.*
```

**Writing rules:**
- **Intro:** 2–3 sentences that name the theme of the week, not a summary of every story. The reader should feel oriented before they've read a single headline.
- **Key Takeaways:** Implications, not just facts. Each bullet ends with what a developer or founder should *do* or *think* differently as a result.
- **Section titles:** Group stories by theme (e.g. "Meta Goes Closed-Source", "AI Meets the Real World") — never just "News" or "Updates"
- **Story write-ups:** 2–3 sentences, one inline source link on the key claim, end with the implication. No hanging "time will tell" sentences.
- **Quick Hits:** Stories that matter but don't need context — funding rounds, minor releases, policy moves, notable tools
- **Voice:** Direct and confident, like a smart colleague briefing you before a meeting. Not a journalist, not a hype merchant. Casual enough to be readable, precise enough to be trusted.
- **Banned words:** "revolutionary", "game-changing", "powerful", "cutting-edge", "groundbreaking", "exciting", "innovative"
- **Every factual claim has a source** — linked inline. No hallucinated stats; if a number can't be verified, omit it.
- **Total word count:** 700–1,100 words. Skimmable but substantive.
- **SEO:** The intro and Key Takeaways naturally include the major company names and "AI news [month year]" — do not force it, let coverage drive it.

### 6. Produce the social post brief

After the article is drafted, create a separate brief for Gosia and Soto at the bottom of the article file under a `---` separator, or as a note to the user:

```
SOCIAL POST BRIEF — [publication date]

Format: Carousel (Instagram/LinkedIn)
Post on: Same day as article publication

Slide 1 — Cover: "What happened in AI this week 🧠" + date
Slide 2–[N] — One story per slide: bold headline + 1-sentence summary
Last slide — CTA: "Full breakdown at lablab.ai → link in bio"

Stories to cover (pick top 4–5 for carousel):
1. [Story 1 headline]
2. [Story 2 headline]
3. [Story 3 headline]
4. [Story 4 headline]
5. [Story 5 headline]

Tone: Clean, minimal, no buzzwords. Reference: @evolving.ai on Instagram.
Template: Soto to create reusable carousel template for this series.
```

### 7. Run publish-check

Before marking done, run the `publish-check` skill on the draft:
- Confirm no placeholders, no skeleton sections, no unverified stats
- Confirm MDX frontmatter is complete (title, description, image, authorUsername)
- Confirm word count is 700–1,100 words
- Confirm all source links are present

Fix any issues before continuing.

### 8. Update Notion

Once publish-check passes:
- Set Notion task Status → `In Progress` (article written, pending publication)
- Append to Notes: `Draft written. File: [FILE_PATH]. Branch: [BRANCH]. Social brief included. Date: [today].`

### 9. Hand off

Confirm to the user:
- [ ] Feature branch created: `[BRANCH]`
- [ ] Article draft written at `[FILE_PATH]`
- [ ] MDX frontmatter complete
- [ ] Social post brief produced
- [ ] Notion task updated to In Progress
- [ ] Publish-check passed

Next steps for the user:
1. Review the article and edit as needed
2. Share the social brief with Gosia + Soto
3. Open a PR from `[BRANCH]` → `main` targeting the lablab-ai/community-content upstream
4. After PR merges and article is live, run `publish-check` again and set Notion task → Done
5. Gosia posts the carousel same day

## Series tracking

This skill is designed to repeat every Monday for the 5-week experiment (Apr 14 – May 12, 2026).
After 5 editions, review performance data before committing to ongoing publication.

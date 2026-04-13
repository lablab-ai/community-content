---
name: content-start
description: Run the mandatory pre-writing research protocol before starting any Lablab article or tutorial. Use when about to write or draft a new article or tutorial — checks for duplicates, gathers sources, confirms the angle, and sets the Notion task to In Progress.
compatibility: Designed for Claude Code. Requires Exa MCP, Brave Search MCP (or WebSearch fallback), and Notion API token in ~/.claude/settings.local.json.
---

## Steps

### 1. Identify the piece

Ask the user (if not already provided):
- Is this an **article** or a **tutorial**?
- What is the working title or topic?
- Is there a Notion task already, or does one need to be created?

### 2. Check Notion for an existing brief

Fetch the Notion task from the Tasks & Action Items DB (`2cab4088-66ca-4d1f-aeb9-8fe29dafb470`):
- Filter: `Workspace = Lablab`, `Category = Content`, title matches the topic
- Read the Notes field for any brief, Slack context, angle, or contacts already captured
- Note the current Status — if `Not Started`, it will be set to `In Progress` at the end of this skill

### 3. Run the uniqueness check

Search for existing content using this order:

1. **Exa MCP** (`mcp__exa__*`) — semantic search for similar articles/tutorials
2. **Brave Search MCP** (`mcp__brave__*`) — keyword search
3. **Built-in WebSearch** — fallback if MCPs are unavailable

Run these queries:
- Exact topic title (e.g., `"AI-driven interactive charts with Claude"`)
- Broader topic (e.g., `"Claude API data visualization tutorial"`)
- Lablab-specific: `site:lablab.ai [topic]`

**Decision:**
- Near-identical piece exists on a major platform → flag to user. Angle must change before proceeding.
- Similar pieces exist but shallow or outdated → note the gap we're filling, proceed.
- Nothing close → proceed with confidence.

### 4. Gather sources

Search for:
- Official docs for all tools/APIs the piece will use
- Real-world examples and use cases
- Recent library/API release notes that affect the content
- Any stats or claims that need a live source (no hallucinated numbers)

### 5. Confirm the angle with the user

Present:
- What exists already and how we're different
- The proposed unique hook in one sentence
- Target reader level: beginner / intermediate / advanced
- Any code demos, repos, or partner links to include

Wait for user confirmation before proceeding to draft.

### 6. Set Notion task to In Progress

Update the Notion task status to `In Progress`.
If no task exists, create one now using the `notion-task` skill before continuing.

### 7. Hand off

Confirm the following are locked before writing begins:
- [ ] Angle confirmed
- [ ] Target reader level confirmed
- [ ] Sources gathered
- [ ] Notion task is `In Progress`
- [ ] File location decided: `articles/[slug].md` or `tutorials/[slug]/article.md`

## Content type reminders

**Articles** (`articles/[slug].md`):
- 800–1,500 words
- Lead with the insight, not the setup — no "In this article..." openers
- Clear point of view; practical takeaway at the end

**Tutorials** (`tutorials/[slug]/article.md`):
- 1,200–2,500 words
- Structure: Introduction → Prerequisites → Steps → Conclusion
- All code blocks complete and runnable — no `...` placeholders
- Each step doable in under 10 minutes for an intermediate developer

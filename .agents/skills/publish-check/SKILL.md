---
name: publish-check
description: Run the publishing checklist for a Lablab article or tutorial before marking it as Done. Use when a draft is complete and ready to be signed off — checks all sections are written, code blocks work, images use Cloudinary, and Notion task is updated.
compatibility: Designed for Claude Code. Requires Notion API token in ~/.claude/settings.local.json.
---

## Steps

### 1. Identify the piece

Ask the user (if not already clear):
- Article or tutorial?
- File path of the draft (e.g., `tutorials-and-articles/articles/monetize-llm-usdc-circle.md` or `tutorials-and-articles/tutorials/claude-interactive-charts/article.md`)
- Notion task title (to find and update it)

### 2. Read the draft

Read the full draft file.

### 3. Run the checklist

#### For both articles and tutorials:

- [ ] **No placeholders** — no TODOs, no `[insert X here]`, no `...` in code blocks
- [ ] **No skeleton sections** — every H2/H3 has real prose, not just a heading
- [ ] **Images use Cloudinary** — all image URLs are `https://res.cloudinary.com/dygkv9gam/image/upload/...` — no local paths, no hotlinked external images
- [ ] **No unverified stats** — any numbers or claims have a linked source in the text
- [ ] **No marketing language** — scan for: "powerful", "revolutionary", "cutting-edge", "game-changing"

#### For articles only:

- [ ] **800–1,500 words** — count and flag if outside range
- [ ] **No "In this article..." opener** — first sentence leads with the idea
- [ ] **Clear point of view** — the piece takes a stance, not just reports facts
- [ ] **Practical takeaway at the end** — not a generic "get started today"
- [ ] **At least one code snippet or concrete example** per technical claim
- [ ] **File saved as** `articles/[slug].md`

#### For tutorials only:

- [ ] **1,200–2,500 words** — count and flag if outside range
- [ ] **All code blocks are runnable** — no partial snippets; every block includes all imports
- [ ] **Language declared** on every fenced code block (` ```python `, ` ```typescript `, etc.)
- [ ] **Prerequisites section present** — tools, API keys, framework versions listed
- [ ] **`.env` format shown** (if needed) — with placeholder values, never real keys
- [ ] **Final output shown** — screenshot, terminal output, or demo of the working result
- [ ] **File saved in** `tutorials/[slug]/article.md`

### 4. Report results

List every checklist item with a pass/fail. For any failure:
- Quote the specific line or section that has the problem
- Suggest the fix

Do not mark the piece as done if any item fails.

### 5. Update Notion

Once all checklist items pass:
- Fetch the Notion task by title from DB `2cab4088-66ca-4d1f-aeb9-8fe29dafb470`
- Update Status → `Done`
- Add a note to the Notes field: `Draft complete. File: [path]. Checked: [today's date].`

### 6. Confirm

Report: "All checks passed. Notion task '[title]' set to Done."

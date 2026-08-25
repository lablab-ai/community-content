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

### 3. Run the humanizer pass

Run the `humanizer` skill on the full prose body (frontmatter, code blocks, YAML, and link targets stay untouched — content only):

- If `humanizer` appears in the Skill tool registry, invoke it directly in file mode on the draft.
- If it doesn't (a fresh plugin install doesn't show up until the next session), read `SKILL.md` directly instead of skipping the step — check `~/.claude/plugins/cache/humanizer/humanizer/*/SKILL.md` first; if that's not present, fetch `https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md` — and apply its rewrite process by hand.

Fix what the pass flags (em dashes used as parenthetical punctuation, filler phrases, forced triads, vague sourcing, chatbot artifacts, etc.) without changing any fact, number, name, date, or link. If a flagged pattern is actually the site's deliberate house style (e.g. this repo's consistent title-case section headings, or a recurring series sign-off), leave it and note why in the report rather than forcing a change for its own sake. It's fine for this step to find nothing to change — say so rather than editing for the sake of editing.

Sentence-level tells (dashes, curly quotes, filler words) are the easy half of this check and checking only those produces false confidence — a piece can pass every line-level pattern and still read as AI-written at the structural level. Read the whole draft once specifically for these before signing off:
- **Reflexive "moral of the story" tags** — a sentence at the end of a paragraph that explicitly states the takeaway ("The lesson stuck: ...", "That discipline is the only reason...", "a mistake that taught him to...") instead of trusting the reader to draw it from the facts already given. Cut these; the preceding facts should already carry the point.
- **Mystery-box narration** — withholding what happened for a sentence ("something happened that had nothing to do with his code") before revealing it in the next. State it directly.
- **Redundant recap conclusions** — a closing section that re-narrates each point already made in the body, rather than adding a real synthesis or a different level of abstraction. If the current piece has other installments in the same series, check their closing sections for the actual house pattern before assuming the draft's structure is normal.
- **Uniform templating across parallel sections** — when a piece covers multiple similar subjects (people, products, releases), check whether each section leans on the identical rhetorical device (the same contrast construction in every headline, the same sentence shape closing every section). Some repetition is natural; identical scaffolding every time is a tell.

### 4. Run the checklist

#### For both articles and tutorials:

- [ ] **No placeholders** — no TODOs, no `[insert X here]`, no `...` in code blocks
- [ ] **No skeleton sections** — every H2/H3 has real prose, not just a heading
- [ ] **Images use Cloudflare Images** — all image URLs are `https://imagedelivery.net/K11gkZF3xaVyYzFESMdWIQ/{image_id}/public` — no local paths, no Cloudinary URLs, no hotlinked external images. To upload a new image: use the Cloudflare Images API with the `CLOUDFLARE_IMAGES_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` from `.agents/skills/.env`.
- [ ] **No unverified stats** — any numbers or claims have a linked source in the text
- [ ] **No marketing language** — scan for: "powerful", "revolutionary", "cutting-edge", "game-changing"
- [ ] **No internal production notes in the file** — the article/tutorial file must end with published content only. Scan for and strip anything like a "SOCIAL POST BRIEF" section, editor notes, or other non-reader-facing content appended after the sign-off line — these ship live if left in.
- [ ] **No AI-writing patterns** — covered by the humanizer pass in step 3

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
- [ ] **No GFM pipe tables** — the lablab.ai MDX renderer does not support markdown pipe-syntax tables (`| col |`). Every table must use raw HTML: `<table><thead><tr><th>…</th></tr></thead><tbody><tr><td>…</td></tr></tbody></table>`. Use `<code>` tags (not backticks) for inline code inside table cells.
- [ ] **Language declared** on every fenced code block (` ```python `, ` ```typescript `, etc.)
- [ ] **Prerequisites section present** — tools, API keys, framework versions listed
- [ ] **`.env` format shown** (if needed) — with placeholder values, never real keys
- [ ] **Final output shown** — screenshot, terminal output, or demo of the working result
- [ ] **File saved in** `tutorials/[slug]/article.md`

### 5. Report results

List every checklist item with a pass/fail. For any failure:
- Quote the specific line or section that has the problem
- Suggest the fix

Report the humanizer pass separately: what it changed (or that it found nothing to change), and any pattern it flagged that was deliberately left as house style.

Do not mark the piece as done if any item fails.

### 6. Update Notion

Once all checklist items pass:
- Fetch the Notion task by title from DB `2cab4088-66ca-4d1f-aeb9-8fe29dafb470`
- Update Status → `Done`
- Add a note to the Notes field: `Draft complete. File: [path]. Checked: [today's date].`

### 7. Confirm

Report: "All checks passed. Notion task '[title]' set to Done."

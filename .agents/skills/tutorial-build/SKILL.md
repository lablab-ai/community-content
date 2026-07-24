---
name: tutorial-build
description: Build and verify a working code project before writing a tutorial. Use before drafting any tutorial that involves code — scaffolds the project, implements each component step by step, and confirms end-to-end functionality. Only hand off to writing once the code actually runs.
compatibility: Designed for Claude Code. Requires API keys for the relevant services to be available in the project .env file.
---

## Why this skill exists

Tutorials written from a working project are more accurate, more complete, and contain no speculative code. This skill ensures the implementation is verified before a single tutorial word is written.

## Steps

### 1. Confirm inputs

Collect (from the prior `content-start` run or from the user):
- **Tutorial topic and angle** — what the project does and who it is for
- **Tech stack** — APIs, SDKs, and libraries involved
- **Suggested file path** — the tutorial destination (e.g. `tutorials/en/[slug]/article.mdx`)

Derive the project name from the tutorial slug:
- Tutorial slug: `bright-data-hiring-signal-detector`
- Project directory: `~/Lablab-AI/bright-data-hiring-signal-detector/`

### 2. Scaffold the project

Create the project directory **outside** the community-content repo, under `~/Lablab-AI/[project-slug]/`.

Standard layout:

```
~/Lablab-AI/[project-slug]/
├── main.py            — entry point; orchestrates the pipeline
├── scraper.py         — data collection (API calls, pagination)
├── analyzer.py        — AI analysis / inference layer
├── .env               — API keys (never committed)
├── .gitignore         — at minimum: .env, __pycache__, *.pyc
├── requirements.txt   — pinned dependencies
└── sample_input.json  — sample watchlist or test fixtures
```

Adjust the layout as needed:
- Single-file scripts are fine for short projects
- Add subdirectories only if the project genuinely needs them

**Before writing any files:** confirm the directory does not already exist.

### 3. Write requirements.txt first

List all packages before writing any implementation code. Pin major versions (e.g. `google-generativeai>=0.8`). This makes the install step in the tutorial concrete and reproducible.

### 4. Build the .env template

Create a `.env.example` (committed) alongside the `.env` (gitignored):

```
# .env.example — copy to .env and fill in your keys
BRIGHT_DATA_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

Only include keys that are actually used. Do not add placeholders for services not in scope.

### 5. Implement component by component

Build in dependency order — data in → processing → output out. For each component:

1. Write the file
2. Test it in isolation before moving to the next
3. Fix any errors before proceeding — do not stack untested code

**Do not mock API calls** unless a service is completely unavailable. Real API responses reveal real edge cases that determine what the tutorial needs to explain.

Typical order:
1. `scraper.py` — get data from the external API; print raw response to confirm shape
2. `analyzer.py` — pass sample data to the AI model; confirm output schema
3. `main.py` — wire scraper → analyzer → output; run the full pipeline

### 6. Add a sample input

Create `sample_input.json` with 2–3 realistic entries — enough to produce meaningful output without burning excessive API credits during development.

Example for a company watchlist:
```json
[
  { "company": "Stripe", "linkedin_url": "https://www.linkedin.com/company/stripe" },
  { "company": "Notion", "linkedin_url": "https://www.linkedin.com/company/notion" }
]
```

### 7. Run end-to-end

Run `python main.py` (or equivalent) against the sample input. The project passes when:

- [ ] No unhandled exceptions
- [ ] Output matches the expected schema
- [ ] Every API call returns real data (not mocked, not stubbed)
- [ ] The output is meaningful enough to screenshot or quote in the tutorial

If any check fails, fix the code before proceeding.

### 8. Build a demo UI (if the tutorial involves a live/streaming demo or a demo video)

A console log is not enough when the tutorial's whole point is watching something happen live (streaming transcription, multi-step agent output, real-time scores/sentiment, etc.). Build a small UI once the CLI version above proves the pipeline works — never skip straight to UI before the pipeline is verified.

- **Default to Gradio** unless the project already has a matching precedent (e.g. the vendor's own reference demo uses something else) or the user asks for a different framework — it's the fastest path from a working async/callback pipeline to something screen-recordable.
- Bridge async producers (websocket callbacks, streaming SDKs) into Gradio with a background thread + thread-safe `queue.Queue`, and a generator function that `yield`s updated output tuples as events arrive. Don't block Gradio's main thread on the async loop.
- Show every moving part at once: whatever the pipeline produces (transcript, translations, scores, summaries) gets its own visible panel — the point is that a viewer can watch the whole system think, not just see a final answer.
- Keep it to one file (`ui.py`), reusing the same component modules the CLI version already validated (e.g. `analyzer.py`, `transcriber.py`) — don't duplicate logic between the CLI and UI entry points.
- Verify the app builds (`gr.Blocks` constructs without error) even before real API keys are available; do the full interactive click-through once keys are in place.
- This UI becomes the artifact used for the demo video and for tutorial screenshots — write the corresponding tutorial section as a walkthrough of this UI, not of raw console output.

### 9. Push the project to a GitHub companion repo

Once the code is fully verified (and the demo UI, if any, is built), push it somewhere a tutorial reader can actually see it — don't leave it only on disk. Someone landing on this repo cold (from the tutorial's links) should immediately understand what it is — that means a real name, a real description, and a real README, not defaults inherited from the tutorial's own slug.

1. **Pick a short, human repo name — never the raw tutorial slug.** Tutorial slugs are SEO-optimized and long (`aws-kiro-hooks-steering-custom-agents-deep-dive`); a repo is a project, not an article, and needs a name someone would actually type or remember (`kiro-task-tracker`). If the tutorial already tells readers to `mkdir` a project with a specific name, use that same name — consistency between what the article says to create and what the repo is actually called matters. Check it's free: `gh repo view [github-username]/[project-name]`.
2. Review what's about to be pushed before creating anything — `git status`, `git ls-files`, and a quick secrets scan (`git grep -niE "sk-|api[_-]?key|token\s*="`). Confirm no real credentials, only `.env.example` placeholders.
3. **Write a real README before pushing** (not the placeholder from scaffolding, if one exists). At minimum: one line on what the project is, what it demonstrates (tie it to the tutorial's actual hook/feature, not generic boilerplate), a table or list of what's in the repo and why each piece exists, exact setup/run commands, and a closing line pointing back to the tutorial. A visitor should be able to read only the README and know whether this is worth exploring further.
4. Create it under the user's own account, not an org, unless told otherwise, with a real one-sentence description (what it does + that it's a tutorial companion — not a copy-paste of the tutorial's title): `gh repo create [username]/[project-name] --private --description "..." --source=. --remote=origin`. Default to **private** — ask the user whether/when it should go public, since a private repo means the line-anchored links below won't resolve for readers until it's flipped.
5. Push: `git branch -M main && git push -u origin main`.
6. Note the exact commit SHA pushed (`git rev-parse HEAD`) — use it (not `main`) for every line-anchored link so the links stay stable even if the repo changes later: `https://github.com/[user]/[repo]/blob/[sha]/[path]#L[start]-L[end]`.
7. For each code block the tutorial shows in full and that matches the repo file 1:1, add a link right after it: `*[View [file] on GitHub]([permalink])*`. For files that evolve across the tutorial (e.g. a base scaffold in an early step, more endpoints added later), link the partial line range for the early snippet and the full file for the finished version — don't link a range that doesn't match what's actually shown at that point.
8. Verify the links resolve as the user would see them — `gh api repos/[user]/[repo]/contents/[path]` confirms the file is really there; a plain `curl` on a private repo will 404 even when everything is correct, so don't mistake that for a broken push.
9. If the repo name changes for any reason after links are already written (a rename, a typo fix), `gh repo rename` preserves history and old commit SHAs stay valid — but update every link in the tutorial to the new name anyway rather than relying on GitHub's redirect.

### 10. Capture what matters for the tutorial

Before handing off, note:

- **Exact install command:** `pip install -r requirements.txt`
- **Exact run command:** `python main.py` (or with args if applicable)
- **Any non-obvious setup steps** (environment variable names, account prerequisites, API console steps)
- **One real output sample** — paste or save actual output to reference while writing
- **Any gotchas found** during implementation (rate limits, response shape surprises, auth quirks)

These notes become the Prerequisites and troubleshooting sections of the tutorial.

### 11. Hand off to tutorial writing

The project is ready to document when all end-to-end checks pass. Proceed with writing the tutorial at the path confirmed in `content-start`. Write by narrating what the working code does — do not invent or speculate. Where a code block matches a pushed file, include its GitHub permalink from Step 9.

**Lead with the demo, not the code.** Right after the intro (before Prerequisites, before any code walkthrough), add a "See it running first" section:
1. `git clone` the companion repo from Step 9, install, and run it — the exact commands a reader needs to get the finished thing running with zero code written yet.
2. 1–3 of the strongest screenshots/output from the working demo (the payoff moments — a regression caught, a scoped agent refusing something, a live dashboard updating), framed as "here's what you'll have by the end."
3. A one-line bridge into the build: something like "the rest of this tutorial builds this from scratch and explains why."

Only after that does Prerequisites → step-by-step code walkthrough begin. It's fine for a hero screenshot to reappear later at the exact step that produces it — caption the repeat so it reads as intentional ("the same green state, reached by actually building X") rather than a duplicate slip-up.

**Explain the why, not just the what.** Never introduce a code block as a bare instruction ("`app.py` — a minimal Task Tracker API:" followed immediately by the file). Every non-trivial block gets 1–3 sentences first that answer: what does this piece need to do, and why does it look the way it does — which design decisions in it are arbitrary versus load-bearing for a step that comes later. Concretely:
- If a field, structure, or convention in this code gets referenced or enforced by something later (a steering doc, a hook, a scoped tool), say so explicitly — "this is written by hand once here; Step N makes Kiro repeat it automatically."
- If a design choice looks like it could've been done another, more obvious way, say why it wasn't (e.g. why validation happens in the tool itself and not a client-side setting, why a script defensively scans a whole payload instead of trusting one field name).
- Keep this tight — one to three sentences per block, not a paragraph per line of code. The goal is "I understand why this exists," not a line-by-line narration.
- This applies to config files (JSON agent configs, steering docs) exactly as much as to source code — a JSON block dropped with no framing is the same mistake as an unexplained Python function.

Tutorial checklist at handoff:
- [ ] Project runs end-to-end with real APIs
- [ ] `sample_input.json` exists and produces real output
- [ ] All gotchas and setup steps are noted
- [ ] File path for tutorial confirmed: `tutorials/en/[slug]/article.mdx`
- [ ] Project pushed to a GitHub companion repo, commit SHA noted
- [ ] Notion task is `In Progress`

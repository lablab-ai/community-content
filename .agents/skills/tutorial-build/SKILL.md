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

### 8. Capture what matters for the tutorial

Before handing off, note:

- **Exact install command:** `pip install -r requirements.txt`
- **Exact run command:** `python main.py` (or with args if applicable)
- **Any non-obvious setup steps** (environment variable names, account prerequisites, API console steps)
- **One real output sample** — paste or save actual output to reference while writing
- **Any gotchas found** during implementation (rate limits, response shape surprises, auth quirks)

These notes become the Prerequisites and troubleshooting sections of the tutorial.

### 9. Hand off to tutorial writing

The project is ready to document when all end-to-end checks pass. Proceed with writing the tutorial at the path confirmed in `content-start`. Write by narrating what the working code does — do not invent or speculate.

Tutorial checklist at handoff:
- [ ] Project runs end-to-end with real APIs
- [ ] `sample_input.json` exists and produces real output
- [ ] All gotchas and setup steps are noted
- [ ] File path for tutorial confirmed: `tutorials/en/[slug]/article.mdx`
- [ ] Notion task is `In Progress`

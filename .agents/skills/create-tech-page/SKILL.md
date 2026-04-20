---
name: create-tech-page
description: Create a new technology page in the technologies/ directory. Use when adding a new company, model, or product to the Lablab tech index — researches the technology, drafts the MDX, and places it in the correct location.
compatibility: Designed for Claude Code. Requires WebSearch or Exa MCP for research.
---

## Steps

### 1. Identify the page type and subject

Ask the user (if not already provided):
- **Company or model/product?**
  - Company → creates `technologies/[provider-slug]/index.mdx`
  - Model/product → creates `technologies/[provider-slug]/[model-slug].mdx` (provider dir may already exist)
- **Name of the company, model, or product** (e.g. "Groq", "Llama 4", "Claude Sonnet")
- **Official website URL** (required — used as the canonical source)
- Any other useful links the user already has (docs, GitHub, Discord, API reference)

### 2. Check for an existing page

Before writing anything, check whether the page already exists:

```
Glob: technologies/[provider-slug]/**/*.mdx
```

- If an exact match exists → stop. Tell the user and suggest updating the existing file instead.
- If the provider directory exists but the specific model page does not → note this; the new file goes inside the existing directory.
- If nothing exists → proceed.

### 3. Research the technology

Use this search order:
1. **Exa MCP** (`mcp__exa__*`) — semantic search for official docs and overviews
2. **Brave Search MCP** (`mcp__brave__*`) — keyword search
3. **Built-in WebSearch** — fallback

Queries to run:
- `"[technology name]" site:[official-domain] docs OR documentation`
- `"[technology name]" overview OR about OR features`
- `"[technology name]" GitHub`
- `"[technology name]" API OR SDK`

Collect:
- Founding year and company background (for company pages)
- Release date (for model/product pages)
- Core features and capabilities
- Available SDKs, libraries, API access
- GitHub repo URL
- Discord or community link (if any)
- Pricing model (free tier, API costs) if publicly documented
- Any notable integrations or ecosystem partners

Do not invent facts. If something is not found, omit it rather than guess.

### 4. Determine the file path and branch

**File path rules:**
- Company index: `technologies/[provider-slug]/index.mdx`
- Model/product subpage: `technologies/[provider-slug]/[model-slug].mdx`
- Slugs use lowercase kebab-case (e.g. `llama-4`, `groq`, `claude-sonnet`)

**Branch:** Check the current git branch. If already on a suitable feature branch (e.g. `add-[slug]`), use it. Otherwise, remind the user to create one:
```
git checkout -b add-[slug]
```

### 5. Draft the MDX

#### For a company index page (`index.mdx`)

```mdx
---
title: "[Company Name]"
description: "[One sentence: what the company does and why it matters to AI builders. 20–40 words.]"
---

# [Company Name]

[2–3 sentence intro: founding story, core mission, and what makes it relevant to developers.]

| General | |
|---------|--|
| **Company** | [Company Name](https://company.com) |
| **Founded** | [Year] by [Founder(s)] |
| **Headquarters** | [City, Country] |
| **Website** | [company.com](https://company.com) |
| **Documentation** | [Docs title](https://docs.company.com) |
| **GitHub** | [github.com/org](https://github.com/org) |
| **Type** | [Category, e.g. "AI Infrastructure", "LLM Provider"] |

---

## Core Products

### [Product 1 Name]
[2–3 sentences describing what it does and who it is for.]

### [Product 2 Name]
[2–3 sentences.]

---

## Developer Resources

[1–2 sentences introducing the developer ecosystem.]

<TechTutorials/>

### Helpful Links

- [Documentation](https://docs.company.com) — official API and SDK reference
- [GitHub](https://github.com/org) — open-source repos and examples
- [Discord](https://discord.gg/...) — community support *(if available)*
- [API Console / Playground](https://console.company.com) — start building

---

## Key Features

**[Feature 1]**
[1–2 bullet points or sentence.]

**[Feature 2]**
[1–2 bullet points or sentence.]

---

## Use Cases

**[Use Case 1]**
[1–2 sentences.]

**[Use Case 2]**
[1–2 sentences.]
```

#### For a model/product subpage (`[model-slug].mdx`)

```mdx
---
title: "[Model/Product Name]"
author: "[provider-slug]"
description: "[One sentence: what the model/product is, its architecture or key capability, and availability. 25–50 words.]"
---

# [Model/Product Name]

[2–3 sentence intro: what it is, what makes it technically notable, and where it fits in the ecosystem. Link the name to the official announcement or product page.]

| General | |
|---------|--|
| **Release date** | [Day Mon Year] |
| **Developer** | [Company Name] |
| **Type** | [e.g. "Open-weight multimodal LLM", "Text-to-speech API"] |
| **License** | [License name, or "Commercial API"] |
| **GitHub** | [org/repo](https://github.com/org/repo) *(if open-source)* |
| **Documentation** | [Docs title](https://docs.url) |

---

## Core Features

- **[Feature 1]** — [one-line explanation with source link if available].
- **[Feature 2]** — [one-line explanation].
- **[Feature 3]** — [one-line explanation].

---

## [Model Variants / Pricing Tiers] *(include only if the product has multiple variants)*

| Variant | [Key Param] | [Key Param] | Best for |
|---------|-------------|-------------|----------|
| **[Variant A]** | [value] | [value] | [use case] |
| **[Variant B]** | [value] | [value] | [use case] |

---

## Tools and Resources

- **[Resource 1]** — [what it is and link].
- **[Resource 2]** — [what it is and link].
- **[Quickstart / Playground]** — [link].

---

## Ecosystem and Integrations

- [Integration or deployment context 1].
- [Integration or deployment context 2].

---

[1–2 sentence closing: how to get started, with 1–2 direct links.]
```

### 6. Quality checks before saving

Run these checks on the draft before writing the file:

- [ ] **No em dashes (—)** — replace with commas, periods, or parentheses
- [ ] **No invented facts** — every specific claim (founding year, parameter count, pricing) has a source you actually found
- [ ] **All URLs resolve** — spot-check at least the homepage and docs URL
- [ ] **Frontmatter complete** — `title` and `description` present; `author` present on model pages
- [ ] **`<TechTutorials/>` included** on company index pages (in the Developer Resources section)
- [ ] **No placeholder text** — no `[insert X]`, no `TBD` unless genuinely not yet announced
- [ ] **No marketing language** — avoid "powerful", "revolutionary", "cutting-edge", "game-changing"
- [ ] **Slug is kebab-case lowercase** in the file path

### 7. Write the file

Write the drafted MDX to the correct path. Confirm the full path to the user before writing.

### 8. Confirm and hand off

Report:
- File written to: `technologies/[path]`
- Key facts sourced from: [list URLs used]
- Any gaps left blank because they could not be verified (user should fill these in)
- Suggested next step: run `publish-check` if the page is ready to ship, or note what still needs filling in

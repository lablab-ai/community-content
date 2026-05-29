---
name: hackathon-tutorial
description: Generate a tutorial concept directly from a hackathon page. Takes a hackathon URL or pasted page content, extracts partners, tracks, timeline, and challenge requirements, then identifies the strongest tutorial angle a participant could actually build and submit. Outputs a ready-to-write brief and Notion task. Hands off to content-start.
compatibility: Designed for Claude Code. Requires WebSearch or WebFetch for URL fetching, and python3 with requests installed for Notion posting.
---

## When to use

Run this skill when you have a hackathon page and need to produce a tutorial that:
- Helps participants understand how to use the partner tech
- Serves as a working reference implementation for the challenge
- Is publishable before or during the hackathon (not after it ends)

Do NOT use this skill for post-hackathon recap articles or winner write-ups — use `content-ideate` for those.

---

## Steps

### 1. Ingest the hackathon page

Accept either:
- A URL — fetch the full page content with WebFetch
- Pasted page content — use as-is

Extract and record the following. If any field is missing, note it as unknown rather than guessing:

```
Hackathon name:
Hackathon URL:
Dates: [start] to [end]  ← compute days remaining from today
Prize pool:
Tracks: [list each track name + one-line description]
Partner technologies: [name, what it does, docs URL if visible]
Minimum submission requirements: [e.g. "at least 3 agents", "must use Band SDK"]
Example projects listed on page: [titles only]
Target participant level implied by the page:
```

### 2. Identify the strongest tutorial angle

A strong hackathon tutorial must satisfy all three:

1. **Directly uses partner tech** — the tutorial builds something with the sponsor's SDK/API, not a generic stack that happens to mention it
2. **Maps to a real track** — the output is a plausible submission for one of the listed tracks (name the track explicitly)
3. **Completable in one sitting** — an intermediate developer can follow it in 60–90 minutes and have a working demo

Evaluate each partner technology:
- Is there already an official "getting started" guide? (If yes, the tutorial must go further — a starter is not enough)
- Which partner has the least existing tutorial coverage? (This is usually the best angle)
- Which combination of partners produces the most interesting demo?

Pick the **single strongest angle**. If the hackathon has multiple tracks, default to the track with the most example use cases listed on the page (usually the broadest one). Note if a different track would make a better tutorial and explain why.

### 3. Uniqueness check

The tutorial must cover ground that does not already exist. Run all searches in parallel:

1. `site:lablab.ai [partner name] tutorial`
2. `[partner SDK name] tutorial [current year]`
3. `[partner SDK name] site:medium.com OR site:dev.to OR site:hashnode.com`
4. `[partner SDK name] [hackathon challenge type] tutorial` — e.g. "Band SDK multi-agent tutorial"
5. `[partner SDK name] github example` — check if an official example repo already exists that would make our tutorial redundant

After searching, answer:
- What already exists? (list title + platform for each)
- What is the specific gap? (use case, reader level, tool combination, or recency)
- Is the tutorial still worth writing? If existing coverage is deep and recent, reframe or pick a different partner.

Only proceed with an angle that passes: **"I could not find this exact tutorial written anywhere."**

### 4. Define what the tutorial builds

Specify the demo project in one concrete paragraph:

```
What it builds: [noun phrase — e.g. "a 3-agent software delivery pipeline"]
Input: [what the user provides — e.g. "a GitHub issue title"]
Output: [what the system produces — e.g. "a reviewed, tested pull request draft"]
Partner tech used: [SDK/API name + which features]
Track this targets: [track name from the hackathon page]
Repo structure: [top-level files — e.g. planner.py, engineer.py, reviewer.py, band_config.py]
Estimated steps in the tutorial: [number]
```

This section forces specificity before writing begins. If you cannot fill it in, the angle is not concrete enough — go back to step 2.

### 5. Generate titles

Produce 3 title options. Requirements:
- Outcome-first: lead with what the reader will have built, not the technology name
- Name the partner tech and the use case
- Avoid: "A Guide to X", "Getting Started with X", "Introduction to X", "The Ultimate X Tutorial"

Format:
```
Option 1 (recommended): [title]
Option 2: [title]
Option 3: [title]
```

### 6. Present the full brief

```
─────────────────────────────────────────────
HACKATHON TUTORIAL BRIEF
─────────────────────────────────────────────
Hackathon:        [name + URL]
Submission window: [days remaining]
Target track:     [track name]

Type:             Tutorial
Recommended title: [title]
Alternative titles:
  - [option 2]
  - [option 3]

What it builds:   [one sentence]
Partner tech:     [SDK/API name(s)]
Hook:             [one sentence — what makes this different from what already exists]
Target reader:    [Beginner / Intermediate / Advanced]
Angle:            [2–3 sentences — what the tutorial covers, what the reader walks away able to submit]

Steps outline:
  1. [step name]
  2. [step name]
  3. [step name]
  ... (5–8 steps total)

Suggested file path: tutorials/en/[slug].mdx
Suggested repo name: [kebab-case-repo-name]
─────────────────────────────────────────────
```

Wait for the user to confirm the title and angle before continuing.

### 7. Post to Notion

Once the user confirms, post to the Tasks & Action Items DB (`2cab4088-66ca-4d1f-aeb9-8fe29dafb470`):

```bash
python3 scripts/post_to_notion.py \
  --title "confirmed title" \
  --type "Tutorial" \
  --hook "hook sentence" \
  --reader "Intermediate" \
  --angle "angle summary" \
  --path "tutorials/en/slug.mdx"
```

Append to the Notes field (manually via PATCH if the script does not support it):
```
Hackathon: [name]
Track: [track name]
Deadline: [submission end date]
Partner tech: [SDK/API names]
Repo: [suggested repo name]
```

Share the Notion URL with the user.

### 8. Hand off

Confirm to the user:
- [ ] Hackathon page parsed
- [ ] Tutorial angle confirmed
- [ ] Uniqueness check passed
- [ ] What it builds is fully specified
- [ ] Notion task created with deadline and track noted
- [ ] File path decided: `tutorials/en/[slug].mdx`

Next steps:
1. Run `content-start` with the confirmed title to run the full pre-writing protocol
2. Create the GitHub repo (`[suggested repo name]`) and scaffold the files listed in the steps outline
3. Write the tutorial — aim to publish at least 3 days before the hackathon submission deadline so participants have time to use it

---

## Timing rule

If fewer than 3 days remain before the submission deadline, flag this to the user before proceeding. A tutorial published the day before submissions close has limited value. Suggest either:
- A shorter format (a README walkthrough in the partner's repo rather than a full lablab tutorial)
- Shifting focus to a post-hackathon article summarising what was built

---

## Common mistakes to avoid

- **Angle too broad:** "Build an AI agent with Band" is not a tutorial — "Build a 3-agent PR review pipeline with Band SDK and Claude" is
- **Partner tech is decorative:** if you could remove the partner SDK and the tutorial would still work, the angle is wrong
- **Existing official example:** check the partner's GitHub — if they already ship a working example that matches your idea, build on top of it rather than duplicating it
- **No working demo:** every tutorial must end with something the user can run and show in a 2-minute demo video

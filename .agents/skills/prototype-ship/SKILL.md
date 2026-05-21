---
name: prototype-ship
description: Build a working prototype, verify it end-to-end, create a GitHub repo, commit each file individually with a descriptive message, build a web UI frontend, and push everything. Use whenever a tutorial prototype is ready to be shipped to GitHub.
compatibility: Designed for Claude Code. Requires gh CLI authenticated as Stephen-Kimoi.
---

## Steps

### 1. Verify the prototype works end-to-end

Before touching git:
- Run the core script manually and confirm it produces real output
- Fix any errors until a clean run completes
- Note any gotchas encountered — these are tutorial gold

### 2. Build a web UI (if not already present)

Every prototype needs a UI that non-technical people can understand.

**Required files:**
- `agent.py` (or equivalent) — refactor to expose a **generator/stream interface** alongside the CLI interface. The generator yields typed event dicts: `{"type": "tool_call"|"tool_result"|"thinking"|"report"|"error", ...}`
- `app.py` — Flask server with a **Server-Sent Events (SSE) endpoint** that wraps the generator
- `templates/index.html` — single-page UI with:
  - Input field + submit button
  - Live **activity feed** panel (shows tool calls streaming in real time)
  - **Output/report panel** (renders markdown with marked.js or similar)
  - Stats bar (counts of tool calls, searches, scrapes, etc.)
- `requirements.txt` — must include `flask>=3.0.0`

**UI design standards:**
- Dark theme (`#0f0f13` background)
- Accent color: `#7c6aff` (purple) for primary actions, `#06b6d4` (cyan) for secondary
- Animated dot indicator while agent is running
- Activity items animate in with `slideIn` keyframe
- Markdown rendered in the report panel — use `marked.js` from CDN
- No frontend framework — vanilla JS only

**Smoke test the UI before committing:**
```bash
source venv/bin/activate && python app.py &
sleep 2 && curl -s http://localhost:5000 | head -3
kill %1
```

### 3. Create the GitHub repository

```bash
gh repo create Stephen-Kimoi/<repo-slug> \
  --public \
  --description "<one-line description>"
```

Then:
```bash
git init
git config user.name "Steve Kimoi"
git config user.email "stephen.kimoi@nativelyai.com"
git remote add origin https://github.com/Stephen-Kimoi/<repo-slug>.git
git branch -M main
```

### 4. Commit each file individually

Commit in this order, one file per commit:

| File | Commit message pattern |
|---|---|
| `.gitignore` | `Add .gitignore` + what it excludes |
| `requirements.txt` | `Add requirements.txt` + list the key deps and why |
| Core logic file (e.g. `agent.py`) | `Add <file> — <one-line role>` + what it implements and how |
| Server file (e.g. `app.py`) | `Add <file> — <one-line role>` + what the endpoint does |
| `templates/index.html` | `Add templates/index.html — frontend UI` + what it shows |
| `README.md` | `Add README.md` + what it covers |

**Commit message rules:**
- Subject line: `Add <filename> — <role>` (imperative, under 72 chars)
- Body: 2–4 lines explaining what the file does and any non-obvious decisions
- No `Co-Authored-By` lines
- No "Generated with Claude" footers

### 5. Write the README

The README must include:
- [ ] What the project does (2–3 sentences)
- [ ] Architecture diagram (ASCII, showing data flow)
- [ ] Project file structure with one-line descriptions
- [ ] Prerequisites (accounts, tools needed)
- [ ] Full setup steps (clone → venv → pip install → .env → run)
- [ ] How the core loop works (simplified code snippet)
- [ ] Example output
- [ ] Ideas for extending the project
- [ ] Built-with table

### 6. Push

```bash
git push -u origin main
```

### 7. Hand off

Confirm:
- [ ] Prototype runs end-to-end without errors
- [ ] UI serves at `localhost:5000` and streams live tool calls
- [ ] All files committed individually with descriptive messages
- [ ] README covers architecture + full setup
- [ ] Repo is public at `https://github.com/Stephen-Kimoi/<repo-slug>`
- [ ] Ready to write the tutorial (proceed to drafting)

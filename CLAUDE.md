# CLAUDE.md — community-content

This is the Lablab community-content repo. It contains all published articles, tutorials, technology pages, and topic pages for [lablab.ai](https://lablab.ai).

---

## Repo structure

```
blog/en/          — Articles (MDX)
tutorials/        — Tutorial articles (MDX)
technologies/     — Technology index pages
topics/           — Topic index pages
```

## Content standards

- **Frontmatter required on every file:** `title`, `description`, `image`, `authorUsername`
- **Images must use Cloudflare Images:** all image URLs must be `https://imagedelivery.net/K11gkZF3xaVyYzFESMdWIQ/{image_id}/public` — no local paths, no hotlinked external images, no Cloudinary URLs
- **Cloudflare Images account hash:** `K11gkZF3xaVyYzFESMdWIQ` (API token in `.agents/skills/.env` as `CLOUDFLARE_IMAGES_TOKEN`)
- **Author username:** `stevekimoi`
- **SEO guidelines:** see `SEO_GUIDELINES.md` for keyword strategy and frontmatter formatting rules

## Skills

Six agent skills live in `.agents/skills/` and cover the full content lifecycle. Use them in order:

| Skill | When to use |
|-------|-------------|
| [`hackathon-tutorial`](.agents/skills/hackathon-tutorial/SKILL.md) | When you have a hackathon page (URL or pasted content) and need a tutorial concept — parses partners/tracks/timeline, finds the strongest angle, does a uniqueness check, outputs a ready-to-write brief. Run this first, before content-start |
| [`content-ideate`](.agents/skills/content-ideate/SKILL.md) | When you have a source (tweet, article, raw idea) and want to turn it into a content concept — outputs working title + brief, hands off to content-start |
| [`content-start`](.agents/skills/content-start/SKILL.md) | Before writing any new article or tutorial — runs uniqueness check, gathers sources, confirms angle, sets Notion task to In Progress |
| [`tutorial-build`](.agents/skills/tutorial-build/SKILL.md) | For tutorials with code — scaffolds and builds the working project end-to-end before any writing starts; hands off once the code runs cleanly |
| [`create-tech-page`](.agents/skills/create-tech-page/SKILL.md) | When adding a new technology, model, or product to the tech index — researches, drafts, and places the MDX in `technologies/` |
| [`publish-check`](.agents/skills/publish-check/SKILL.md) | When a draft is complete — runs the full publishing checklist and updates Notion to Done |
| [`seo-apply`](.agents/skills/seo-apply/SKILL.md) | After a draft passes publish-check — reads this week's Notion SEO clusters and applies surgical keyword improvements without changing tone |
| [`weekly-ai-recap`](.agents/skills/weekly-ai-recap/SKILL.md) | Every Monday — researches the week's top AI news, writes the recap article, produces the social post brief |

## Notion

- Tasks DB: `2cab4088-66ca-4d1f-aeb9-8fe29dafb470`
- Token: stored in `~/claude-workspace-automation/.env` as `NOTION_TOKEN`
- Filter for content tasks: `Workspace = Lablab`, `Category = Content`

## Git workflow

- All new content goes on a feature branch, never directly to `main`
- Branch naming: `add-[slug]`, `update-[slug]`, `fix-[slug]`
- PRs target the upstream `lablab-ai/community-content` repo
- **No `Co-Authored-By` lines in commits** — do not add Claude Code attribution to any commit message

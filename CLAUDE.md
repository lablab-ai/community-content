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
- **Images must use Cloudinary:** all image URLs must be `https://res.cloudinary.com/dygkv9gam/image/upload/...` — no local paths, no hotlinked external images
- **Cloudinary cloud name:** `dygkv9gam` (credentials in env as `CLOUDINARY_URL`)
- **Author username:** `stevekimoi`
- **SEO guidelines:** see `SEO_GUIDELINES.md` for keyword strategy and frontmatter formatting rules

## Skills

Four agent skills live in `.agents/skills/` and cover the full content lifecycle. Use them in order:

| Skill | When to use |
|-------|-------------|
| [`content-ideate`](.agents/skills/content-ideate/SKILL.md) | When you have a source (tweet, article, raw idea) and want to turn it into a content concept — outputs working title + brief, hands off to content-start |
| [`content-start`](.agents/skills/content-start/SKILL.md) | Before writing any new article or tutorial — runs uniqueness check, gathers sources, confirms angle, sets Notion task to In Progress |
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

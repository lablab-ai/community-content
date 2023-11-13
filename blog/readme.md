# Blog

Repo to handle submitting & updating blog posts on lablab.ai

## How to publish a new blog post on lablab

In this guide you will learn how to publish blog postss on lablab.

## General information

- [Check out our example blog posts page]([https://github.com/lablab-ai/community-content/blob/main/blog/ai-in-business-how-use-ai-to-stay-ahead-of-the-competition.mdx](https://github.com/lablab-ai/community-content/blob/main/blog/en/ai-in-business-how-use-ai-to-stay-ahead-of-the-competition.mdx))
- Please **don’t** copy the content from other websites!
- Please **don’t** use AI content generators to create the content for this page!
- Make sure the blog post has a **clear structure**. Use a minimum of three H2 headings, including one for the introduction, another for the topic input, and the last one to summarize all previously discussed points. Additionally, use H3 subheadings for every significant point you cover.

## If you want to publish a new blog post on lablab.ai, follow these steps:

1. Create an mdx file for the blog post with the post title in slug format (you can slugify [here](https://slugify.online/)) as the filename in this GitHub repository: [https://github.com/lablab-ai/community-content/edit/main/blog/](https://github.com/lablab-ai/community-content/edit/main/blog/)

2. Please keep in mind we might change the filename and title of the blog post to make it more SEO friendly.

3. For each blog post page, include the following information:

   - **title**: Title of the post
   - **description**: Description of the post
   - **authorUsername**: Your username on lablab.ai

4. To add image use the `<Img src={path_to_your_img}, alt={img_alt}, caption={short_img_caption_below_it}/>` component.

5. After you create a PR we will check the blog post content and merge it if everything is fine.

Finally, visit our GitHub repo and add AI Blog posts here, get inspiration from the existing pages when creating your own: [https://github.com/lablab-ai/community-content/edit/main/blog/](https://github.com/lablab-ai/community-content/edit/main/blog/).

## How to add page?

1. Write it!
2. Create two pull requests:
   - to `community-content` branch - thanks to that our internal system will be able to check if your files contains plagiarism/AI generated content (required)
   - to `main` branch

## Adding as sponsored content/Adding sponsored banner

1. To add sponsor as author and link to the sponsor website add to the top of the file under the mandatory fields:
   - **sponsor**: Sponsored by ...
   - **sponsorUrl**: https://...

Keep in mind still you have to add a valid authorUsername!

2. To place a sponsor banner inside the post --> add `<SponsoredContentImage url="https://linktosponsor.com" imageUrl="https://sponsor/linktosponsorlogo.jpg"/>` somewhere in the post

# Tutorials

Repo to handle submitting & updating tutorials on lablab.ai

## How to publish a new tutorial on lablab

In this guide you will learn how to publish tutorial pages on lablab.

## General information

- [Check out the tutorial page template](https://github.com/lablab-ai/tutorials/blob/main/template.mdx)
- Please **don’t** copy the content from other websites!
- Please **don’t** use AI content generators to create the content for this page!
- Make sure the tutorial has a **clear structure**. Use a minimum of three H2 headings, including one for the introduction, another for the topic input, and the last one to summarize all previously discussed points. Additionally, use H3 subheadings for every significant point you cover.
- The tutorial you create must relate to one of the technologies listed in the lablab database.

## If you want to publish a new tutorial on lablab.ai, follow these steps:

1. Create an mdx file for the tutorial with the tutorial title in slug format (you can slugify [here](https://slugify.online/)) as the filename in this GitHub repository: [https://github.com/lablab-ai/tutorials](https://github.com/lablab-ai/tutorials)

2. Please keep in mind we might change the filename and title of the tutorial to make it more SEO friendly.

3. For each tutorial page, include the following information:
    - **title**: Title of the tutorial
    - **description**: Description of the tutorial
    - **authorUsername**: Your username on lablab.ai

<Img src="https://imagedelivery.net/K11gkZF3xaVyYzFESMdWIQ/1f01d403-aa8b-43fd-0a0f-e7f5ee3e8b00/full" alt="tutorial title, description, and author"/>

4. You can use one of our tutorial page as a template or the [template](https://github.com/lablab-ai/tutorials/blob/main/template.mdx) file in this repo to create your own tutorial page.
5. To add image use the `<Img src={path_to_your_img}, alt={img_alt}, caption={short_img_caption_below_it}/>` component.
 
6. After you create a PR we will check the tutorial content and merge it if everything is fine.

Finally, visit our GitHub repo and add AI tutorials here, get inspiration from the existing pages when creating your own: [https://github.com/lablab-ai/tutorials](https://github.com/lablab-ai/tutorials).

## How to add page?

1. Write it!
2. Create two pull requests:
    - to `tutorials` branch - thanks to that our internal system will be able to check if your files contains plagiarism/AI generated content (required)
    - to `main` branch

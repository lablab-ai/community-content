# Technologies

Repo to handle submitting & updating technologies on lablab.ai

## 👉 How to publish a new technology on lablab

In this guide you will learn how to publish technology pages on lablab.

### General information

- [Check out the technology page template](https://github.com/lablab-ai/community-content/blob/main/technologies/template.mdx)
- Please **don’t** copy the content from other websites!
- Please **don’t** use AI content generators to create the content for this page!

If you want to publish a new technology on lablab.ai, follow these steps:

1. Create a folder for the technology you're adding in this GitHub repository: [https://github.com/lablab-ai/community-content/tree/main/technologies)
2. Here create the folder, and create a file named 'index.mdx' for the technology.
3. If you're adding multiple technologies from the same provider, create a folder with the provider's name, and include an 'index.mdx' file that describes the provider, as well as separate pages for each technology they offer. You can find a good example of this in the [OpenAI folder of our GitHub repo](https://github.com/lablab-ai/technologies/tree/main/openai).

## 👉 Create a technology provider page

4. Create a page for the technology provider that includes the following information:
   - **Title**: Same as the provider's name.
   - **Description**: A brief (88-158 characters) description that includes one main keyword related to the provider (e.g., "OpenAI").
   - **Table**: Start with a heading (H1) that includes the company name, description, and the date it was founded. If the provider has a public repository, include a link to it.
   - **Start building with provider's products**: Create a heading (H2) that says "Start building with [Provider's] products" and write a short introduction (at least two sentences) about the company's products. End with a sentence that encourages readers to check out the apps created with this technology during lablab.ai hackathons.
   - **List the products**: Use the heading (H2) for the technology, and include a short description and a link to its page.

<Img src="https://imagedelivery.net/K11gkZF3xaVyYzFESMdWIQ/0ef49169-6775-4ce9-6da5-a28f4eb95d00/full" alt="title index"/>
<Img src="https://imagedelivery.net/K11gkZF3xaVyYzFESMdWIQ/3041412d-49ce-42e8-aff9-42a5ba2ec600/full" alt="table index"/>

## 👉 Create a page for a specific technology

5. If you're adding only one technology, use the index file for the technology. If you're adding multiple products, create a separate page for each technology using its name as the title.
6. For each technology page, include the following information:
   - **Author**: Name of the provider (e.g., 'author="OpenAI"').
   - **Table**: Include the release date, author, link to documentation, link to the public GitHub repository, and the type of technology you're adding.
   - **Start building with the technology section**: Create a heading (H2) that says "Start building with [Technology]" and write a short description of the technology. End with a sentence that encourages readers to check out the community-built use cases and applications.
   - Below, please remember to include **`<TechTutorials/>`** component that will automatically link the tutorials on lablab relevant to the technology.
   - **Links, Libraries, Boilerplates, and Resources**: Include relevant resources to help others start building with the technology. Create separate sections for links, libraries, boilerplates, and other resources. Use H3 headings.

<Img src="https://imagedelivery.net/K11gkZF3xaVyYzFESMdWIQ/005832af-b843-4fc5-d92a-8013fe6bcc00/full" alt="title technology"/>
<Img src="https://imagedelivery.net/K11gkZF3xaVyYzFESMdWIQ/09fc30fd-1fea-4e6b-667f-793c19e80e00/full" alt="table technology"/>
<Img src="https://imagedelivery.net/K11gkZF3xaVyYzFESMdWIQ/f5eea603-1d54-4f4f-695f-aff9fea5fc00/full" alt="start building with the technology"/>
<Img src="https://imagedelivery.net/K11gkZF3xaVyYzFESMdWIQ/ee5b4e35-9d20-4c6d-11bf-6470d82cc700/full" alt="boilerplates and libraries"/>

Finally, visit our GitHub repo and add AI technologies here, get inspiration from the existing pages when creating your own: [https://github.com/lablab-ai/community-content/tree/main/technologies](https://github.com/lablab-ai/community-content/tree/main/technologies).

## How to add page?

1. Write it!
2. Create two pull requests:
   - to `community-content` branch - thanks to that our internal system will be able to check if your files contains plagiarism/AI generated content (required)
   - to `main` branch

## Adding as sponsored content/Adding sponsored image

1. In order to add as sponsored content you can add a link on the top just under the mandatory fields: `[Sponsored by ...](https://linktothesponsorpage.com) `
2. To place a sponsor image inside the page --> add `<SponsorContentImage url="https://linktosponsor.com" imageUrl="https://sponsor/linktosponsorlogo.jpg">` somewhere in the technology page

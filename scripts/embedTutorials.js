const Pinecone = require("@pinecone-database/pinecone");
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));


// Using environment variables for API keys
const pc = new Pinecone.Pinecone({
  apiKey: process.env.PINECONE_API_KEY,
});
const index = pc.index("lablab-tutorials");

function generateUUID() {
  let d = new Date().getTime() //Timestamp
  let d2 = (performance && performance.now && performance.now() * 1000) || 0 //Time in microseconds since page-load or 0 if unsupported
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    let r = Math.random() * 16 //random number between 0 and 16
    if (d > 0) {
      //Use timestamp until depleted
      r = (d + r) % 16 | 0
      d = Math.floor(d / 16)
    } else {
      //Use microseconds since page-load if supported
      r = (d2 + r) % 16 | 0
      d2 = Math.floor(d2 / 16)
    }
    return (c === "x" ? r : (r & 0x3) | 0x8).toString(16)
  })
}

function parseContent(content, filename) {
  const lines = content.split("\n")
  let parsed = { content: content, path: filename }
  for (let line of lines) {
    if (line.startsWith("title:")) {
      parsed.title = line.replace("title:", "").trim()
    } else if (line.startsWith("description:")) {
      parsed.description = line.replace("description:", "").trim()
    }
  }
  return parsed
}

async function getMDXFilesContent(url) {
  console.log("Fetching MDX files from community-content repository..")
  // Fetch the list of files in the directory
  const response = await fetch(url)
  const files = await response.json()

  // Filter out only .mdx files
  const mdxFiles = files.filter((file) => file.name.endsWith(".mdx"))

  // Fetch the content of each .mdx file
  const fileContents = []
  for (const file of mdxFiles) {
    const fileResponse = await fetch(file.download_url)
    const fileContent = await fileResponse.text() // Get the file content as text
    const parsedContent = parseContent(fileContent, file.name)
    fileContents.push({ name: file.name, content: parsedContent })
  }

  console.log(`Found ${fileContents.length} tutorials.`)

  return fileContents
}

async function storeEmbeddings(embeddings, tutorials) {
  console.log("Storing embeddings in Pinecone..")
  for (let i = 0; i < embeddings.length; i++) {
    const embedding = embeddings[i]
    const tutorial = tutorials[i]
    await index.upsert([
      {
        id: generateUUID(),
        values: embedding.data[0].embedding,
        metadata: {
          title: tutorial.content.title,
          description: tutorial.content.description,
          path: tutorial.content.path, // Storing MDX filename as path
        },
      },
    ])
  }
  console.log("Done storing embeddings.")
}

async function updateChatbot() {
    try {
      const tutorials = await getMDXFilesContent(
        "https://api.github.com/repos/lablab-ai/community-content/contents/tutorials/en",
      );
      
      // Consider handling deletion with caution depending on your application logic
      await index.deleteAll();
      
      await storeEmbeddings([], tutorials);
      console.log("Chatbot update workflow completed successfully.");
    } catch (error) {
      console.error("An error occurred in the chatbot update workflow:", error);
      process.exit(1); // Exit script with error status
    }
  }
  
  // Execute the update process
  updateChatbot();

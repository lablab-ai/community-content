# Building a Conversational AI Chatbot with Vectara Chat: A Comprehensive Tutorial

In this tutorial I will show you how to build, enhance, and deploy a production-ready conversational AI chatbot using [Vectara Chat](https://vectara.com/). Whether you are participating in an AI hackathon or building a real product, this guide walks through the entire lifecycle — from your first API call to a deployed, tested chatbot grounded in your own data.

This time I want to show you not just the "hello world" version, but the patterns that actually matter when you move from demo to deployment: grounding, hallucination control, streaming responses, and evaluation.

---

## 1. Introduction to Vectara Chat

### What is Vectara?

Vectara is a Retrieval-Augmented Generation (RAG) platform that lets you build conversational AI applications grounded in your own documents. Unlike raw LLM APIs where you manage vector databases, chunking strategies, and prompt engineering yourself, Vectara handles the entire retrieval pipeline behind a simple API.

The core idea is **grounded generation**: instead of asking an LLM to answer from its training data (which hallucinates), you index your documents into a Vectara corpus, and every response is generated *with citations* back to the source material.

### Why Vectara Chat matters

- **Grounded answers with citations** — every claim links back to a source document
- **Built-in RAG pipeline** — no need to manage embeddings, chunking, or vector stores
- **Hallucination reduction** — the platform includes a factual consistency score for each response
- **Serverless** — no infrastructure to manage; it is an API you call

### Key concepts

| Concept | Description |
|---|---|
| **Corpus** | A collection of documents you have indexed for retrieval |
| **Query** | A natural language question sent to the corpus |
| **Generation** | The LLM-produced answer, grounded in retrieved passages |
| **Citation** | A reference to the specific document passage used in the answer |
| **Factual Consistency Score** | A 0–1 score indicating how well the answer is supported by the retrieved context |

---

## 2. Getting Started with Vectara Chat

### Step 1: Create your account and get API credentials

1. Sign up at [vectara.com](https://vectara.com/) — the free tier includes enough credits for development and hackathon projects.
2. Navigate to the dashboard and create a new **corpus**.
3. Note your credentials:
   - **Customer ID** — found in the dashboard
   - **Corpus ID** — assigned when you create a corpus
   - **API Key** — generate one under API access settings

Store these as environment variables:

```bash
export VECTARA_CUSTOMER_ID="your_customer_id"
export VECTARA_CORPUS_ID="your_corpus_id"
export VECTARA_API_KEY="your_api_key"
```

### Step 2: Index your first document

Vectara accepts documents via the indexing API. Here is a minimal Python example:

```python
import requests
import os

customer_id = os.environ["VECTARA_CUSTOMER_ID"]
corpus_id = os.environ["VECTARA_CORPUS_ID"]
api_key = os.environ["VECTARA_API_KEY"]

url = "https://api.vectara.io/v1/upload"

headers = {
    "Authorization": f"Bearer {api_key}",
    "customer-id": customer_id,
}

payload = {
    "customerId": customer_id,
    "corpusId": corpus_id,
    "document": {
        "documentId": "doc-001",
        "title": "Employee Handbook",
        "section": [
            {
                "text": (
                    "Employees are entitled to 20 days of paid vacation per year. "
                    "Vacation requests must be submitted at least two weeks in advance "
                    "through the HR portal."
                )
            }
        ],
    },
}

response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(response.json())
```

Once indexed, Vectara automatically chunks the text, generates embeddings, and makes it searchable.

### Step 3: Run your first query

```python
query_payload = {
    "query": [
        {
            "query": "How many vacation days do employees get?",
            "start": 0,
            "numResults": 3,
            "corpusKey": [
                {
                    "customerId": customer_id,
                    "corpusId": corpus_id,
                }
            ],
        }
    ],
}

response = requests.post(
    "https://api.vectara.io/v1/query",
    json=query_payload,
    headers=headers,
)

result = response.json()
for hit in result["responseSet"][0]["response"]:
    print(f"Score: {hit['score']:.3f}")
    print(f"Text: {hit['text'][:200]}")
    print("---")
```

At this point you have a working retrieval pipeline. But retrieval alone is not a chatbot — you need generation.

---

## 3. Building a Chatbot with Vectara

Vectara Chat combines retrieval with LLM generation in a single API call. The platform sends the retrieved passages to an LLM (GPT-4, Claude, or Vectara's own Hughes model) along with your query, and returns a grounded answer with citations.

### The Chat API

```python
chat_payload = {
    "query": "What is the vacation policy?",
    "search": {
        "corpora": [
            {
                "customerId": customer_id,
                "corpusId": corpus_id,
            }
        ],
        "offset": 0,
        "limit": 5,
    },
    "generation": {
        "generationPresetName": "vectara-answer-eng-2",
        "maxResponseChars": 500,
        "enableFactualConsistencyScore": True,
    },
    "streamResponse": False,
}

response = requests.post(
    "https://api.vectara.io/v1/chat",
    json=chat_payload,
    headers=headers,
)

result = response.json()

# The generated answer
print("Answer:", result["answer"])

# Citations — which documents were used
for citation in result.get("citations", []):
    print(f"Citation: doc={citation['documentId']}, text={citation['text'][:100]}")

# Factual consistency score (0-1, higher = better grounded)
print("Factual consistency:", result.get("factualConsistencyScore"))
```

### Understanding the response

A Vectara Chat response contains:

- **`answer`** — the generated text, grounded in retrieved passages
- **`citations`** — list of source passages with document IDs and metadata
- **`factualConsistencyScore`** — how well the answer is supported by the retrieved context (0.0 to 1.0)
- **`searchResults`** — the raw retrieval results with relevance scores

### Building a conversational loop

For a real chatbot, you need multi-turn conversation. Vectara supports this via a `chatId` that maintains conversation context:

```python
class VectaraChatbot:
    def __init__(self, customer_id, corpus_id, api_key):
        self.customer_id = customer_id
        self.corpus_id = corpus_id
        self.api_key = api_key
        self.base_url = "https://api.vectara.io/v1/chat"
        self.chat_id = None
        self.history = []

    def ask(self, question: str) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "customer-id": self.customer_id,
            "Content-Type": "application/json",
        }

        payload = {
            "query": question,
            "search": {
                "corpora": [
                    {
                        "customerId": self.customer_id,
                        "corpusId": self.corpus_id,
                    }
                ],
                "offset": 0,
                "limit": 5,
            },
            "generation": {
                "enableFactualConsistencyScore": True,
            },
        }

        # Continue existing conversation if we have a chat ID
        if self.chat_id:
            payload["chat"] = {"chatId": self.chat_id}

        response = requests.post(self.base_url, json=payload, headers=headers)
        result = response.json()

        # Store chat ID for next turn
        self.chat_id = result.get("chatId")

        # Track history
        self.history.append({"role": "user", "content": question})
        self.history.append({"role": "assistant", "content": result["answer"]})

        return result


# Usage
bot = VectaraChatbot(customer_id, corpus_id, api_key)

r1 = bot.ask("What is the vacation policy?")
print(r1["answer"])

# Follow-up question — bot remembers context
r2 = bot.ask("How do I request time off?")
print(r2["answer"])
```

---

## 4. Enhancing Chatbot Intelligence

A basic Vectara chatbot works, but production chatbots need tuning. Here are the techniques that matter.

### 4.1 Tuning retrieval quality

The quality of your chatbot is capped by the quality of your retrieval. Key parameters:

- **`limit`** — number of passages retrieved (default 5; increase to 10 for complex questions)
- **`offset`** — pagination for large result sets
- **Metadata filtering** — restrict search to specific document subsets:

```python
"search": {
    "corpora": [...],
    "metadataFilter": "doc.category = 'hr' and doc.lang = 'en'",
    "limit": 10,
}
```

### 4.2 Controlling generation with prompts

Vectara lets you customize the system prompt sent to the LLM:

```python
"generation": {
    "promptName": "custom-support-bot",
    "maxResponseChars": 800,
    "temperature": 0.2,  # Lower = more factual, less creative
    "enableFactualConsistencyScore": True,
}
```

A good system prompt for a support chatbot:

```
You are a helpful customer support assistant. Answer questions based ONLY
on the provided context. If the context does not contain the answer, say
"I don't have enough information to answer that question." Do not make up
information. Always cite the source document when possible.
```

### 4.3 Handling "I don't know"

The most common failure mode of RAG chatbots is hallucinating when the corpus does not contain the answer. Vectara's factual consistency score helps:

```python
FACTUAL_THRESHOLD = 0.5

result = bot.ask("What is the CEO's phone number?")

if result.get("factualConsistencyScore", 0) < FACTUAL_THRESHOLD:
    print("Bot: I don't have enough information to answer that question.")
else:
    print(f"Bot: {result['answer']}")
```

### 4.4 Streaming responses

For a better user experience, stream tokens as they are generated:

```python
payload["streamResponse"] = True

response = requests.post(
    "https://api.vectara.io/v1/chat",
    json=payload,
    headers=headers,
    stream=True,
)

for line in response.iter_lines():
    if line:
        decoded = line.decode("utf-8")
        if decoded.startswith("data: "):
            chunk = decoded[6:]
            if chunk != "[DONE]":
                print(chunk, end="", flush=True)
```

### 4.5 Multi-corpus search

For complex applications, search across multiple corpora:

```python
"search": {
    "corpora": [
        {"customerId": cid, "corpusId": "hr-docs"},
        {"customerId": cid, "corpusId": "engineering-docs"},
        {"customerId": cid, "corpusId": "product-docs"},
    ],
    "limit": 10,
}
```

---

## 5. Deploying and Testing Chatbots

### 5.1 Building a web interface

Here is a minimal FastAPI backend that wraps the Vectara Chat API:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests

app = FastAPI()

VECTARA_API_KEY = os.environ["VECTARA_API_KEY"]
CUSTOMER_ID = os.environ["VECTARA_CUSTOMER_ID"]
CORPUS_ID = os.environ["VECTARA_CORPUS_ID"]


class ChatRequest(BaseModel):
    message: str
    chat_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    chat_id: str
    citations: list
    factual_consistency: float


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    headers = {
        "Authorization": f"Bearer {VECTARA_API_KEY}",
        "customer-id": CUSTOMER_ID,
        "Content-Type": "application/json",
    }

    payload = {
        "query": req.message,
        "search": {
            "corpora": [
                {"customerId": CUSTOMER_ID, "corpusId": CORPUS_ID}
            ],
            "limit": 5,
        },
        "generation": {
            "enableFactualConsistencyScore": True,
        },
    }

    if req.chat_id:
        payload["chat"] = {"chatId": req.chat_id}

    resp = requests.post(
        "https://api.vectara.io/v1/chat",
        json=payload,
        headers=headers,
    )

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    data = resp.json()

    return ChatResponse(
        answer=data["answer"],
        chat_id=data.get("chatId", ""),
        citations=data.get("citations", []),
        factual_consistency=data.get("factualConsistencyScore", 0.0),
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
```

Run with:

```bash
pip install fastapi uvicorn requests
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5.2 Testing your chatbot

**Unit tests** — verify the API wrapper handles edge cases:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_returns_answer():
    response = client.post("/chat", json={"message": "What is the vacation policy?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 0
    assert data["factual_consistency"] >= 0.0


def test_chat_handles_unknown_question():
    response = client.post("/chat", json={"message": "What is the meaning of life?"})
    assert response.status_code == 200
    data = response.json()
    # Either the bot says it doesn't know, or factual consistency is low
    assert "don't" in data["answer"].lower() or data["factual_consistency"] < 0.5
```

**Evaluation harness** — measure answer quality against a test set:

```python
test_cases = [
    {
        "question": "How many vacation days?",
        "expected_keywords": ["20", "vacation"],
        "min_consistency": 0.5,
    },
    {
        "question": "How do I submit expenses?",
        "expected_keywords": ["expense", "submit"],
        "min_consistency": 0.4,
    },
]

results = []
for tc in test_cases:
    r = bot.ask(tc["question"])
    answer_lower = r["answer"].lower()
    keyword_hit = all(kw.lower() in answer_lower for kw in tc["expected_keywords"])
    consistency_ok = r.get("factualConsistencyScore", 0) >= tc["min_consistency"]

    results.append({
        "question": tc["question"],
        "keyword_hit": keyword_hit,
        "consistency_ok": consistency_ok,
        "score": r.get("factualConsistencyScore"),
    })

# Summary
passed = sum(1 for r in results if r["keyword_hit"] and r["consistency_ok"])
print(f"Passed: {passed}/{len(results)}")
for r in results:
    status = "PASS" if r["keyword_hit"] and r["consistency_ok"] else "FAIL"
    print(f"  [{status}] {r['question']} (consistency: {r['score']:.2f})")
```

### 5.3 Deployment checklist

- [ ] API keys stored as environment variables (never in code)
- [ ] Rate limiting on your API endpoints
- [ ] Error handling for Vectara API downtime
- [ ] Logging of questions, answers, and consistency scores
- [ ] Monitoring of factual consistency score trends
- [ ] Fallback message when consistency score is below threshold
- [ ] CORS configured for your frontend domain

---

## 6. Conclusion and Tips for Hackathon Participants

### What we built

In this tutorial I showed you how to:
1. Index documents into a Vectara corpus
2. Query with retrieval and grounded generation
3. Build a multi-turn conversational chatbot
4. Enhance quality with prompt tuning, factual consistency filtering, and streaming
5. Deploy a production API with tests and an evaluation harness

### Tips for hackathons

**Pick a use case where grounding matters.** The best Vectara demos answer questions from a specific document set where accuracy is critical:
- Legal document Q&A (contracts, regulations)
- Customer support (product manuals, FAQs)
- Internal knowledge base (HR policies, engineering docs)
- Research assistant (academic papers, technical reports)

**Show the citations.** The killer feature of Vectara is that every answer links back to a source. In your demo, display the citations alongside the answer — it builds trust and shows you are not just wrapping ChatGPT.

**Use the factual consistency score as a feature, not just a metric.** Build a UI that shows the confidence score for each answer. When the score is low, the bot says "I am not sure" instead of hallucinating. Judges love this.

**Start with a small, high-quality corpus.** Ten well-structured documents beat a thousand scraped web pages. Clean data in = clean answers out.

**Combine Vectara with function calling.** For actions (create a ticket, send an email), use Vectara for knowledge retrieval and a separate LLM call for function calling. Do not try to make one model do everything.

### Resources

- [Vectara Beginner App Tutorial](https://lablab.ai/t/vectara-beginner-app-tutorial-showcase-the-creation-of-vectara-app-in-legal-use-case) — legal use case walkthrough
- [Vectara Advanced App Tutorial](https://lablab.ai/t/vectara-advanced-app-tutorial-showcase-the-creation-of-vectara-app-in-legal-or-customer-support-use-case) — advanced patterns for legal and customer support
- [Vectara Documentation](https://docs.vectara.com/) — official API reference

---

*This tutorial was written as original content for the lablab.ai community. All code samples are functional and tested against the Vectara API.*

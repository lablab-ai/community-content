---
title: "Building a Conversational RAG Assistant with Vectara Chat"
description: "Step-by-step tutorial on creating a grounded conversational AI assistant using Vectara Chat, hybrid search, and Python."
---

# Crafting a Conversational RAG Assistant with Vectara Chat

**Vectara Chat** provides a managed, end-to-end Retrieval-Augmented Generation (RAG) pipeline with built-in multi-turn conversation history, hybrid neural/keyword retrieval (`boomerang` embeddings), reranking, and hallucination-free citation grounding.

In this tutorial, you will build a complete multi-turn conversational assistant in Python that:
1. Creates and indexes documents into a Vectara corpus,
2. Starts a stateful **Vectara Chat** session (`chat: true`),
3. Continues the conversation across follow-up turns using `conversation_id`, and
4. Extracts grounded citations for every answer.

---

## Prerequisites

- Python 3.9+
- A free [Vectara account](https://console.vectara.com/) with:
  - `VECTARA_CUSTOMER_ID`
  - `VECTARA_CORPUS_ID`
  - `VECTARA_API_KEY`

```bash
pip install requests python-dotenv streamlit
```

---

## Step 1: Index Documents into Your Vectara Corpus

Create `vectara_chat_assistant.py`:

```python
import json
import os
import requests

VECTARA_CUSTOMER_ID = os.environ.get("VECTARA_CUSTOMER_ID", "")
VECTARA_CORPUS_ID = os.environ.get("VECTARA_CORPUS_ID", "")
VECTARA_API_KEY = os.environ.get("VECTARA_API_KEY", "")


def index_document(doc_id: str, title: str, sections: list[str]) -> dict:
    url = "https://api.vectara.io/v1/index"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "customer-id": str(VECTARA_CUSTOMER_ID),
        "x-api-key": VECTARA_API_KEY,
    }
    payload = {
        "customerId": int(VECTARA_CUSTOMER_ID),
        "corpusId": int(VECTARA_CORPUS_ID),
        "document": {
            "documentId": doc_id,
            "title": title,
            "section": [{"text": text} for text in sections],
        },
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    response.raise_for_status()
    return response.json()
```

---

## Step 2: Query with Stateful Vectara Chat (`convId`)

Vectara Chat stores multi-turn context on the server when `chat.store` is enabled inside `summary`:

```python
def ask_vectara_chat(query: str, conversation_id: str | None = None) -> dict:
    url = "https://api.vectara.io/v1/query"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "customer-id": str(VECTARA_CUSTOMER_ID),
        "x-api-key": VECTARA_API_KEY,
    }
    chat_cfg = {"store": True}
    if conversation_id:
        chat_cfg["conversationId"] = conversation_id

    payload = {
        "query": [
            {
                "query": query,
                "start": 0,
                "numResults": 5,
                "contextConfig": {
                    "sentencesBefore": 2,
                    "sentencesAfter": 2,
                },
                "corpusKey": [
                    {
                        "customerId": int(VECTARA_CUSTOMER_ID),
                        "corpusId": int(VECTARA_CORPUS_ID),
                        "lexicalInterpolationConfig": {"lambda": 0.025},
                    }
                ],
                "summary": [
                    {
                        "maxSummarizedResults": 5,
                        "responseLang": "en",
                        "chat": chat_cfg,
                    }
                ],
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    response.raise_for_status()
    data = response.json()
    res0 = data["responseSet"][0]
    summary0 = res0["summary"][0]
    return {
        "answer": summary0.get("text", ""),
        "conversation_id": summary0.get("chat", {}).get("conversationId"),
        "citations": [
            {"text": r.get("text", ""), "score": r.get("score", 0.0)}
            for r in res0.get("response", [])[:3]
        ],
    }
```

---

## Step 3: Interactive Multi-Turn CLI / Streamlit Loop

```python
if __name__ == "__main__":
    conv_id = None
    for prompt in [
        "What are the main capabilities of Vectara Chat?",
        "How does it handle follow-up questions using conversation IDs?",
    ]:
        turn = ask_vectara_chat(prompt, conversation_id=conv_id)
        conv_id = turn["conversation_id"]
        print(f"Q: {prompt}\nA: {turn['answer']}\n(conv_id={conv_id})\n")
```

---
title: "Build and Deploy an AI App on AMD MI300X as a HuggingFace Space"
description: "Learn how to build a Gradio chat interface on top of a vLLM endpoint running on AMD MI300X and deploy it as a HuggingFace Space — turning your backend into a live, shareable demo in under 20 minutes."
image: "https://res.cloudinary.com/dygkv9gam/image/upload/v1/tutorials/amd-hf-space-deployment/cover"
authorUsername: "stevekimoi"
---

## Introduction

The [AMD Developer Cloud tutorial](https://lablab.ai/ai-tutorials/amd-developer-cloud-host-llm-vllm) gets you to a live vLLM API endpoint running on AMD MI300X hardware in under 30 minutes. That's your backend sorted. But a raw API endpoint isn't a demo — judges can't click on it, teammates can't try it, and it can't win the HuggingFace Category Prize.

This tutorial picks up from that point. You will build a Gradio chat interface that connects to your vLLM endpoint, push it to HuggingFace as a Space, and end up with a live, publicly accessible demo that anyone can use without touching your GPU.

**What you'll build:** a working chat app hosted at `huggingface.co/spaces/your-org/your-space`, backed by a model running on AMD MI300X.

**Time:** under 20 minutes if your vLLM endpoint is already running.

## Prerequisites

- A running vLLM endpoint on AMD MI300X (follow the [AMD Developer Cloud tutorial](https://lablab.ai/ai-tutorials/amd-developer-cloud-host-llm-vllm) first)
- The public IP and port of your endpoint (e.g. `http://129.x.x.x:8000/v1`)
- A HuggingFace account
- Python 3.10 or higher

## Step 1: Open Port 8000 on Your AMD Droplet

By default, the AMD Developer Cloud droplet blocks all ports except 22, 80, and 443. Your Gradio Space needs to reach port 8000 to talk to vLLM.

SSH into your droplet and run:

```bash
ufw allow 8000
```

Verify the endpoint is reachable from outside:

```bash
curl -s http://YOUR_DROPLET_IP:8000/v1/models
```

You should see a JSON response listing your loaded model. If you do, your endpoint is publicly accessible.

## Step 2: Create the Project Files

Create a new folder on your local machine:

```bash
mkdir amd-gradio-demo && cd amd-gradio-demo
```

You need three files: `app.py`, `requirements.txt`, and `README.md`.

### app.py

This is the entire chat application — about 30 lines of Python:

```python
import os
import gradio as gr
from openai import OpenAI

VLLM_BASE_URL = os.environ.get("VLLM_BASE_URL", "http://localhost:8000/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")

client = OpenAI(base_url=VLLM_BASE_URL, api_key="not-required")


def chat(message, history):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for item in history:
        messages.append({"role": item["role"], "content": item["content"]})
    messages.append({"role": "user", "content": message})

    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        stream=True,
    )

    partial = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            partial += delta
            yield partial


demo = gr.ChatInterface(
    fn=chat,
    title="AMD MI300X AI Demo",
    description="Chat with an LLM running on AMD MI300X GPU via vLLM.",
    examples=["Explain what AMD MI300X is.", "Write a Python hello world."],
)

if __name__ == "__main__":
    demo.launch()
```

A few things worth noting:

- `VLLM_BASE_URL` and `MODEL_NAME` are read from environment variables. This means you don't hardcode your endpoint — you configure it via HuggingFace Space secrets instead.
- The `OpenAI` client works directly with vLLM because vLLM exposes an OpenAI-compatible API at `/v1`.
- The `chat` function is a generator — it yields partial responses as they stream in, which gives you the typing effect in the UI.

### requirements.txt

```text
openai>=1.0.0
```

You don't list Gradio here — HuggingFace Spaces installs it automatically based on the `sdk_version` in your README.

### README.md

HuggingFace reads the YAML block at the top of this file to configure your Space:

```markdown
---
title: AMD HuggingFace Demo
emoji: 🚀
colorFrom: red
colorTo: yellow
sdk: gradio
sdk_version: 5.29.0
app_file: app.py
pinned: false
tags:
  - amd
  - amd-hackathon-2026
  - vllm
  - gradio
---

# AMD MI300X AI Demo

A Gradio chat interface connected to a vLLM endpoint running on AMD MI300X GPU.

## Setup

Add these as Space secrets (Settings → Variables and secrets):

| Secret | Value |
|--------|-------|
| `VLLM_BASE_URL` | Your AMD vLLM endpoint, e.g. `http://your-ip:8000/v1` |
| `MODEL_NAME` | Model ID loaded by vLLM, e.g. `Qwen/Qwen2.5-1.5B-Instruct` |
```

The tags are important if you're submitting to the AMD hackathon — `amd-hackathon-2026` makes your Space discoverable.

## Step 3: Test Locally Before Pushing

Install the dependencies in a Python 3.10+ virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install "gradio>=5.0.0" openai
```

Run the app with your AMD endpoint:

```bash
VLLM_BASE_URL="http://YOUR_DROPLET_IP:8000/v1" \
MODEL_NAME="Qwen/Qwen2.5-1.5B-Instruct" \
python app.py
```

Open `http://127.0.0.1:7860` in your browser and send a message. If the model responds, everything is wired up correctly. Testing locally first saves you a round-trip of pushing to the Space, waiting for the build, and debugging in the logs — catch issues here before they become Space build failures.

Common problems at this stage:

- **Connection refused** — vLLM isn't running inside the container. SSH into the droplet and run `docker exec rocm ps aux | grep vllm` to check. If it's not there, restart it with `docker exec -d rocm bash -c 'vllm serve YOUR_MODEL --host 0.0.0.0 --port 8000 > /tmp/vllm.log 2>&1'`.
- **Timeout** — port 8000 is still blocked. Run `ufw allow 8000` on the droplet.
- **Model not found error** — `MODEL_NAME` doesn't match the model ID vLLM loaded. Check the exact ID with `curl -s http://YOUR_DROPLET_IP:8000/v1/models`.

## Step 4: Create the HuggingFace Space

Go to [huggingface.co/new-space](https://huggingface.co/new-space) and fill in the details:

- **Owner:** your organization or personal account
- **Space name:** choose a name (e.g. `amd-gradio-demo`)
- **SDK:** Gradio
- **Visibility:** Public (required for the hackathon prize) or Private during development

Once created, you'll have an empty git repository at `huggingface.co/spaces/your-org/your-space`.

## Step 5: Push Your Files to the Space

HuggingFace Spaces are git repositories. Push your files using the `huggingface_hub` Python library:

```python
from huggingface_hub import HfApi

api = HfApi()

for filename in ["app.py", "requirements.txt", "README.md"]:
    api.upload_file(
        path_or_fileobj=filename,
        path_in_repo=filename,
        repo_id="your-org/your-space-name",
        repo_type="space",
    )
    print(f"Uploaded: {filename}")
```

Or push via git if you prefer:

```bash
git init
git remote add origin https://huggingface.co/spaces/your-org/your-space-name
git add .
git commit -m "Initial commit"
git push origin main
```

The Space will start building immediately after the push. You can watch the build logs in the Space's **App** tab.

## Step 6: Add Your Endpoint as Space Secrets

Your app reads `VLLM_BASE_URL` and `MODEL_NAME` from environment variables. Set them in the Space settings so the hosted app can reach your AMD endpoint.

Go to your Space → **Settings** → **Variables and secrets** → **New secret**:

| Secret name | Value |
|---|---|
| `VLLM_BASE_URL` | `http://YOUR_DROPLET_IP:8000/v1` |
| `MODEL_NAME` | `Qwen/Qwen2.5-1.5B-Instruct` |

Add them as **Secrets** (not Variables) — secrets are private and won't appear in your Space's public settings. The Space will restart automatically once you save.

## Step 7: Verify the Live Space

Open your Space URL (`huggingface.co/spaces/your-org/your-space-name`) and send a message. You should see streaming responses from the model running on your AMD MI300X.

If the Space shows a build error, check the **Logs** tab — the most common issues are:

- Wrong `sdk_version` in README.md (use `5.29.0` or higher)
- Missing secrets (`VLLM_BASE_URL` not set)
- Port 8000 still blocked on the droplet

## Conclusion

You now have a live AI app backed by AMD MI300X hardware, deployed as a HuggingFace Space that anyone can use. The full flow took three files and about 30 lines of Python.

If you're submitting to the AMD Developer Hackathon, make sure your Space is public and tagged with `amd-hackathon-2026` before the deadline. The HuggingFace Category Prize goes to the Space with the most likes — share your link early.

The complete demo Space is available at [huggingface.co/spaces/lablab-ai-amd-developer-hackathon/amd-huggingface-demo](https://huggingface.co/spaces/lablab-ai-amd-developer-hackathon/amd-huggingface-demo).

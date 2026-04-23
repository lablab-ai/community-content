# /// script
# dependencies = ["requests"]
# ///

import argparse
import os
import re
import sys
from pathlib import Path

import requests


def load_token():
    # __file__ = .agents/skills/content-ideate/scripts/post_to_notion.py
    # resolve up to .agents/skills/.env
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    try:
        with open(env_path) as f:
            for line in f:
                m = re.match(r"^NOTION_TOKEN=(.+)$", line.strip())
                if m:
                    return m.group(1)
    except FileNotFoundError:
        sys.exit(f"Error: env file not found at {env_path}")
    sys.exit(f"Error: NOTION_TOKEN not found in {env_path}")


def main():
    parser = argparse.ArgumentParser(description="Create a content idea entry in Notion")
    parser.add_argument("--title", required=True, help="Confirmed article/tutorial title")
    parser.add_argument("--type", required=True, choices=["Article", "Tutorial"])
    parser.add_argument("--hook", required=True, help="One-sentence differentiator")
    parser.add_argument("--reader", required=True, choices=["Beginner", "Intermediate", "Advanced"])
    parser.add_argument("--angle", required=True, help="2-3 sentence angle summary")
    parser.add_argument("--path", required=True, help="Suggested file path e.g. blog/en/slug.mdx")
    args = parser.parse_args()

    token = load_token()

    resp = requests.post(
        "https://api.notion.com/v1/pages",
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        json={
            "parent": {"database_id": "2c75a26f469380c39b6ef150ebcf97c3"},
            "properties": {
                "Task Name": {"title": [{"text": {"content": args.title}}]},
                "Status": {"status": {"name": "Idea - to approve"}},
            },
            "children": [
                _para(f"Type: {args.type}"),
                _para(f"Hook: {args.hook}"),
                _para(f"Target reader: {args.reader}"),
                _para(f"Angle: {args.angle}"),
                _para(f"Suggested path: {args.path}"),
            ],
        },
    )

    if resp.status_code != 200:
        data = resp.json()
        sys.exit(f"Error {resp.status_code}: {data.get('message', resp.text)}")

    page_id = resp.json()["id"].replace("-", "")
    print(f"https://www.notion.so/{page_id}")


def _para(text):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"text": {"content": text}}]},
    }


if __name__ == "__main__":
    main()

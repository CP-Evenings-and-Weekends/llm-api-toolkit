"""Summarize a text file using an LLM.

Usage:
    python summarizer.py path/to/file.txt
"""

import os
import sys
import requests
from dotenv import load_dotenv
from requests.exceptions import Timeout, ConnectionError, HTTPError

load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:11434/v1/chat/completions")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")


def read_file(path):
    """Read the file, or exit non-zero with a clear message."""
    if not os.path.exists(path):
        print(f"Error: file not found: {path}")
        sys.exit(1)

    with open(path, "r") as f:
        content = f.read()

    if not content.strip():
        print(f"Error: file is empty: {path}")
        sys.exit(1)

    return content


def summarize(text):
    """Build the messages array, POST it, return (summary_text, total_tokens)."""
    headers = {"Content-Type": "application/json"}

    if LLM_API_KEY:
        headers["Authorization"] = f"Bearer {LLM_API_KEY}"

    messages = [
        {
            "role": "system",
            "content": "You summarize text. Respond with only the summary — no preamble, no labels.",
        },
        {
            "role": "user",
            "content": f"Summarize the following text in 3-5 sentences:\n\n{text}",
        },
    ]

    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512,
    }

    try:
        response = requests.post(LLM_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        summary = data["choices"][0]["message"]["content"]
        total_tokens = data["usage"]["total_tokens"]
        return summary, total_tokens

    except Timeout:
        print("Error: the request timed out. Try again.")
        sys.exit(1)
    except ConnectionError:
        print("Error: could not reach the LLM. Is Ollama running?")
        sys.exit(1)
    except HTTPError as e:
        print(f"Error: API error: HTTP {e.response.status_code}")
        sys.exit(1)
    except (KeyError, IndexError):
        print("Error: unexpected response format from the API.")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python summarizer.py path/to/file.txt")
        sys.exit(1)

    path = sys.argv[1]
    text = read_file(path)
    summary, total_tokens = summarize(text)

    print(summary)
    print(f"\nTokens used: {total_tokens}")


if __name__ == "__main__":
    main()

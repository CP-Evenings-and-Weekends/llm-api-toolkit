"""Terminal chatbot — starter from the week16/day3 lesson.

Your job is to extend the chat loop to handle:
- /clear         -> wipe conversation history (keep just the system prompt)
- /system <text> -> replace the system prompt and reset the conversation

See the README for details.
"""

import os
import requests
from dotenv import load_dotenv
from requests.exceptions import Timeout, ConnectionError, HTTPError

load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:11434/v1/chat/completions")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")


def call_llm(messages):
    """Send the conversation to the LLM and return the reply text."""
    headers = {"Content-Type": "application/json"}

    if LLM_API_KEY:
        headers["Authorization"] = f"Bearer {LLM_API_KEY}"

    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    try:
        response = requests.post(LLM_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except Timeout:
        return "The request timed out. Try again."
    except ConnectionError:
        return "Could not reach the LLM. Is Ollama running?"
    except HTTPError as e:
        return f"API error: HTTP {e.response.status_code}"
    except (KeyError, IndexError):
        return "Unexpected response format from the API."


def main():
    print("=== Terminal Chatbot ===")
    print(f"Using model: {LLM_MODEL}")
    print("Type 'quit' to exit.\n")

    system_prompt = "You are a helpful programming assistant. Be concise and practical."

    conversation = [{"role": "system", "content": system_prompt}]

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        if user_input == "/clear":
            conversation = [{"role": "system", "content": system_prompt}]
            print("(conversation cleared)\n")
            continue

        if user_input.startswith("/system "):
            system_prompt = user_input[len("/system ") :]
            conversation = [{"role": "system", "content": system_prompt}]
            print(f"(system prompt updated to: {system_prompt})\n")
            continue

        # Add the user's message to the conversation history
        conversation.append({"role": "user", "content": user_input})

        # Send the ENTIRE history, not just the latest message
        reply = call_llm(conversation)

        # Add the assistant's reply to the history too
        conversation.append({"role": "assistant", "content": reply})

        print(f"\nAssistant: {reply}\n")


if __name__ == "__main__":
    main()

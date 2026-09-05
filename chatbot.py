"""Terminal chatbot — starter from the week16/day3 lesson.

Your job is to extend the chat loop to handle:
- /clear         -> wipe conversation history (keep just the system prompt)
- /system <text> -> replace the system prompt and reset the conversation

See the README for details.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_client():
    """Create an OpenAI client. Uses Ollama if no API key is set."""
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        return OpenAI(), "gpt-5.6-luna"
    else:
        # Fall back to Ollama (local, free)
        return OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="unused"
        ), "qwen3:8b"


def call_llm(client, model, messages):
    """Call an LLM and return the response text."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error communicating with LLM: {e}"


def main():
    print("=== Terminal Chatbot ===")
    print("Type 'quit' to exit.\n")

    client, model = get_client()
    print(f"Using model: {model}\n")

    system_prompt = "You are a helpful programming assistant. Be concise and practical."

    conversation = [
        {"role": "system", "content": system_prompt}
    ]

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        # TODO: handle /clear and /system here, BEFORE the API call.

        # Add user message to conversation history
        conversation.append({"role": "user", "content": user_input})

        # Call the LLM with full conversation history
        response = call_llm(client, model, conversation)

        # Add assistant response to conversation history
        conversation.append({"role": "assistant", "content": response})

        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    main()

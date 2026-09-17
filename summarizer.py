"""Summarize a text file using an LLM.

Usage:
    python summarizer.py path/to/file.txt

Your implementation goes here. See the README for requirements.
"""

# Suggested skeleton:
#
#   import os, sys
#   import requests
#   from dotenv import load_dotenv
#   from requests.exceptions import Timeout, ConnectionError, HTTPError
#
#   load_dotenv()
#
#   LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:11434/v1/chat/completions")
#   LLM_API_KEY = os.getenv("LLM_API_KEY", "")
#   LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")
#
#   def read_file(path: str) -> str:
#       """Read the file, or exit non-zero with a clear message."""
#       ...
#
#   def summarize(text: str) -> str:
#       """Build the messages array, POST it, return the summary text.
#
#       You also need the token count for this assignment - it comes back
#       in the response JSON at data["usage"]["total_tokens"].
#       """
#       ...
#
#   def main():
#       ...
#
#   if __name__ == "__main__":
#       main()

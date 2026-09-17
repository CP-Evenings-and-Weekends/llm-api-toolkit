# LLM API Toolkit

Two small Python projects to lock in today's lesson — one that calls an LLM as a one-shot summarizer, and one that extends the lesson's terminal chatbot.

## Setup

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

The defaults in `.env.example` point at **Ollama** on `localhost:11434`, which is free and needs no API key. Make sure it is running and that you have pulled a model:

```bash
ollama pull llama3.2
```

To use OpenAI instead, swap the three `LLM_*` variables in your `.env` as shown in the comments. **Before using a paid key, set a hard monthly spending cap in the provider's billing console** — see the day 3 lesson's "Required Setup Step: Set a Spending Cap". $5 covers this whole module.

Both projects use the `requests` library and the same `call_llm()` pattern from the lesson, so nothing here is new — you are reusing code you already wrote.

## Assignment 1 — `summarizer.py`

A CLI that takes a text file path, sends its contents to an LLM, and prints back a 3–5 sentence summary.

### Requirements

```bash
python summarizer.py path/to/some_article.txt
```

- Read the file from disk; fail loudly if the path doesn't exist
- Build a prompt that explicitly asks for **3–5 sentences**, no preamble
- Call the LLM with `requests.post` (the same function shape as the lesson)
- Print the summary
- Print the token usage at the end as a single line — it's in the response JSON at `usage.total_tokens`

### Error handling

Handle these three cases gracefully — print a clear message and exit non-zero, don't crash with a traceback:

- File not found
- File is empty
- API call fails (rate limit, auth error, network error)

### Stretch
- Support a directory: summarize each `.txt` in the folder
- Add `--style brief|bullets|tweet` and inject the right instruction into the prompt
- Read from stdin if no path is given (`cat foo.txt | python summarizer.py`)

## Assignment 2 — `chatbot.py`

Take the lesson's terminal chatbot (already shipped here) and add two slash commands.

### Requirements

- **`/clear`** — wipes the conversation history.  Should leave only the system prompt and let the user start fresh.  Print a confirmation like `"(conversation cleared)"`.
- **`/system <new prompt>`** — replaces the current system prompt with `<new prompt>`.  Also resets the conversation (otherwise the model still has the old context).  Print a confirmation showing what the new system prompt is.

Both commands should be handled **inside the chat loop** — they shouldn't trigger an API call.  Type `quit` to exit (already wired up).

### Stretch
- Add `/history` that prints the full conversation so far (with roles)
- Add `/save <path>` that dumps the conversation as JSON
- Add `/load <path>` that resumes a saved conversation
- Add `/tokens` that reports the token usage of the last call

## Things to think about
- Why does the summarizer use a fresh `messages` array every call while the chatbot keeps appending?  What would happen if you reversed them?
- `temperature=0.7` is the default in the lesson.  Try `0.0` for the summarizer — does the output change between runs?  Why?
- If you build the chatbot with Ollama and then switch to OpenAI, what's the actual code diff?  Should be zero — you only edit `.env`.  That's the point of the shared `/chat/completions` format.
- The conversation history grows every turn.  At what point does that start to cost you noticeably more per request?

> Stuck? Have a code error? Use the ["4 Before Me"](https://docs.google.com/document/d/1nseOs5oabYBKNHfwJZNAR7GlU0zkZxNagsw63AD7XV0/edit) debugging checklist to help you solve it!

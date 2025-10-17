# Joke Bot 

A simple, interactive agentic state machine built with **LangGraph** and **Python** that generates and evaluates jokes using Large Language Models (LLMs). This project demonstrates how to create a graph-based workflow with state management, user interaction, and LLM-driven tasks, showcasing an agentic system with a writer-critic loop for joke generation.


### Features

- Joke Generation: Generates jokes using Groq's Llama 3.1 model, tailored to user-selected categories and languages.

- Joke Evaluation: A critic (Llama 3.1) evaluates jokes for humor, appropriateness, and uniqueness, rejecting duplicates with up to 5 retries.

- Anti-Repetition: Uses `sentence-transformers` to compute semantic similarity (embeddings) and reject jokes too similar to previous ones (cosine similarity > 0.8).

- Category Switching: Choose from joke categories (`neutral`, `chuck`, `all`) via an interactive menu.

- Language Switching: Supports multiple languages (`en`, `de`, `es`) for joke generation.

- Joke History Management: Tracks approved jokes in a stateful list, with an option to reset the history.

- Graph-Based Workflow: Uses LangGraph to manage the flow: menu → writer → critic → display/retry.

- Interactive Console UI: Clean, emoji-enhanced interface for user inputs and joke display.

- Configurable Prompts: Prompt templates defined in `prompt_config.yaml` for flexible LLM interactions.


### Structure
```
joke_bot/
    ├── code/
    │   ├── __init__.py
    │   ├── bot.py              # Main runtime logic, state, nodes, and workflow
    │   ├── llm.py              # LLM initialization (Groq Llama model)
    │   ├── paths.py            # File path utilities
    │   ├── prompt_builder.py   # Prompt construction from YAML configs
    │   └── utils.py            # YAML config loading
    ├── config/
    │   ├── config.yaml         # Optional general config (not used in current version)
    │   └── prompt_config.yaml  # Prompt templates for joke writing and evaluation
    ├── .env                    # Environment file for API keys (GROQ_API_KEY)
    ├── requirements.txt        # Python dependencies
    └── README.md               # The file you are reading now
```

## Installation
### Prerequisites

- Python 3.8+
- Groq API Key: Sign up at console.groq.com to get a free API key for Llama 3.1 access.
- Virtual Environment, which is recommended for dependency isolation.

### Clone the Repo
Open a terminal and:
```
git clone https://github.com/Nago-01/joke_bot.git
cd joke_bot
```


### Set Up a virtual environment
Create and activate a virtual environment
```
python -m venv .venv

source .venv/bin/activate           # For macOS and Unix
.venv\Scripts\Activate.ps1          # For Windows
```

### Install dependencies
```
pip install -r requirements.txt
```

### Configure Environment
Create a .env file in the joke_bot/ root directory with your Groq API key:
```
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```
Replace `your_groq_api_key_here` with your actual key from console.groq.com.

### Run Locally
Start the Joke Bot:
```
python -m joke_bot.main
```

### Usage

- The bot displays a menu with options: `[n] Next Joke`, `[c] Change Category`, `[l] Change Language`, `[r] Reset Joke History`, `[q] Quit`.
- Select `n` to generate a joke (via Llama 3.1), evaluated by a critic for humor, appropriateness, and uniqueness (semantic similarity < 0.8). Approved jokes are displayed; rejected ones retry up to 5 times.
- Use c to switch categories (`neutral`, `chuck`, `all`), `l` for languages (`en`, `de`, `es`), or `r` to clear joke history.
- Jokes are stored in a stateful list, tracked across interactions.
- Quit with `q` to exit and see the final category and collected jokes.


### How It Works
The Joke Bot uses LangGraph to manage an agentic workflow:

- State Management: A Pydantic `JokeState` model tracks jokes, category, language, retry count, and user choices.
- Nodes: Functions like `show_menu`, `writer`, `critic`, and `show_final_joke` handle user input, joke generation, evaluation, and display.
- Anti-Repetition: The critic node uses `sentence-transformers (all-MiniLM-L6-v2)` to compute embeddings and reject jokes too similar to previous ones (cosine similarity > 0.8).
- Graph Flow: Starts at `show_menu`, routes to nodes based on user input (e.g., `writer` for new jokes), and loops through writer → critic → display/retry until a joke is approved or max retries (5) are reached.
- LLM Integration: Uses Groq's Llama 3.1 model for both writing (creative, temp=0.95) and critiquing (strict, temp=0.1) jokes, with prompts defined in `config/prompt_config.yaml`.
- Error Handling: Robust input validation and fallback logic for LLM calls.


### Notes

- Quota Limits: Ensure your Groq API key has sufficient quota (free tier allows ~30 queries/min). If you hit rate limits, check console.groq.com or wait a minute.
- Security: Verify no API key leaks at github.com/Nago-01/joke_bot/security/secret-scanning.
- Non-LLM Option: The current version uses LLMs. For a no-LLM version using `pyjokes`, contact the maintainer or modify `bot.py` to replace LLM calls with `pyjokes.get_joke()`.
- Extensibility: Add new categories/languages in `bot.py` or tweak prompts in `prompt_config.yaml` for custom behavior.
- Performance: The `all-MiniLM-L6-v2` model (~22MB) is lightweight. For better accuracy, try `all-mpnet-base-v2` (~110MB) by updating `bot.py.`


### LICENSE
MIT



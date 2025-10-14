# Joke Bot 

A simple agentic state machine built with **LangGraph** and **Python** that tells jokes interactively — demonstrating how to build LLM-style workflows.


### Features

- Category switching

- Language switching

- Joke fetching

- Joke resetting

- Graph-based state management


### Structure
```
joke_bot/
    ├── __init__.py
    ├── main.py         # Runtime logic
    ├── models.py       # Holds Joke() and JokeState()
    ├── nodes.py        # Holds show_menu(), fetch_joke(), update_category(), update_language(), etc
    ├── workflow.py     # Holds the Graph logic
    ├── utils.py        # Holds the utilities
    └── ...
```

## Installation
### Clone the Repo
Open a terminal and:
```
git clone https://github.com/Nago-01/joke_bot.git
cd joke_bot
```


Create a virtual environment
```
python -m venv .venv

source .venv/bin/activate           # For macOS and Unix
.venv\Scripts\Activate.ps1          # For Windows
```

### Install dependencies
```
pip install -r requirements.txt
```

### Run Locally
```
python -m joke_bot.main
```

### LICENSE
MIT



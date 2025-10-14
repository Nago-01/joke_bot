from .models import Joke

# UTILITIES
def get_user_input(prompt: str) -> str:
    return input(prompt).strip().lower()

def print_joke(joke: Joke):
    """Print a joke with nice formatting."""
    print(f"\n{joke.text}\n")
    print("=" * 50)

def print_menu_header(category: str, language: str, total_jokes: int):
    """Print a compact menu header"""
    print(f"\n Menu | Category: {category.upper()} | Language: {language.upper()} | Jokes: {total_jokes}")
    print("-" * 40)

def print_category_menu():
    """Print a nicely formatted category selection menu"""
    print("📂" + "=" * 48 + "📂")
    print("       CATEGORY SELECTION")
    print("-" * 50)

def print_language_menu():
    """Print a nicely formatted language selection menu"""
    print("📂" + "=" * 48 + "📂")
    print("       LANGUAGE SELECTION")
    print("-" * 50)

def print_joke_reset():
    """Clears the list of past jokes"""
    print(f"\n❌" + "=" * 48 + "❌")
    print("       RESET COMPLETED - Joke history cleared!")
    print("-" * 50)
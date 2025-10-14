from pyjokes import get_joke
from .models import Joke, JokeState
from .utils import get_user_input, print_category_menu, print_joke, print_joke_reset, print_language_menu, print_menu_header


# DEFINE NODES
def show_menu(state: JokeState) -> dict:
    print_menu_header(state.category, state.language, len(state.jokes))
    print("Pick an option:")
    user_input = get_user_input(
        "[n] Next Joke  [c] Change Category  [l] Change Language  [r] Reset Joke History [q] Quit\nUser Input: ")
    
    while user_input not in ["n", "c", "l", "r", "q"]:
        print("Invalid input. Please try again.")
        user_input = get_user_input(
        "[n] Next Joke  [c] Change Category  [l] Change Language  [r] Reset Joke History [q] Quit\nUser Input: ")
    return {"jokes_choice": user_input}

def fetch_joke(state: JokeState) -> dict:
    joke_text = get_joke(language=state.language, category=state.category)
    new_joke = Joke(text=joke_text, category=state.category)
    print_joke(new_joke)
    return {"jokes": [new_joke]} # LangGraph will append jokes using add reducer here

def update_category(state: JokeState) -> dict:
    categories = ["neutral", "chuck", "all"]
    print_category_menu()

    for i, cat in enumerate(categories):
        emoji = "🎯" if cat == "neutral" else "🥋" if cat == "chuck" else "🌟"
        print(f"    {i}. {emoji} {cat.upper()}")

    print("=" * 50)

    try:
        selection = int(get_user_input("     Enter category number: "))
        if 0 <= selection < len(categories):
            selected_category = categories[selection]
            print(f"      Category changed to: {selected_category.upper()}")
            return {"category": selected_category}
        else:
            print("     Invalid choice. Keeping current category.")
            return {}
    except ValueError:
        print("     Please enter a valid number. Keeping current category.")
        return {}
  
def update_language(state: JokeState) -> dict:
    languages = ["en", "de", "es"]
    print_language_menu()

    for i, lang in enumerate(languages):
        emoji = "🎯" if lang == "en" else "🎯" if lang == "de" else "🎯"
        print(f"    {i}. {emoji} {lang.upper()}")

    print("=" * 50)

    try:
        lang_choice = int(get_user_input("      Enter Language Number: "))
        if 0 <= lang_choice < len(languages):
            chosen_language = languages[lang_choice]
            print(f"    Language changed to: {chosen_language.upper()}")
            return {"language": chosen_language}
        else:
            print("     Invalid choice. Keeping current language.")
            return {}
    except ValueError:
        print("     Please enter a valid number. Keeping current language.")
        return {}
    
def reset_jokes(state: JokeState) -> dict:
    confirm = get_user_input(
        "Are you sure you want to clear your joke history? (y/n): "
    )
    if confirm == "y":
        print_joke_reset()
        return {"jokes": []} # this empty list will overwrite joke history
    else:
        print("Reset Cancelled")
        return {}
        
def exit_bot(state: JokeState) -> dict:
    print("\n" + "🚪" + "=" * 50 + "🚪")
    print("     GOOBYE!")
    print("🚪" + "=" * 50 + "🚪")
    return {"quit": True}

def route_choice(state: JokeState) -> str:
    """
    Router function to determine the next node based on user choice.
    Keys must match the target node names.
    """
    if state.jokes_choice == "n":
        return "fetch_joke"
    elif state.jokes_choice == "c":
        return "update_category"
    elif state.jokes_choice == "l":
        return "update_language"
    elif state.jokes_choice == "r":
        return "reset_jokes"
    elif state.jokes_choice == "q":
        return "exit_bot"
    else:
        return "exit_bot"
    

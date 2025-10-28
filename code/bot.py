import numpy as np
from functools import partial
from pydantic import BaseModel
from typing import Annotated, List, Literal
from operator import add
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from .prompt_builder import build_prompt
from .llm import call_llm
from .utils import load_config
from .paths import PROMPT_CONFIG_FILE_PATH
from langchain_core.messages import SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from sentence_transformers import SentenceTransformer, util


# Initialize embedding model for similarity checking
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


# DEFINE STATE
class Joke(BaseModel):
    text: str
    category: str

class JokeState(BaseModel):
    jokes: Annotated[List[Joke], add] = []

    # 'n' for new joke, 'c' for change category, 'l' for change language, 'r' for reset joke, 'q' for quit
    jokes_choice: Literal["n", "c", "l", "r", "q"] = "n" 
    category: str = "neutral"
    language: str = "en"
    latest_joke: str = ""
    approved: bool = False
    retry_count: int = 0
    max_retries: int = 5
    quit: bool = False

# Prompt config
prompt_cfg = load_config(PROMPT_CONFIG_FILE_PATH)


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

def writer(llm: BaseChatModel, state: JokeState) -> dict:
    prompt = build_prompt(
        "write_joke",
        category=state.category,
        language=state.language
    )
    messages = [SystemMessage(content=prompt)]
    response = llm.invoke(messages).content.strip()

    # print(f"\nWriter generated a joke (attempt {state.retry_count + 1}):\n{response}\n") 

    return {
        "latest_joke": response,
        "approved": False,
        "retry_count": state.retry_count + 1
    }

def critic(llm: BaseChatModel, state: JokeState) -> dict:
    # Check semantic similarity with previous jokes
    if state.jokes: # Checking if there are previous jokes
        new_joke = state.latest_joke
        new_embedding = embedding_model.encode(new_joke, convert_to_tensor=True)
        previous_jokes = [joke.text for joke in state.jokes]
        previous_embeddings = embedding_model.encode(previous_jokes, 
        convert_to_tensor=True)
        similarities = util.cos_sim(new_embedding, previous_embeddings)[0]
        max_similarity = np.max(similarities.numpy()) if similarities.numel() > 0 else 0.0
        if max_similarity > 0.8: # If too similar
            print(f"Critic: Joke rejected because it is too similar to previous one. Similarity: {max_similarity:.2f}")
            return {"approved": False}
        
    # Existing logic for humour and appropriateness
    prompt = build_prompt(
        "evaluate_joke",
        joke_text=state.latest_joke,
        category=state.category,
        language=state.language
    )
    messages = [SystemMessage(content=prompt)]
    decision = llm.invoke(messages).content.strip().lower()
    approved = "approve" in decision or "yes" in decision


    # Reset retries if approved
    if approved:
        return {"approved": True, "retry_count": 0}
    else:
        return {"approved": False}


def show_final_joke(state: JokeState) -> dict:
    joke = Joke(text=state.latest_joke, category=state.category)
    print_joke(joke)
    return {"jokes": [joke], "latest_joke": "", "approved": False, "retry_count": 0}


def writer_critic_router(state: JokeState) -> str:
    if state.approved or state.retry_count >= state.max_retries:
        return "show_final_joke"
    return "writer"

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
            print(f"Category changed to: {selected_category.upper()}")
            return {"category": selected_category}
        else:
            print("Invalid choice. Keeping current category.")
            return {}
    except ValueError:
        print("Please enter a valid number. Keeping current category.")
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
            print("Invalid choice. Keeping current language.")
            return {}
    except ValueError:
        print("Please enter a valid number. Keeping current language.")
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
        return "writer"
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
    

# BUILD GRAPH
def build_joke_graph(
        writer_model: str = "llama-3.1-8b-instant",
        critic_model: str = "llama-3.1-8b-instant",
        writer_temp: float = 0.95,
        critic_temp: float = 0.1,
    ) -> CompiledStateGraph:

    writer_llm = call_llm(writer_model, writer_temp)
    critic_llm = call_llm(critic_model, critic_temp)

    workflow = StateGraph(JokeState)
     
    # register nodes
    workflow.add_node("show_menu", show_menu)
    workflow.add_node("update_category", update_category)
    workflow.add_node("update_language", update_language)
    workflow.add_node("reset_jokes", reset_jokes)
    workflow.add_node("exit_bot", exit_bot)
    workflow.add_node("writer", partial(writer, writer_llm))
    workflow.add_node("critic", partial(critic, critic_llm))
    workflow.add_node("show_final_joke", show_final_joke)

    # Setting entry logic
    workflow.set_entry_point("show_menu")

    # Routing logic
    workflow.add_conditional_edges(
        "show_menu",
        route_choice,
        {
            "writer": "writer",
            "update_category": "update_category",
            "update_language": "update_language",
            "reset_jokes": "reset_jokes",
            "exit_bot": "exit_bot",
        },
    )

    # Transitions
    workflow.add_edge("update_category", "show_menu")
    workflow.add_edge("update_language", "show_menu")
    workflow.add_edge("reset_jokes", "show_menu")
    workflow.add_edge("writer", "critic")
    workflow.add_conditional_edges(
        "critic",
        writer_critic_router,
        {"writer": "writer", "show_final_joke": "show_final_joke"},
    )
    workflow.add_edge("show_final_joke", "show_menu")
    workflow.add_edge("exit_bot", END)

    return workflow.compile()


# MAIN ENTRY
def main():
    print("Welcome to the Joke Bot!")
    print("Demonstrating a simple agentic state flow using LangGraph with LLMs.")
    print("=" * 70 + "\n")

    graph = build_joke_graph(writer_temp=0.8, critic_temp=0.1)
    final_state = graph.invoke(
        JokeState(category="neutral"), config={"recursion_limit": 500})

    # After completion, print the collected jokes
    print(f"\nFinal category: {final_state.get('category', 'unknown').upper()}")
    print("Thanks for using the Joke Bot!")

if __name__ == "__main__":
    main()
        
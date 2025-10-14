from .models import JokeState
from .workflow import build_joke_graph

# MAIN ENTRY
def main():
    print("Welcome to the Joke Bot!")
    print("Demonstrating a simple agentic state flow using LangGraph without LLMs.")
    print("=" * 70 + "\n")

    graph = build_joke_graph()
    final_state = graph.invoke(JokeState(), config={"recursion_limit": 100})

    # After completion, print the collected jokes
    print(f"\nFinal category: {final_state.get('category', 'unknown').upper()}")
    print("Thanks for using the Joke Bot!")

if __name__ == "__main__":
    main()
        
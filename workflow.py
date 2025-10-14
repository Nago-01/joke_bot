from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from .nodes import show_menu, fetch_joke, update_category, update_language, reset_jokes, exit_bot, route_choice
from .models import JokeState
# BUILD GRAPH
def build_joke_graph() -> CompiledStateGraph:
    workflow = StateGraph(JokeState)
     
    # register nodes
    workflow.add_node("show_menu", show_menu)
    workflow.add_node("fetch_joke", fetch_joke)
    workflow.add_node("update_category", update_category)
    workflow.add_node("update_language", update_language)
    workflow.add_node("reset_jokes", reset_jokes)
    workflow.add_node("exit_bot", exit_bot)

    # Setting entry logic
    workflow.set_entry_point("show_menu")

    # Routing logic
    workflow.add_conditional_edges(
        "show_menu",
        route_choice,
        {
            "fetch_joke": "fetch_joke",
            "update_category": "update_category",
            "update_language": "update_language",
            "reset_jokes": "reset_jokes",
            "exit_bot": "exit_bot",
        }
    )

    # Transitions
    workflow.add_edge("fetch_joke", "show_menu")
    workflow.add_edge("update_category", "show_menu")
    workflow.add_edge("update_language", "show_menu")
    workflow.add_edge("reset_jokes", "show_menu")
    workflow.add_edge("exit_bot", END)

    return workflow.compile()
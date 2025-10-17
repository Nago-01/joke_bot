"""
Centralized utility for creating prompts or instructions used by the Joke Bot for LLM-driven tasks.
"""

from typing import Optional
from .utils import load_config
from .paths import PROMPT_CONFIG_FILE_PATH



prompt_cfg = load_config(PROMPT_CONFIG_FILE_PATH)



def build_prompt(
    task: str,
    category: Optional[str] = None,
    language: Optional[str] = None,
    joke_text: Optional[str] = None
) -> str:
    """
    Builds structured prompts depending on the task.

    Args:
        task (str): The purpose of the prompt (e.g., 'fetch_joke', 'show_menu', 'show_final_joke')
        category (str, optional): Joke category (e.g., 'neutral', 'chuck', 'all')
        language (str, optional): Joke language code (e.g., 'en', 'de', 'es')
        joke_text (str, optional): A joke text (used for explain or rate tasks).

    Returns:
        str: A formatted prompt ready for use in LLM calls or debugging.
    """

    if task not in prompt_cfg:
        raise ValueError(f"Unknown task: {task}. Check prompt_config.yaml.")
    
    cfg = prompt_cfg[task]

    # Build the system prompt from YAML
    prompt = f"Role: {cfg['role']}\n"
    prompt += f"Goal: {cfg['goal']}\n"

    if 'instructions' in cfg:
        prompt += "Instructions:\n" + "\n".join(f"- {i}" for i in cfg['instructions']) + "\n"
    
    if 'output_constraints' in cfg:
        prompt += "Output Constraints:\n" + "\n".join(f"- {c}" for c in cfg['output_constraints']) + "\n"
    
    if 'style_or_tone' in cfg:
        prompt += "Style/Tone:\n" + "\n".join(f"- {s}" for s in cfg['style_or_tone']) + "\n"

    # Add task-sepcific details
    if task == "write_joke":
        prompt += f"Write a joke in {language or 'en'} about {category or 'neutral'}.\n"
    elif task == "evaluate_joke":
        prompt += f"Joke to evaluate: {joke_text}\n"
        prompt += f"Category: {category or 'neutral'}, Language: {language or 'en'}\n"
        prompt += "Respond only with 'approve' or 'reject'.\n"

    return prompt


# if __name__ == "__main__":

#     # quick demo
#     print(build_prompt("fetch_joke", category="chuck", language="en"))
#     print(build_prompt("explain_joke", joke_text="Why did the chicken cross the road? To get to the other side!"))
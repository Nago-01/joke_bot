from pydantic import BaseModel
from typing import Annotated, List, Literal
from operator import add


# DEFINE STATE
class Joke(BaseModel):
    text: str
    category: str

class JokeState(BaseModel):
    jokes: Annotated[List[Joke], add] = []
    # 'n' for new joke, 'c' for change category, 'q' for quit
    jokes_choice: Literal["n", "c", "l", "r", "q"] = "n" 
    category: str = "neutral"
    language: str = "en"
    quit: bool = False

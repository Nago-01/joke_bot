from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.language_models.chat_models import BaseChatModel
from dotenv import load_dotenv
import warnings


load_dotenv()

def call_llm(model_name: str, temperature: float = 0.7) -> BaseChatModel:
    try:
        if model_name == "llama-3.1-8b-instant":
            return ChatGroq(model="llama-3.1-8b-instant", temperature=temperature)
        elif model_name == "gpt-4o-mini":
            return ChatOpenAI(model="gpt-4o-mini", temperature=temperature)
        else:
            raise ValueError(f"Unknown model name: {model_name}")
    except Exception as e:
        warnings.warn(f"LLM initialization failed: {e}. Falling back to Groq Llama")
        return ChatGroq(model="llama-3.1-8b-instant", temperature=temperature)
from langchain_mistralai import ChatMistralAI
from langchain_ollama import ChatOllama

from src.config import (
    MISTRAL_API_KEY,
    MISTRAL_LLM_MODEL,
    OLLAMA_MODEL,
)


def get_cloud_llm():

    if not MISTRAL_API_KEY:
        raise ValueError(
            "MISTRAL_API_KEY is missing."
        )

    return ChatMistralAI(
        model=MISTRAL_LLM_MODEL,
        api_key=MISTRAL_API_KEY,
        temperature=0,
    )


def get_local_llm():

    return ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0,
    )
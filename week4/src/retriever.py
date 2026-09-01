from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS

from src.config import (
    MISTRAL_API_KEY,
    EMBEDDING_MODEL,
    VECTORSTORE_DIR,
    TOP_K,
)


def load_vectorstore():

    embeddings = MistralAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=MISTRAL_API_KEY,
    )

    vectorstore = FAISS.load_local(
        VECTORSTORE_DIR,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return vectorstore


def retrieve_with_scores(
    vectorstore,
    question,
    k=TOP_K,
):

    results = (
        vectorstore
        .similarity_search_with_score(
            question,
            k=k,
        )
    )

    return results
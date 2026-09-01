from pathlib import Path

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS

from src.config import (
    DATA_DIR,
    VECTORSTORE_DIR,
    MISTRAL_API_KEY,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


def load_documents():
    print("\nLoading HR policy documents...")

    loader = DirectoryLoader(
        DATA_DIR,
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8"
        },
        show_progress=True,
    )

    documents = loader.load()

    print(f"Loaded documents: {len(documents)}")

    return documents


def split_documents(documents):

    print("\nSplitting documents into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(documents)

    print(f"Generated chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks):
        print(
            f"Chunk {index + 1}: "
            f"{len(chunk.page_content)} characters | "
            f"{chunk.metadata.get('source')}"
        )

    return chunks


def create_vectorstore(chunks):

    print("\nCreating Mistral embeddings...")

    embeddings = MistralAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=MISTRAL_API_KEY,
    )

    print("Building FAISS vector store...")

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings,
    )

    Path(VECTORSTORE_DIR).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    vectorstore.save_local(
        VECTORSTORE_DIR
    )

    print(
        f"\nFAISS index saved to: "
        f"{VECTORSTORE_DIR}"
    )


def main():

    if not MISTRAL_API_KEY:
        raise ValueError(
            "MISTRAL_API_KEY is missing. "
            "Add it to your .env file."
        )

    documents = load_documents()

    chunks = split_documents(
        documents
    )

    create_vectorstore(
        chunks
    )


if __name__ == "__main__":
    main()
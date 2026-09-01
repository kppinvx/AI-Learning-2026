import argparse

from src.llm import (
    get_cloud_llm,
    get_local_llm,
)

from src.rag import HRPolicyRAG


def print_retrieved_chunks(result):

    print("\n")
    print("=" * 80)
    print("RETRIEVED CONTEXT")
    print("=" * 80)

    for rank, (
        document,
        distance,
    ) in enumerate(
        result["retrieved"],
        start=1,
    ):

        similarity = (
            1 / (1 + float(distance))
        )

        print(
            f"\nChunk #{rank}"
        )

        print(
            f"Source: "
            f"{document.metadata.get('source')}"
        )

        print(
            f"FAISS distance: "
            f"{float(distance):.6f}"
        )

        print(
            f"Derived similarity: "
            f"{similarity:.6f}"
        )

        print("-" * 80)

        print(
            document.page_content
        )

        print("-" * 80)


def print_answer(result):

    print("\n")
    print("=" * 80)
    print("ANSWER")
    print("=" * 80)

    print(
        result["answer"]
    )

    print("\nTiming:")

    print(
        f"Retrieval: "
        f"{result['retrieval_time']:.4f}s"
    )

    print(
        f"Generation: "
        f"{result['generation_time']:.4f}s"
    )

    print(
        f"Total: "
        f"{result['total_time']:.4f}s"
    )


def main():

    parser = argparse.ArgumentParser(
        description="HR Policy RAG CLI"
    )

    parser.add_argument(
        "--model",
        choices=[
            "cloud",
            "ollama",
        ],
        default="cloud",
    )

    args = parser.parse_args()

    if args.model == "cloud":

        print(
            "Using Mistral Cloud LLM..."
        )

        llm = get_cloud_llm()

    else:

        print(
            "Using local Ollama LLM..."
        )

        llm = get_local_llm()

    rag = HRPolicyRAG(
        llm
    )

    print("\n")
    print("=" * 80)
    print("HR POLICY Q&A BOT")
    print("=" * 80)

    print(
        "\nType 'exit' to quit."
    )

    while True:

        question = input(
            "\nHR Question: "
        ).strip()

        if question.lower() in {
            "exit",
            "quit",
        }:

            print(
                "\nGoodbye!"
            )

            break

        if not question:
            continue

        try:

            result = rag.answer(
                question
            )

            print_retrieved_chunks(
                result
            )

            print_answer(
                result
            )

        except Exception as error:

            print(
                f"\nError: {error}"
            )


if __name__ == "__main__":
    main()
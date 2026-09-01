import json
import time
from pathlib import Path

from src.llm import (
    get_cloud_llm,
    get_local_llm,
)

from src.rag import HRPolicyRAG


QUESTIONS = [
    "How many paid annual leave days do employees receive?",

    "How many days of annual leave can be carried forward?",

    "How many days per week can an employee work remotely?",

    "What are the normal working hours?",

    "How long does an employee have to submit an expense claim?",

    "Can employees claim personal expenses?",

    "What happens if an employee needs emergency leave?",

    "Does the HR policy provide a salary increase percentage?",
]


def run_model(
    model_name,
    llm,
):

    print(
        f"\nRunning benchmark: "
        f"{model_name}"
    )

    rag = HRPolicyRAG(
        llm
    )

    results = []

    for question in QUESTIONS:

        print(
            f"\nQuestion: {question}"
        )

        start = time.perf_counter()

        result = rag.answer(
            question
        )

        elapsed = (
            time.perf_counter()
            - start
        )

        item = {
            "model": model_name,
            "question": question,
            "answer": result["answer"],
            "retrieval_time": (
                result["retrieval_time"]
            ),
            "generation_time": (
                result["generation_time"]
            ),
            "total_time": elapsed,
            "retrieved_chunks": [],
        }

        for (
            document,
            distance,
        ) in result["retrieved"]:

            item[
                "retrieved_chunks"
            ].append(
                {
                    "source": document.metadata.get(
                        "source"
                    ),
                    "distance": float(
                        distance
                    ),
                    "derived_similarity": (
                        1
                        / (
                            1
                            + float(
                                distance
                            )
                        )
                    ),
                    "content": (
                        document.page_content
                    ),
                }
            )

        results.append(
            item
        )

        print(
            f"Time: {elapsed:.3f}s"
        )

    return results


def main():

    Path("results").mkdir(
        exist_ok=True
    )

    cloud_results = run_model(
        "mistral-cloud",
        get_cloud_llm(),
    )

    local_results = run_model(
        "ollama-local",
        get_local_llm(),
    )

    output = {
        "cloud": cloud_results,
        "local": local_results,
    }

    output_file = (
        "results/benchmark_results.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"\nBenchmark saved to: "
        f"{output_file}"
    )


if __name__ == "__main__":
    main()
import time

from langchain_core.prompts import ChatPromptTemplate

from src.retriever import (
    load_vectorstore,
    retrieve_with_scores,
)


PROMPT = """
You are an HR policy assistant.

Answer the user's question using ONLY the HR policy
context provided below.

Rules:

1. Do not use outside knowledge.
2. Do not invent policies.
3. If the answer is not present in the context,
   say that the HR policy documents do not contain
   enough information to answer the question.
4. Be concise and factual.
5. If the policy contains a specific number, date,
   limit, or requirement, preserve it accurately.

HR POLICY CONTEXT:

{context}

USER QUESTION:

{question}
"""


prompt = ChatPromptTemplate.from_template(
    PROMPT
)


class HRPolicyRAG:

    def __init__(self, llm):

        self.llm = llm

        self.vectorstore = (
            load_vectorstore()
        )

    def retrieve(
        self,
        question,
        k=4,
    ):

        return retrieve_with_scores(
            self.vectorstore,
            question,
            k,
        )

    def format_context(
        self,
        results,
    ):

        contexts = []

        for rank, (doc, distance) in enumerate(
            results,
            start=1,
        ):

            similarity = (
                1 / (1 + float(distance))
            )

            contexts.append(
                f"""
--- Retrieved Chunk {rank} ---

Source:
{doc.metadata.get("source", "unknown")}

FAISS Distance:
{float(distance):.6f}

Derived Similarity:
{similarity:.6f}

Content:
{doc.page_content}
"""
            )

        return "\n".join(
            contexts
        )

    def answer(
        self,
        question,
        k=4,
    ):

        retrieval_start = time.perf_counter()

        results = self.retrieve(
            question,
            k,
        )

        retrieval_time = (
            time.perf_counter()
            - retrieval_start
        )

        context = self.format_context(
            results
        )

        messages = prompt.format_messages(
            context=context,
            question=question,
        )

        generation_start = time.perf_counter()

        response = self.llm.invoke(
            messages
        )

        generation_time = (
            time.perf_counter()
            - generation_start
        )

        answer = response.content

        total_time = (
            retrieval_time
            + generation_time
        )

        return {
            "question": question,
            "answer": answer,
            "retrieved": results,
            "context": context,
            "retrieval_time": retrieval_time,
            "generation_time": generation_time,
            "total_time": total_time,
        }
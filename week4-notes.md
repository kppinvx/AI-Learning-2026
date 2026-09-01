## What is RAG?
Retrieval-Augmented Generation (RAG) is a technique that allows an LLM to answer questions using external knowledge instead of relying only on its training data.

### Without RAG:
LLM answers based on its pre-trained knowledge.
May produce outdated information or hallucinations.

### With RAG:
Relevant documents are retrieved from a knowledge base.
Retrieved context is provided to the LLM.
LLM generates answers grounded in the retrieved data.

## RAG Pipeline Architecture

                Documents
                    │
                    ▼
           Document Loader
                    │
                    ▼
              Text Splitter
                    │
                    ▼
               Chunks
                    │
                    ▼
           Embedding Model
                    │
                    ▼
             Vector Store
                (FAISS)
                    │
         ───────────┼───────────
                    │
               User Query
                    │
                    ▼
           Query Embedding
                    │
                    ▼
               Retriever
                    │
                    ▼
          Relevant Chunks
                    │
                    ▼
                  LLM
                    │
                    ▼
              Final Answer

## Cloud vs Local LLMs (Ollama)

### Cloud LLMs

Examples:
- OpenAI
- Anthropic Claude
- Google Gemini

Advantages
- Best quality
- Large context windows
- No hardware requirements
- Easy integration

Disadvantages
- API cost
- Internet required
- Data leaves local machine

### Local LLMs Using Ollama

Ollama allows running models locally.

Popular models:
- Llama 3
- Mistral
- Gemma
- Qwen
- DeepSeek

Advantages
- Free after setup
- Private
- Offline
- Good for internal company documents

Disadvantages
- Requires RAM/CPU/GPU
- Slower than cloud APIs
- Quality depends on hardware

## Complete RAG Workflow Summary

1. Load Documents
2. Split into Chunks
3. Generate Embeddings
4. Store in FAISS
5. User Question
6. Embed Question
7. Retriever Finds Similar Chunks
8. Retrieved Context + Question
9. LLM Generates Answer
10. Grounded Response

## Key LangChain Components

| Component         | Purpose                                       |
| ----------------- | --------------------------------------------- |
| Document Loader   | Load data from PDFs, text, web pages, etc.    |
| Text Splitter     | Break documents into chunks                   |
| Chunking          | Create manageable pieces for embeddings       |
| Embedding Model   | Convert text into vectors                     |
| Vector Store      | Store and search vectors                      |
| FAISS             | Local vector database for similarity search   |
| Retriever         | Fetch relevant chunks                         |
| Similarity Search | Find nearest matching vectors                 |
| Context Retrieval | Supply relevant context to LLM                |
| LLM               | Generate final answer using retrieved context |


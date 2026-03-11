# AI Layer (placeholders)

This folder will contain scripts for:
- Document normalization & chunking
- Embedding generation and vector index (FAISS / Weaviate / Milvus)
- RAG retrieval pipeline and citation
- Offline evaluation harness for chatbot accuracy

Suggested files to add later:
- `index_docs.py` — process markdown lessons into embeddings
- `rag_service.py` — a thin server to perform retrieval + prompt assembly
- `notebooks/` — experiments for knowledge tracing and KT models

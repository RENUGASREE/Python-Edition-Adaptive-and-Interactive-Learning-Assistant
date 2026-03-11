# Architecture Overview

This document summarizes the high-level architecture for "Python Edition: Adaptive and Interactive Learning Assistant".

Components:
- Frontend: React app (Dashboard, Lessons, Quizzes, Coding IDE, Chatbot, Certificates, Gamification). Connects to backend REST API + WebSocket for real-time events.
- Backend: FastAPI (REST) providing Auth, Profile, Recommendation, Grader (sandbox stub), Certificate generator, Gamification, Notifications, Analytics endpoints.
- Datastores: PostgreSQL for relational data, object store for certificates, vector index for RAG (e.g., FAISS/Weaviate), logs in separate table or ELK stack.
- AI layer: scripts for indexing documents, RAG retrieval, and model orchestration (calls to hosted LLMs or local models via API).
- Infra: `docker-compose` to run backend + postgres locally for development.

Security & Integrity:
- Auth: JWT, password hashing
- Auto-grader: run user code in isolated Docker runner (not implemented in this scaffold — placeholder endpoint exists)
- Integrity events: frontend tracks focus/blur and sends events to backend for auditing

Files in the scaffold:
- `backend/app/` : FastAPI application and API endpoints (stubs)
- `frontend/src/` : React components skeleton
- `ai/` : placeholder scripts for RAG indexing
- `infra/docker-compose.yml` : Compose file for Postgres + backend (starter)

Use this doc to guide implementation details and iterate on components.

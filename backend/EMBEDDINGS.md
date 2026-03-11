# Embedding Provider Management

## Provider Configuration
- EMBEDDING_PROVIDER: auto | openai | local | hash
- OPENAI_API_KEY: required for OpenAI embeddings
- OPENAI_EMBEDDING_MODEL: default text-embedding-3-small
- LOCAL_EMBEDDING_MODEL: default sentence-transformers/all-MiniLM-L6-v2
- EMBEDDING_DIMENSIONS: vector size stored in pgvector (match model output or truncation)
- EMBEDDING_DISTANCE_METRIC: cosine | l2
- EMBEDDING_MIN_SIMILARITY: filter threshold for RAG sources

## pgvector Extension Checklist
1. Ensure PostgreSQL has the pgvector extension installed.
2. Enable extension in the target database.
3. Apply Django migrations that add VectorField columns.
4. Backfill embeddings for existing lessons.
5. Create a vector index for similarity search.

## Migration Steps
1. Install dependencies:
   - pip install -r backend/requirements.txt
2. Enable extension:
   - CREATE EXTENSION IF NOT EXISTS vector;
3. Run migrations:
   - python manage.py migrate
4. Start background workers:
   - python manage.py qcluster
5. Backfill embeddings by re-saving lessons or running the command:
   - python manage.py backfill_embeddings
   - python manage.py backfill_embeddings --force

## Indexing Strategy
Use pgvector indexes to accelerate similarity search. Choose IVFFLAT for large datasets with batch build and HNSW for lower latency.

### Example SQL
IVFFLAT cosine index:
CREATE INDEX CONCURRENTLY lessonchunk_embedding_ivfflat
ON lessons_lessonchunk
USING ivfflat (embedding_vector vector_cosine_ops)
WITH (lists = 100);

HNSW cosine index:
CREATE INDEX CONCURRENTLY lessonchunk_embedding_hnsw
ON lessons_lessonchunk
USING hnsw (embedding_vector vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

### Query Example
SELECT id, topic, content
FROM lessons_lessonchunk
ORDER BY embedding_vector <-> '[0.1,0.2,...]'::vector
LIMIT 5;

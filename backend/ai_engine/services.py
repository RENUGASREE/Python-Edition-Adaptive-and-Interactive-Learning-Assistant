"""Hybrid AI services for mastery updates and RAG-style retrieval."""
import hashlib
import logging
import os
import time
from typing import Dict, List, Optional
from django.core.cache import cache
from core.models import User
from lessons.models import LessonChunk

logger = logging.getLogger("ai_engine.embeddings")
_LOCAL_MODEL = None


def apply_bkt_update(user: User, topic: str, correct: bool, learn_rate=0.2, slip_factor=0.1):
    mastery = user.mastery_vector or {}
    current = float(mastery.get(topic, 0.3))
    if correct:
        updated = current + (1 - current) * learn_rate
    else:
        updated = current * slip_factor
    mastery[topic] = round(updated, 4)
    user.mastery_vector = mastery
    user.save(update_fields=["mastery_vector"])
    return mastery[topic]


def _embedding_dimensions() -> int:
    return int(os.getenv("EMBEDDING_DIMENSIONS", "384"))


def _hash_embedding(text: str, dimensions: int = 384) -> List[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    buffer = list(digest) * ((dimensions // len(digest)) + 1)
    return [round(b / 255, 4) for b in buffer[:dimensions]]


def _openai_embedding(text: str, model: str) -> Optional[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    base_url = os.getenv("OPENAI_BASE_URL")
    timeout = float(os.getenv("OPENAI_TIMEOUT_SECONDS", "30"))
    try:
        from openai import OpenAI
    except Exception:
        return None
    client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)
    response = client.embeddings.create(model=model, input=text)
    if not response.data:
        return None
    return response.data[0].embedding


def _local_embedding(text: str, model_name: str) -> Optional[List[float]]:
    global _LOCAL_MODEL
    try:
        from sentence_transformers import SentenceTransformer
    except Exception:
        return None
    if _LOCAL_MODEL is None:
        _LOCAL_MODEL = SentenceTransformer(model_name)
    embedding = _LOCAL_MODEL.encode([text])[0]
    return embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)


def _normalize_embedding(embedding: Optional[List[float]], dimensions: int) -> Optional[List[float]]:
    if embedding is None:
        return None
    if len(embedding) >= dimensions:
        return [float(val) for val in embedding[:dimensions]]
    padded = list(embedding) + [0.0] * (dimensions - len(embedding))
    return [float(val) for val in padded]


def _provider_order() -> List[str]:
    provider = os.getenv("EMBEDDING_PROVIDER", "auto").lower()
    if provider == "openai":
        return ["openai", "local", "hash"]
    if provider == "local":
        return ["local", "hash"]
    if provider == "hash":
        return ["hash"]
    if os.getenv("OPENAI_API_KEY"):
        return ["openai", "local", "hash"]
    return ["local", "hash"]


def _embed_with_retry(provider: str, text: str, dimensions: int) -> Optional[List[float]]:
    max_retries = int(os.getenv("EMBEDDING_MAX_RETRIES", "3"))
    base_sleep = float(os.getenv("EMBEDDING_RETRY_BASE_SECONDS", "0.5"))
    for attempt in range(max_retries):
        try:
            if provider == "openai":
                model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
                return _normalize_embedding(_openai_embedding(text, model), dimensions)
            if provider == "local":
                model_name = os.getenv("LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
                return _normalize_embedding(_local_embedding(text, model_name), dimensions)
            if provider == "hash":
                return _hash_embedding(text, dimensions=dimensions)
        except Exception as exc:
            logger.warning("Embedding provider failure", extra={"provider": provider, "attempt": attempt + 1})
            logger.error(str(exc))
        time.sleep(base_sleep * (attempt + 1))
    logger.error("Embedding retries exhausted", extra={"provider": provider})
    return None


def _record_embedding_metrics(duration: float, provider: str, primary_provider: str):
    total_key = "embedding_metrics:total_seconds"
    count_key = "embedding_metrics:count"
    total = cache.get(total_key, 0.0) + duration
    count = cache.get(count_key, 0) + 1
    cache.set(total_key, total, timeout=None)
    cache.set(count_key, count, timeout=None)
    average = total / count if count else duration
    logger.info("Embedding timing", extra={"duration_seconds": round(duration, 4), "average_seconds": round(average, 4), "provider": provider})
    if provider != primary_provider:
        logger.warning("Embedding provider fallback", extra={"provider": provider, "primary_provider": primary_provider})


def embed_text(text: str, dimensions: Optional[int] = None) -> List[float]:
    dimensions = dimensions or _embedding_dimensions()
    provider_order = _provider_order()
    primary_provider = provider_order[0] if provider_order else "hash"
    for provider in provider_order:
        start = time.perf_counter()
        embedding = _embed_with_retry(provider, text, dimensions)
        if embedding:
            duration = time.perf_counter() - start
            _record_embedding_metrics(duration, provider, primary_provider)
            return embedding
    return _hash_embedding(text, dimensions=dimensions)


def _retrieval_cache_key(query: str, topic: Optional[str], metric: str, top_k: int) -> str:
    model = os.getenv("OPENAI_EMBEDDING_MODEL", "")
    provider = os.getenv("EMBEDDING_PROVIDER", "auto")
    digest = hashlib.sha256(f"{query}:{topic}:{metric}:{top_k}:{provider}:{model}".encode("utf-8")).hexdigest()
    return f"rag:query:{digest}"


def _distance_metric() -> str:
    return os.getenv("EMBEDDING_DISTANCE_METRIC", "cosine").lower()


def _similarity_from_distance(distance: float, metric: str) -> float:
    if metric == "l2":
        similarity = 1.0 / (1.0 + distance)
    else:
        similarity = 1.0 - distance
    return max(0.0, min(1.0, similarity))


def retrieve_context(query: str, top_k: int = 3, topic: Optional[str] = None) -> List[Dict]:
    metric = _distance_metric()
    cache_ttl = int(os.getenv("EMBEDDING_QUERY_CACHE_SECONDS", "60"))
    cache_key = _retrieval_cache_key(query, topic, metric, top_k)
    cached = cache.get(cache_key)
    if cached:
        return cached
    start = time.perf_counter()
    
    try:
        query_vec = embed_text(query)
    except Exception as exc:
        logger.error(f"Embedding generation failed: {exc}")
        return []

    queryset = LessonChunk.objects.all()
    if topic:
        queryset = queryset.filter(topic=topic)

    if not queryset.exists():
        return []

    try:
        from django.conf import settings
        use_pgvector = "pgvector.django" in settings.INSTALLED_APPS and os.getenv("PGVECTOR_ENABLED", "true").lower() == "true"
        
        if use_pgvector:
            from pgvector.django import CosineDistance, L2Distance
            if metric == "l2":
                queryset = queryset.annotate(distance=L2Distance("embedding_vector", query_vec))
            else:
                queryset = queryset.annotate(distance=CosineDistance("embedding_vector", query_vec))
            results = list(queryset.order_by("distance")[:top_k])
            use_distance = True
        else:
            raise ImportError("pgvector not enabled or installed")
    except (Exception, ImportError) as exc:
        logger.info("Falling back to python similarity search")
        use_distance = False
        max_candidates = int(os.getenv("EMBEDDING_FALLBACK_CANDIDATES", "100")) # Reduced from 500 for speed
        candidates = list(queryset.order_by("-created_at")[:max_candidates])

        def _cosine(a: List[float], b: List[float]) -> float:
            try:
                dot = 0.0
                na = 0.0
                nb = 0.0
                for x, y in zip(a, b):
                    fx = float(x)
                    fy = float(y)
                    dot += fx * fy
                    na += fx * fx
                    nb += fy * fy
                if na <= 0.0 or nb <= 0.0:
                    return 0.0
                return dot / ((na ** 0.5) * (nb ** 0.5))
            except Exception:
                return 0.0

        scored = []
        for chunk in candidates:
            vec = getattr(chunk, "embedding_vector", None) or []
            if not isinstance(vec, list) or not vec:
                continue
            similarity = _cosine(query_vec, vec)
            scored.append((similarity, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        results = [chunk for _, chunk in scored[:top_k]]
    
    threshold = float(os.getenv("EMBEDDING_MIN_SIMILARITY", "0.1")) # Lowered threshold slightly
    response = []
    for chunk in results:
        similarity = 0.0
        if use_distance:
            distance = getattr(chunk, "distance", None)
            if distance is not None:
                similarity = _similarity_from_distance(float(distance), metric)
        else:
            vec = getattr(chunk, "embedding_vector", None) or []
            if isinstance(vec, list) and vec:
                similarity = _cosine(query_vec, vec)
        
        if similarity < threshold:
            continue
            
        response.append({
            "topic": chunk.topic,
            "content": chunk.content,
            "similarity": round(similarity, 4),
        })
    
    duration = round(time.perf_counter() - start, 4)
    logger.info(f"Retrieval finished in {duration}s with {len(response)} results")
    cache.set(cache_key, response, timeout=cache_ttl)
    return response


def answer_with_rag(query: str, topic: Optional[str] = None):
    query_lower = query.lower()
    results = retrieve_context(query, topic=topic)
    
    # Try to use OpenAI for intelligent response if available
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            base_url = os.getenv("OPENAI_BASE_URL")
            model = os.getenv("OPENAI_MODEL", "openchat/openchat-7b")
            timeout = float(os.getenv("OPENAI_TIMEOUT_SECONDS", "30"))
            
            client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)
            
            # Build context from retrieved results
            context = ""
            if results:
                context = "\n\n".join([f"Lesson: {entry['topic']}\n{entry['content']}" for entry in results])
            
            # Create prompt with context
            system_prompt = """You are a helpful AI tutor for a programming learning platform. 
            Provide clear, educational responses to help students learn programming concepts.
            Be encouraging and break down complex topics into simple steps."""
            
            user_prompt = f"Question: {query}"
            if topic:
                user_prompt += f"\nTopic: {topic}"
            if context:
                user_prompt += f"\n\nContext from lessons:\n{context}\n\nUse this context to help answer the question."
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            if response.choices:
                ai_response = response.choices[0].message.content
                return {
                    "response": ai_response,
                    "source_topic": results[0]["topic"] if results else topic,
                    "confidence_score": 0.9,
                    "sources": results
                }
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            # Fall back to template responses
    
    # Fallback template-based responses
    response_parts = []
    
    if "hint" in query_lower:
        response_parts.append("### 💡 Helpful Hint")
    elif "debug" in query_lower or "error" in query_lower or "wrong" in query_lower:
        response_parts.append("### 🔍 Debugging Assistance")
    elif "explain" in query_lower or "what is" in query_lower:
        response_parts.append("### 📖 Concept Explanation")
    else:
        response_parts.append("### 👋 AI Tutor Assistance")

    if not results:
        # Fallback if no specific lesson chunk found
        response_parts.append("I couldn't find a specific lesson chunk for this, but I'm here to help! Could you please share the specific part of the code you're working on or the error you're seeing?")
        return {
            "response": "\n\n".join(response_parts),
            "source_topic": topic,
            "confidence_score": 0.3,
            "sources": []
        }

    combined_content = "\n\n".join(entry["content"] for entry in results)
    main_topic = results[0]["topic"]
    
    if "hint" in query_lower:
        response_parts.append(f"For the **{main_topic}** challenge, think about how you can use the core concept discussed in the lesson.")
        response_parts.append("Try breaking the problem into smaller steps. What is the first thing your code needs to do?")
    elif "debug" in query_lower or "error" in query_lower:
        response_parts.append("When debugging Python, always check:")
        response_parts.append("- **Indentation**: Is your code correctly aligned?")
        response_parts.append("- **Syntax**: Did you forget a colon `:` or a parenthesis `)`?")
        response_parts.append("- **Variables**: Are you using the correct variable names?")
        response_parts.append("\nIf you share your code, I can help point out where it might be going wrong!")
    else:
        response_parts.append(f"Let's look at **{main_topic}**:")
        response_parts.append(combined_content)
        response_parts.append("\nDoes that clarify things, or would you like a specific example?")

    return {
        "response": "\n\n".join(response_parts),
        "source_topic": main_topic,
        "confidence_score": 0.8,
        "sources": results
    }


def enqueue_lesson_embedding_update(lesson_id: int):
    try:
        from django_q.tasks import async_task
        from ai_engine.tasks import generate_lesson_embeddings
        async_task(generate_lesson_embeddings, lesson_id)
        return
    except Exception as exc:
        logger.error("Embedding enqueue failed", extra={"lesson_id": lesson_id})
        logger.error(str(exc))
    try:
        from ai_engine.tasks import generate_lesson_embeddings
        generate_lesson_embeddings(lesson_id)
    except Exception as exc:
        logger.error("Embedding fallback failed", extra={"lesson_id": lesson_id})
        logger.error(str(exc))

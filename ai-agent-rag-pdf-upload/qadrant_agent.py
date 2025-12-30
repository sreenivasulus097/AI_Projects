import numpy as np
import os
import uuid
import logging
import hashlib
from dotenv import load_dotenv
from openai import OpenAI

from qdrant_db import client, COLLECTION_NAME
from document_loader import load_pdf

load_dotenv()

# reduce console noise by default; show only errors in normal runs
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------- SPLIT TEXT ----------------
def split_text(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))

    return chunks

# ---------------- EMBEDDINGS ----------------
def create_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )
        embeddings.append(response.data[0].embedding)
    return embeddings

# ---------------- QDRANT ----------------
def upload_chunks(chunks, source_name=None):
    """Upload text chunks to Qdrant. Attach `source_name` metadata if provided."""
    for idx, chunk in enumerate(chunks):
        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )

        # Create a deterministic id for the point to avoid duplicate uploads
        # Use source_name, chunk index and chunk content to derive a stable UUID
        hash_input = f"{source_name or 'no-source'}:{idx}:{chunk}"
        point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, hash_input))
        payload = {"text": chunk}
        if source_name:
            payload["source"] = source_name
            payload["chunk_index"] = idx

        logger.debug("Uploading chunk id=%s source=%s size=%d", point_id, source_name, len(chunk))

        try:
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    {
                        "id": point_id,
                        "vector": response.data[0].embedding,
                        "payload": payload
                    }
                ]
            )
            logger.debug("Chunk uploaded successfully id=%s", point_id)
        except Exception as e:
            # Log and continue; avoid crashing the entire indexing process on transient errors
            logger.error("Failed to upload chunk id=%s: %s", point_id, e)
            # re-raise only in DEBUG mode
            if logger.isEnabledFor(logging.DEBUG):
                raise

def search_qdrant(query, top_k=3):
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_vector = response.data[0].embedding

    logger.debug("Query vector: %s...", query_vector[:10])

    raw_results = None
    try:
        if hasattr(client, "query_points"):
            raw_results = client.query_points(
                collection_name=COLLECTION_NAME,
                query=query_vector,
                limit=top_k,
                with_payload=True,
            )
        else:
            raise RuntimeError("Qdrant client has no 'query_points' method")
    except Exception as e:
        # Log and re-raise to allow the caller (UI) to show a friendly message
        logger.error("Qdrant query error: %s", e)
        raise

    logger.debug("Raw results: %s", raw_results)

    if raw_results is None or (hasattr(raw_results, '__len__') and len(raw_results) == 0):
        logger.info("No results returned from Qdrant.")
        return []

    # Normalize hits to a list of points for different qdrant-client shapes
    hits = getattr(raw_results, "result", raw_results)
    logger.debug("Hits (raw): %s", hits)

    # Possible shapes:
    # - a plain list of ScoredPoint
    # - an object with attribute `points` (e.g., RawSearchResult.points)
    # - a dict with key 'points'
    if isinstance(hits, list):
        hits_list = hits
    elif hasattr(hits, "points"):
        hits_list = list(getattr(hits, "points") or [])
    elif isinstance(hits, dict) and "points" in hits:
        hits_list = list(hits.get("points") or [])
    else:
        # Fallback: try iterating over `hits` if it's iterable
        try:
            hits_list = list(hits)
        except Exception:
            hits_list = []

    logger.debug("Normalized hits_list length: %d", len(hits_list))

    results = []
    for point in hits_list:
        logger.debug("Inspecting point: %s", point)
        # point may be a mapping or an object
        payload = None
        if isinstance(point, dict):
            payload = point.get("payload") or point.get("payloads")
        else:
            payload = getattr(point, "payload", None) or getattr(point, "payloads", None)

        logger.debug("Payload extracted: %s", payload)
        if isinstance(payload, dict):
            # Text could be directly under 'text' or nested
            text_value = payload.get("text")
            if not text_value:
                # try other common keys
                for k in ("content", "text_content", "body"):
                    if payload.get(k):
                        text_value = payload.get(k)
                        break

            source_value = payload.get("source") if isinstance(payload.get("source"), str) else None

            if text_value:
                results.append({"text": text_value, "source": source_value})
                logger.debug("Appended text (len=%d) source=%s", len(text_value), source_value)
            else:
                logger.debug("Payload 'text' key is missing or empty.")
        else:
            logger.debug("Payload is not a dictionary or is None: %s", payload)

    logger.debug("Extracted results count: %d", len(results))
    return results

def inspect_collection():
    """Fetch and log all points in the collection for debugging."""
    try:
        points = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=10,  # Fetch a few points for inspection
            with_payload=True,
            with_vectors=False
        )
        print("Inspecting collection points:")
        for point in points[0]:
            print(f"Point ID: {point.id}, Payload: {point.payload}")
    except Exception as e:
        print(f"Error inspecting collection: {e}")

# ---------------- ANSWER GENERATION ----------------
def generate_answer(question, context_chunks):
    # context_chunks may be a list of dicts with {'text':..., 'source':...} or plain strings
    if not context_chunks:
        context = ""
    else:
        texts = [c["text"] if isinstance(c, dict) and "text" in c else str(c) for c in context_chunks]
        context = "\n".join(texts)

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer only from the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

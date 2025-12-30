from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import socket
import logging

load_dotenv()
QDRANT_URL = os.getenv("QDRANT_ENDPOINT")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

logging.basicConfig(level=logging.DEBUG)

if not QDRANT_URL:
    raise RuntimeError(
        "QDRANT_ENDPOINT environment variable is not set. "
        "Please set QDRANT_ENDPOINT to your Qdrant URL (e.g. https://<host>.qdrant.io)"
    )

# Extract hostname from URL and check DNS resolution early to provide a clearer error
_parsed = urlparse(QDRANT_URL)
_hostname_for_check = _parsed.hostname or QDRANT_URL

# Log DNS resolution attempt
logging.debug(f"Attempting DNS resolution for host: {_hostname_for_check}")
try:
    socket.getaddrinfo(_hostname_for_check, None)
    logging.debug("DNS resolution successful.")
except socket.gaierror as e:
    logging.error(f"DNS resolution failed: {e}")
    raise RuntimeError(f"DNS resolution failed for Qdrant host '{_hostname_for_check}': {e}")

# Construct client and surface any errors immediately with context
try:
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )
except Exception as e:
    raise RuntimeError(f"Failed to construct QdrantClient for URL {QDRANT_URL}: {e}")

COLLECTION_NAME = "document_chunks"
VECTOR_SIZE = 1536  # text-embedding-3-small

# Create collection only if it does not exist
existing_collections = [
    c.name for c in client.get_collections().collections
]

if COLLECTION_NAME not in existing_collections:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )

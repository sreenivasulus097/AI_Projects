import openai
import faiss
import numpy as np
from document_loader import load_pdf
from dotenv import load_dotenv
import os
import uuid

from qdrant_db import client

#load environment variables from a .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

#split text into chunks
def split_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        print("chunks:",chunks)
    return chunks

#generate embeddings for each chunk
def create_embeddings(chunks):
    #print("chunks size:", chunks.size)
    embeddings = []
    for chunk in chunks:
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )
        #print("response:", response)
        embeddings.append(response.data[0].embedding)
    return embeddings

#store embeddings in a FAISS index
def store_embeddings(embeddings):
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))
    return index

#search for similar chunks
def search(query, index, chunks):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_embedding = np.array(response.data[0].embedding).astype("float32")
    distances, indices = index.search(query_embedding.reshape(1, -1), k=3)

    return [chunks[i] for i in indices[0]]

#generate answer using the retrieved chunks
def generate_answer(question, context_chunks):
    context = "\n".join(context_chunks)

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer only from the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


#Additional enhancements for better usability
def upload_chunks(chunks, collection_name):
    for chunk in chunks:
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )

        embedding = response.data[0].embedding

        client.upsert(
            collection_name=collection_name,
            points=[
                {
                    "id": str(uuid.uuid4()),
                    "vector": embedding,
                    "payload": {"text": chunk}
                }
            ]
        )
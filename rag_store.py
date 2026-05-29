import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_DB_DIR, EMBEDDING_MODEL

COLLECTION_NAME = "documents"

_embedding_fn = None
_client = None
_collection = None


def _get_collection():
    global _client, _collection, _embedding_fn
    if _collection is None:
        _embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL,
        )
        _client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=_embedding_fn,
        )
    return _collection


def index_chunks(chunks: list[dict]):
    collection = _get_collection()
    ids = []
    documents = []
    metadatas = []
    for i, c in enumerate(chunks):
        ids.append(f"chunk_{i}")
        documents.append(c["content"])
        metadatas.append({"source": c["source"], "chunk_index": c["chunk_index"]})
    collection.add(ids=ids, documents=documents, metadatas=metadatas)


def search(query: str, top_k: int = 5) -> list[dict]:
    collection = _get_collection()
    results = collection.query(query_texts=[query], n_results=top_k)
    hits = []
    if results["documents"] and results["documents"][0]:
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            hits.append({
                "content": doc,
                "source": meta.get("source", "unknown"),
                "score": round(1 - dist, 4) if dist else 0,
            })
    return hits


def reset_store():
    global _client, _collection, _embedding_fn
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    try:
        _client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    _collection = None
    _embedding_fn = None

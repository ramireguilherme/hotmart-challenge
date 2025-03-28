import chromadb as chroma
import config
import chromadb.utils.embedding_functions as embedding_functions
import os

def init_db():
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.environ.get('OPENAI_API_KEY'),
                model_name="text-embedding-3-small"
            )
    chroma_client = chroma.PersistentClient(config.VECTOR_DB_PATH)
    collection = chroma_client.get_or_create_collection(name=config.COLLECTION_NAME, embedding_function=openai_ef)
    return collection


def query_db(collection, query : str, k : int):
    """
    Queries the database collection for the k most similar text chunks to the query.

    Args:
        query: The query text.
        k: The number of most similar text chunks to return.
    """
    results = collection.query(
        query_texts=[query],
        n_results=k,
    )
    return results

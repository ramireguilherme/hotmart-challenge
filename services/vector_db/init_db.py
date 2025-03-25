import chroma


def init_db():
    chroma_client = chroma.Client()
    collection = chroma_client.create_collection(name="db")
    return collection

def store_data():
    collection = init_db()
    collection.store(data={"key": "value"})
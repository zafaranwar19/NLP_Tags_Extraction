import chromadb
from chromadb.utils import embedding_functions

# 1. Initialize local persistent DB
client = chromadb.PersistentClient(path="./my_vector_db")

# 2. Define embedding function (matches your spaCy model logic)
# Chroma can use its own default or you can pass spaCy embeddings
collection = client.get_or_create_collection(name="org_capabilities")

def save_to_vector_db(doc_name, tags, full_text):
    # We join tags into a single string for 'searchability'
    tag_string = ", ".join(tags)
    
    collection.upsert(
        documents=[full_text], # The searchable text
        metadatas=[{"filename": doc_name, "tags": tag_string,
            "total_tags": len(tags)}], # Metadata for dashboard
        ids=[doc_name] # Unique ID
    )
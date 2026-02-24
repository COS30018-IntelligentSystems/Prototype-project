import chromadb 
from dotenv import load_dotenv
from chromadb.utils import embedding_functions

load_dotenv()

# Setting the Embeddings model
sentence_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
	model_name="all-MiniLM-L6-v2"
)


# Getting the collection
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(
  name="mitre_attack",
  embedding_function=sentence_ef
) 


# Take the first document for checking
result = collection.get(
  ids=["ID0"],  
  include=["embeddings", "documents"]
)

print(f"Total documents: {collection.count()}")
print(f"Embedding function: {type(collection._embedding_function).__name__}")
print(f"Document: {result['documents'][0][:100]}...")
print(f"Embedding dimensions: {len(result['embeddings'][0])}")
print(f"First 5 values: {result['embeddings'][0][:5]}")
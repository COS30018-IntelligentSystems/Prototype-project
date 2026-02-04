from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import chromadb
import os

load_dotenv()

# Setting the Embeddings model
googleai_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
  api_key=os.getenv("GOOGLE_API_KEY"),
  model_name="text-embedding-004"
)


# Setting the environment for local usage
DATA_PATH = "data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(
  name="mitre_attack",
  embedding_function=googleai_ef
)


# Loading the documents
loader = DirectoryLoader(DATA_PATH, glob="*.md")
raw_documents = loader.load()


# Splitting the documents
headers_to_split_on = [
  ("#", "Technique"),       # T1001 - Data Obfuscation
  ("##", "Section"),        # Description, Platforms, References
]

text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

chunks = []
for doc in raw_documents:
  split_docs = text_splitter.split_text(doc.page_content)
  for chunk in split_docs:
    # Carry over the original source file metadata
    chunk.metadata["source"] = doc.metadata.get("source", "")
  chunks.extend(split_docs)


# Preparing to be added in chromadb
documents = []
metadata = []
ids = []

for i, chunk in enumerate(chunks):
  documents.append(chunk.page_content)
  ids.append("ID" + str(i))
  metadata.append(chunk.metadata)


# Adding to chromadb
collection.upsert(
  documents=documents,
  metadatas=metadata,
  ids=ids
)


# Quick verifying
collection = chroma_client.get_or_create_collection(
  name="mitre_attack",
  embedding_function=googleai_ef
)

print(f"Embedding function: {type(collection._embedding_function).__name__}")
print(f"Model: {getattr(collection._embedding_function, '_model_name', 'N/A')}")
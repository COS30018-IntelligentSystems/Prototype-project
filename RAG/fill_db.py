from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
import chromadb

# Setting the environment
DATA_PATH = "data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="mitre_attack")


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
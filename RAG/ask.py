import chromadb
import os 
from chromadb.utils import embedding_functions
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 

# Setting the Embeddings model
googleai_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
  api_key=os.getenv("GOOGLE_API_KEY"),
  model_name="text-embedding-004"
)


# Setting the environment 
DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(
  name="mitre_attack",
  embedding_function=googleai_ef
)

user_query = input("What do you want to know about Mitre attack?\n\n").lower().strip()
results = collection.query(
  query_texts=[user_query],
  n_results=5
)

#print(results['documents'])
#print(results['metadatas']) 
#print(results['distances']) 

context = "" 
for i, (doc, meta) in enumerate(
  zip(results["documents"][0], results["metadatas"][0])
):
  context += f"""
SOURCE {i+1}
File: {meta.get('source')}
Page: {meta.get('page')}

{doc}
"""

system_prompt = f"""
You are a helpful assistant.
You answer questions about Mitre Attacks.

IMPORTANT RULES:
- Use ONLY the information in the SOURCES below.
- Do NOT use your own knowledge.
- If the answer is not in the sources, say: "I don't know".

--------------------
SOURCES:
{context}
""" 

#print(system_prompt)


# Answer with distance check 
THRESHOLD = 0.7
avg_distance = sum(results['distances'][0]) / len(results['distances'][0])
if avg_distance > THRESHOLD:
  print("Out of scope!")
  print(f"(Similarity score: {results['distances'][0][0]:.3f}, threshold: {THRESHOLD})")
else: 
  client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
  )

  response = client.chat.completions.create(
    model="nvidia/nemotron-3-nano-30b-a3b:free",  
    messages=[
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": user_query}
    ]
  )

  print("\n\n---------------------\n\n")

  print(response.choices[0].message.content)
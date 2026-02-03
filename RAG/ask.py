import chromadb
import os 
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 

# Setting the environment 
DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="mitre_attack")

user_query = input("What do you want to know about Mitre attack?\n\n")
results = collection.query(
  query_texts=[user_query],
  n_results=5
)

#print(results['documents'])
#print(results['metadatas']) 

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

client = OpenAI(
  api_key=os.getenv("OPENROUTER_API_KEY"),
  base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
  model="arcee-ai/trinity-large-preview:free",  
  messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_query}
  ]
)

print("\n\n---------------------\n\n")

print(response.choices[0].message.content)
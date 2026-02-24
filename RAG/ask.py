import chromadb
import os 
import json
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
  n_results=8
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
You are a cybersecurity assistant specialized in MITRE ATT&CK techniques.

You MUST follow these rules:
- Use ONLY the provided SOURCES.
- Do NOT use external knowledge.
- Extract information exactly as written.
- If a section is missing, return "Not documented".

IMPORTANT:
- Output MUST be valid JSON.
- Do NOT include explanations.
- Do NOT include markdown.
- Do NOT include text outside JSON.

Return JSON in this exact format:

{{
  "technique_id": "",
  "technique_name": "",
  "tactic": "",
  "description": "",
  "detection": "",
  "mitigations": ""
}}

--------------------
SOURCES:
{context}
"""

#print(system_prompt)


# Answer with distance check 
THRESHOLD = 0.7
best_distance = results['distances'][0][0]
if best_distance > THRESHOLD:
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
      {
        "role": "system", 
        "content": system_prompt
      },
      {
        "role": "user", 
        "content": f"Extract structured MITRE information for: {user_query}"
      }
    ]
  )

  print("\n\n---------------------\n\n")

  # Transfer the JSON answer to readable format
  raw_output = response.choices[0].message.content
  
  try:
    parsed = json.loads(raw_output)
    print(json.dumps(parsed, intent=2))
  except:
    print("Model did not return valid JSON:")
    print(raw_output)
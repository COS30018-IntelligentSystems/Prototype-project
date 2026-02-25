import chromadb
import os
import json
import re
from chromadb.utils import embedding_functions
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ---------------------------
# Embedding Model (Local)
# ---------------------------
sentence_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
  model_name="all-MiniLM-L6-v2"
)

# ---------------------------
# Vector DB Setup
# ---------------------------
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(
  name="mitre_attack",
  embedding_function=sentence_ef
)

# ---------------------------
# MITRE Query Function
# ---------------------------
def query_mitre(user_query):
  results = collection.query(
    query_texts=[user_query],
    n_results=8
  )

  if not results["documents"] or len(results["documents"][0]) == 0:
    return {"error": "No relevant MITRE information found."}

  best_distance = results['distances'][0][0]
  THRESHOLD = 0.7

  if best_distance > THRESHOLD:
    return {"error": "Query out of MITRE scope."}

  # Build context from retrieved chunks
  context = ""
  for i, (doc, meta) in enumerate(
    zip(results["documents"][0], results["metadatas"][0])
  ):
    context += f""" 
SOURCE {i+1}
File: {meta.get('source')}
        
{doc}
"""

  # System prompt
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

  # Call LLM
  client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
  )

  response = client.chat.completions.create(
    model="nvidia/nemotron-3-nano-30b-a3b:free",
    messages=[
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": f"Extract structured MITRE information for: {user_query}"}
    ]
  )

  raw_output = response.choices[0].message.content.strip()

  # Remove markdown formatting if present
  raw_output = re.sub(r"^```json", "", raw_output)
  raw_output = re.sub(r"^```", "", raw_output)
  raw_output = re.sub(r"```$", "", raw_output)
  raw_output = raw_output.strip()

  try:
    parsed = json.loads(raw_output)
    return parsed
  except json.JSONDecodeError:
    return {
      "error": "Model did not return valid JSON",
      "raw_output": raw_output
    }


# ---------------------------
# Allow standalone testing
# ---------------------------
if __name__ == "__main__":
  user_query = input("What do you want to know about MITRE ATT&CK?\n\n")
  result = query_mitre(user_query)
  print(json.dumps(result, indent=2))
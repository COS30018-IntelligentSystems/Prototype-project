import chromadb
import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# setting the environment

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="growing_vegetables")


user_query = input("What do you want to know about vegetables?\n\n")

results = collection.query(
  query_texts=[user_query],
  n_results=1
)

#print(results['documents'])
#print(results['metadatas']) 

system_prompt = """
You are a helpful assistant. You answer questions about how fruits and vegetables healthy on human life. 
But you only answer based on knowledge I'm providing you. You don't use your internal 
knowledge and you don't make thins up.

If you don't know the answer, just say: I don't know 

--------------------

The data:

"""+str(results['documents'])+"""

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
import chromadb
import os
import google.generativeai as genai
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

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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

model = genai.GenerativeModel(
  model_name="gemma3-12b",
  system_instruction=system_prompt
)

response = model.generate_content(user_query)

print("\n\n---------------------\n\n")

print(response.text)
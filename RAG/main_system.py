from utils import detect_input_type
from mitre_tool import query_mitre
from otx_tool import query_otx

user_input = input("Enter query:\n")

input_type = detect_input_type(user_input)

response = {}

if input_type == "technique":
  mitre_data = query_mitre(user_input)
  response["mitre"] = mitre_data

elif input_type == "ip":
  otx_data = query_otx(user_input, "IPv4")
  response["otx"] = otx_data

elif input_type == "hash":
  otx_data = query_otx(user_input, "file")
  response["otx"] = otx_data

elif input_type == "log":
  # For logs, send to RAG to extract technique first
  mitre_data = query_mitre(user_input)
  response["mitre"] = mitre_data

print(response)
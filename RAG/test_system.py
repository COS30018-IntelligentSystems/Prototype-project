import json 
from mitre_tool import query_mitre
from otx_tool import query_otx
from utils import detect_input_type


# ---------------------------
# Main Test Runner
# ---------------------------
if __name__ == "__main__":

  user_input = input("Enter log snippet, technique, or indicator:\n\n")
  input_type = detect_input_type(user_input)

  response = {}

  if input_type == "technique":
    print("\n[+] Querying MITRE RAG...\n")
    response["mitre"] = query_mitre(user_input)

  elif input_type == "ip":
    print("\n[+] Querying OTX for IP intelligence...\n")
    response["otx"] = query_otx(user_input, "IPv4")

  elif input_type == "hash":
    print("\n[+] Querying OTX for file intelligence...\n")
    response["otx"] = query_otx(user_input, "file")

  elif input_type == "log":
    print("\n[+] Sending log to MITRE RAG...\n")
    response["mitre"] = query_mitre(user_input)

  print("\n========== RESULT ==========\n")
  print(json.dumps(response, indent=2))
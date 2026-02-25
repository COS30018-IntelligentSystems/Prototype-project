import re

def detect_input_type(user_input):
  # Detect IP
  ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
  
  # Detect hash (simple MDS/SMA pattern)
  hash_pattern = r"\b[a-fA-F0-9]{32,64}\b"
  
  # Detect MITRE technique ID
  technique_pattern = r"\bT\d{4}\b"
  
  if re.search(ip_pattern, user_input):
    return "ip"
  elif re.search(hash_pattern, user_input):
    return "hash"
  elif re.search(technique_pattern, user_input):
    return "technique"
  else:
    return "log"

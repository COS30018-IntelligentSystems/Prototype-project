"""
Legacy MITRE query interface.

`query_mitre` now delegates to the structured MITRE agent in `rag_system`.
"""

import json

from rag_system.agents.mitre_agent import run_mitre_agent


def query_mitre(user_query: str):
  return run_mitre_agent(user_query)


if __name__ == "__main__":
  user_query = input("What do you want to know about MITRE ATT&CK?\n\n")
  result = query_mitre(user_query)
  print(json.dumps(result, indent=2))

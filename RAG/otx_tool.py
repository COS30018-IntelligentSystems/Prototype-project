from OTXv2 import OTXv2
from dotenv import load_dotenv
import os

load_dotenv()

OTX_API_KEY = os.getenv("OTX_API_KEY")

otx = OTXv2(OTX_API_KEY)

def query_otx(indicator, indicator_type):
  try:
    result = otx.get_indicator_details_full(indicator_type, indicator)
    
    pulse_info = result.get("pulse_info", {})
    pulses = pulse_info.get("pulses", [])
    
    return {
      "indicator": indicator,
      "type": indicator_type,
      "pulse_count": pulse_info.get("count", 0),
      "malware_families": [
        pulse.get("malware_families", [])
        for pulse in pulses
      ],
      "associated_countries": [
        pulse.get("country", "Unknown")
        for pulse in pulses
      ]
    }
    
  except Exception as e:
    return {
      "error": str(e)
    }

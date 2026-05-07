import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

test_alerts = [
    "Multiple failed SSH login attempts from IP 185.220.101.1. Over 50 attempts in 5 minutes.",
    "Ransomware detected - mass file encryption happening on Windows-Target machine.",
    "Privilege escalation detected - user tried to access admin account.",
    "Port scan detected from IP 10.0.0.5 scanning 1000 ports in 30 seconds."
]

SOC_PROMPT = """You are a SOC analyst. Classify this alert and respond in JSON:
{
    "severity": "Critical/High/Medium/Low",
    "attack_type": "name",
    "mitre_technique": "TXXXX",
    "action": "what to do"
}"""

for alert in test_alerts:
    print(f"\n{'='*50}")
    print(f"ALERT: {alert}")
    print(f"{'='*50}")
    
    payload = {
        "model": "phi",
        "prompt": SOC_PROMPT + "\n\nAlert: " + alert,
        "stream": False
    }
    
    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    result = response.json()
    print(f"AI RESPONSE: {result.get('response', 'No response')}")
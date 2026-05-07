# ============================================
# SOC AI TRIAGE BOT
# Author: Ajay Kancherla
# Description: Reads Wazuh alerts and uses
# Ollama AI to automatically classify and
# triage security alerts
# ============================================

import json
import requests
import time
import datetime
import os

# ============================================
# CONFIGURATION — CHANGE THESE TO YOUR VALUES
# ============================================

WAZUH_IP = "192.168.56.105"
WAZUH_USER = "admin"
WAZUH_PASS = "zowZZ32Hoq7kioqBugOcvj.*pN*QB?qe"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi"

THEHIVE_URL = "http://192.168.56.105:9000"
THEHIVE_API_KEY = "YOUR-THEHIVE-API-KEY"

LOG_FILE = "triage_results.json"

# ============================================
# SYSTEM PROMPT FOR AI SOC ANALYST
# ============================================

SOC_ANALYST_PROMPT = """
You are an expert SOC analyst with 10 years experience.
When given a security alert you must respond ONLY in JSON format like this:
{
    "severity": "Critical/High/Medium/Low",
    "attack_type": "Name of the attack",
    "explanation": "What is happening",
    "mitre_technique": "T1XXX - Technique Name",
    "recommended_action": "What SOC analyst should do",
    "false_positive_chance": "High/Medium/Low"
}
Do not write anything outside the JSON.
"""

# ============================================
# FUNCTION: GET WAZUH ALERTS
# ============================================

def get_wazuh_alerts():
    print("[*] Fetching alerts from Wazuh...")
    try:
        url = f"https://{WAZUH_IP}:55000/alerts"
        response = requests.get(
            url,
            auth=(WAZUH_USER, WAZUH_PASS),
            verify=False,
            params={"limit": 10, "sort": "-timestamp"}
        )
        alerts = response.json()
        print(f"[+] Got {len(alerts.get('data', {}).get('affected_items', []))} alerts")
        return alerts.get('data', {}).get('affected_items', [])
    except Exception as e:
        print(f"[-] Error fetching alerts: {e}")
        return []

# ============================================
# FUNCTION: AI TRIAGE ALERT
# ============================================

def ai_triage_alert(alert):
    print(f"[*] Sending alert to AI for triage...")

    alert_text = f"""
    Alert Rule: {alert.get('rule', {}).get('description', 'Unknown')}
    Severity Level: {alert.get('rule', {}).get('level', 'Unknown')}
    Agent Name: {alert.get('agent', {}).get('name', 'Unknown')}
    Source IP: {alert.get('data', {}).get('srcip', 'Unknown')}
    Timestamp: {alert.get('timestamp', 'Unknown')}
    Full Data: {json.dumps(alert.get('data', {}), indent=2)}
    """

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": SOC_ANALYST_PROMPT + "\n\nAlert to analyze:\n" + alert_text,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        result = response.json()
        ai_response = result.get("response", "{}")

        # Parse AI JSON response
        triage_result = json.loads(ai_response)
        print(f"[+] AI Triage Complete: {triage_result.get('severity')} severity")
        return triage_result

    except Exception as e:
        print(f"[-] AI triage error: {e}")
        return {
            "severity": "Unknown",
            "attack_type": "Parse Error",
            "explanation": str(e),
            "mitre_technique": "Unknown",
            "recommended_action": "Manual review required",
            "false_positive_chance": "Unknown"
        }

# ============================================
# FUNCTION: ENRICH WITH OSINT
# ============================================

def enrich_ip(ip_address):
    print(f"[*] Enriching IP {ip_address} with OSINT...")
    try:
        response = requests.get(
            f"https://api.abuseipdb.com/api/v2/check",
            headers={"Key": "YOUR-ABUSEIPDB-API-KEY", "Accept": "application/json"},
            params={"ipAddress": ip_address, "maxAgeInDays": 90}
        )
        data = response.json().get("data", {})
        return {
            "abuse_score": data.get("abuseConfidenceScore", 0),
            "country": data.get("countryCode", "Unknown"),
            "isp": data.get("isp", "Unknown"),
            "total_reports": data.get("totalReports", 0)
        }
    except Exception as e:
        return {"error": str(e)}

# ============================================
# FUNCTION: CREATE THEHIVE CASE
# ============================================

def create_thehive_case(alert, triage_result, osint_data):
    print(f"[*] Creating case in TheHive...")
    try:
        headers = {
            "Authorization": f"Bearer {THEHIVE_API_KEY}",
            "Content-Type": "application/json"
        }

        case_data = {
            "title": f"[{triage_result.get('severity')}] {triage_result.get('attack_type')}",
            "description": f"""
## AI Triage Results

**Severity:** {triage_result.get('severity')}
**Attack Type:** {triage_result.get('attack_type')}
**Explanation:** {triage_result.get('explanation')}
**MITRE Technique:** {triage_result.get('mitre_technique')}
**Recommended Action:** {triage_result.get('recommended_action')}
**False Positive Chance:** {triage_result.get('false_positive_chance')}

## OSINT Enrichment

**Abuse Score:** {osint_data.get('abuse_score')}
**Country:** {osint_data.get('country')}
**ISP:** {osint_data.get('isp')}
**Total Reports:** {osint_data.get('total_reports')}

## Original Alert
{json.dumps(alert, indent=2)}

""",
            "severity": 3 if triage_result.get('severity') == 'Critical' else 2,
            "tags": ["wazuh", "ai-triage", triage_result.get('mitre_technique', 'unknown')],
            "flag": True if triage_result.get('severity') == 'Critical' else False
        }

        response = requests.post(
            f"{THEHIVE_URL}/api/case",
            headers=headers,
            json=case_data,
            verify=False
        )

        if response.status_code == 201:
            case_id = response.json().get('id')
            print(f"[+] Case created in TheHive: {case_id}")
            return case_id
        else:
            print(f"[-] TheHive error: {response.status_code}")
            return None

    except Exception as e:
        print(f"[-] TheHive case creation error: {e}")
        return None

# ============================================
# FUNCTION: SAVE RESULTS TO LOG
# ============================================

def save_results(alert, triage_result, osint_data, case_id):
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "alert_id": alert.get('id', 'unknown'),
        "triage": triage_result,
        "osint": osint_data,
        "thehive_case": case_id
    }

    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)

    logs.append(log_entry)

    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

    print(f"[+] Results saved to {LOG_FILE}")

# ============================================
# MAIN LOOP — RUNS EVERY 60 SECONDS
# ============================================

def main():
    print("=" * 50)
    print("  SOC AI TRIAGE BOT STARTED")
    print("  Author: Ajay Kancherla")
    print("  Checking alerts every 60 seconds")
    print("=" * 50)

    while True:
        print(f"\n[{datetime.datetime.now()}] Checking for new alerts...")

        # Step 1: Get alerts from Wazuh
        alerts = get_wazuh_alerts()

        for alert in alerts:
            print(f"\n--- Processing Alert ---")

            # Step 2: AI triage
            triage_result = ai_triage_alert(alert)

            # Step 3: OSINT enrichment
            src_ip = alert.get('data', {}).get('srcip', '')
            osint_data = enrich_ip(src_ip) if src_ip else {}

            # Step 4: Create TheHive case
            case_id = create_thehive_case(alert, triage_result, osint_data)

            # Step 5: Save results
            save_results(alert, triage_result, osint_data, case_id)

            # Small delay between alerts
            time.sleep(5)

        print(f"\n[*] Sleeping 60 seconds before next check...")
        time.sleep(60)

if __name__ == "__main__":
    main()
    
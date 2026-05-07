# ============================================
# THEHIVE CASE CREATOR
# Author: Ajay Kancherla
# Description: Automatically creates and
# manages incident cases in TheHive based
# on AI triage results
# ============================================

import requests
import json
import datetime

# ============================================
# CONFIGURATION
# ============================================

THEHIVE_URL = "http://192.168.56.105:9000"
THEHIVE_API_KEY = "YOUR-THEHIVE-API-KEY"

HEADERS = {
    "Authorization": f"Bearer {THEHIVE_API_KEY}",
    "Content-Type": "application/json"
}

# ============================================
# SEVERITY MAPPING
# ============================================

SEVERITY_MAP = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4
}

# ============================================
# FUNCTION: CREATE CASE
# ============================================

def create_case(triage_result, alert, osint_data):
    print(f"[*] Creating TheHive case...")

    severity_level = SEVERITY_MAP.get(
        triage_result.get("severity", "Medium"), 2
    )

    case_payload = {
        "title": f"[AI-TRIAGE] [{triage_result.get('severity')}] {triage_result.get('attack_type')}",
        "description": build_description(triage_result, alert, osint_data),
        "severity": severity_level,
        "startDate": int(datetime.datetime.now().timestamp() * 1000),
        "tags": build_tags(triage_result),
        "flag": True if triage_result.get("severity") == "Critical" else False,
        "tlp": 2,
        "pap": 2,
        "status": "New",
        "assignee": "admin@thehive.local"
    }

    try:
        response = requests.post(
            f"{THEHIVE_URL}/api/case",
            headers=HEADERS,
            json=case_payload,
            verify=False
        )

        if response.status_code == 201:
            case = response.json()
            case_id = case.get("_id")
            case_number = case.get("caseId")
            print(f"[+] Case #{case_number} created: {case_id}")

            # Add observables to case
            add_observables(case_id, alert, osint_data)

            # Add task to case
            add_tasks(case_id, triage_result)

            return case_id
        else:
            print(f"[-] Failed to create case: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"[-] Case creation error: {e}")
        return None

# ============================================
# FUNCTION: BUILD DESCRIPTION
# ============================================

def build_description(triage_result, alert, osint_data):
    return f"""
## AI Triage Summary

| Field | Value |
|-------|-------|
| Severity | {triage_result.get('severity')} |
| Attack Type | {triage_result.get('attack_type')} |
| MITRE Technique | {triage_result.get('mitre_technique')} |
| False Positive Chance | {triage_result.get('false_positive_chance')} |

## What Happened

{triage_result.get('explanation')}

## Recommended Action

{triage_result.get('recommended_action')}

## OSINT Intelligence

| Source | Finding |
|--------|---------|
| AbuseIPDB Score | {osint_data.get('abuseipdb', {}).get('abuse_score', 'N/A')} |
| Country | {osint_data.get('geolocation', {}).get('country', 'N/A')} |
| ISP | {osint_data.get('geolocation', {}).get('isp', 'N/A')} |
| VirusTotal Malicious | {osint_data.get('virustotal', {}).get('malicious_votes', 'N/A')} |
| Overall Threat | {osint_data.get('overall_threat', 'N/A')} |

## Original Wazuh Alert

```json
{json.dumps(alert, indent=2)}
```
"""

# ============================================
# FUNCTION: BUILD TAGS
# ============================================

def build_tags(triage_result):
    tags = [
        "wazuh",
        "ai-triage",
        "soc-lab",
        triage_result.get("severity", "unknown").lower(),
        triage_result.get("mitre_technique", "unknown").split(" ")[0]
    ]
    return [tag for tag in tags if tag]

# ============================================
# FUNCTION: ADD OBSERVABLES
# ============================================

def add_observables(case_id, alert, osint_data):
    print(f"[*] Adding observables to case...")

    src_ip = alert.get("data", {}).get("srcip", "")

    if src_ip:
        observable = {
            "dataType": "ip",
            "data": src_ip,
            "message": f"Source IP — Abuse Score: {osint_data.get('abuseipdb', {}).get('abuse_score', 'N/A')}",
            "tags": ["source-ip", "wazuh-alert"],
            "ioc": True if osint_data.get("overall_threat") in ["HIGH", "CRITICAL"] else False
        }

        try:
            response = requests.post(
                f"{THEHIVE_URL}/api/case/{case_id}/artifact",
                headers=HEADERS,
                json=observable,
                verify=False
            )
            if response.status_code == 201:
                print(f"[+] Observable added: {src_ip}")
        except Exception as e:
            print(f"[-] Observable error: {e}")

# ============================================
# FUNCTION: ADD TASKS
# ============================================

def add_tasks(case_id, triage_result):
    print(f"[*] Adding response tasks to case...")

    tasks = [
        {
            "title": "1. Verify Alert — Confirm True Positive",
            "description": "Review the raw Wazuh alert and confirm this is a real threat not a false positive.",
            "status": "Waiting",
            "order": 1
        },
        {
            "title": "2. Investigate Source IP",
            "description": f"Investigate the source IP using OSINT tools. Check AbuseIPDB, VirusTotal, and Shodan.",
            "status": "Waiting",
            "order": 2
        },
        {
            "title": "3. Contain the Threat",
            "description": triage_result.get("recommended_action", "Block source IP and isolate affected host."),
            "status": "Waiting",
            "order": 3
        },
        {
            "title": "4. Document Findings",
            "description": "Document all findings, actions taken, and lessons learned in this case.",
            "status": "Waiting",
            "order": 4
        },
        {
            "title": "5. Close Case",
            "description": "Mark case as resolved with full summary of incident and response.",
            "status": "Waiting",
            "order": 5
        }
    ]

    for task in tasks:
        try:
            response = requests.post(
                f"{THEHIVE_URL}/api/case/{case_id}/task",
                headers=HEADERS,
                json=task,
                verify=False
            )
            if response.status_code == 201:
                print(f"[+] Task added: {task['title']}")
        except Exception as e:
            print(f"[-] Task error: {e}")

# ============================================
# MAIN — TEST CASE CREATION
# ============================================

if __name__ == "__main__":
    # Test data
    test_triage = {
        "severity": "High",
        "attack_type": "SSH Brute Force",
        "explanation": "Multiple failed SSH login attempts detected from single IP",
        "mitre_technique": "T1110 - Brute Force",
        "recommended_action": "Block source IP immediately and review SSH logs",
        "false_positive_chance": "Low"
    }

    test_alert = {
        "rule": {"description": "Multiple SSH login failures", "level": 10},
        "agent": {"name": "windows-target"},
        "data": {"srcip": "185.220.101.1"}
    }

    test_osint = {
        "overall_threat": "HIGH",
        "abuseipdb": {"abuse_score": 89},
        "geolocation": {"country": "Russia", "isp": "Unknown ISP"},
        "virustotal": {"malicious_votes": 7}
    }

    case_id = create_case(test_triage, test_alert, test_osint)
    print(f"\n[+] Test complete. Case ID: {case_id}")

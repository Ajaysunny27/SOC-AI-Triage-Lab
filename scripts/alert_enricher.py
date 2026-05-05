# ============================================
# ALERT ENRICHER
# Author: Ajay Kancherla
# Description: Enriches IP addresses from
# Wazuh alerts with OSINT threat intelligence
# ============================================

import requests
import json
import time

# ============================================
# CONFIGURATION
# ============================================

ABUSEIPDB_KEY = "YOUR-ABUSEIPDB-API-KEY"
VIRUSTOTAL_KEY = "YOUR-VIRUSTOTAL-API-KEY"

# ============================================
# FUNCTION: CHECK ABUSEIPDB
# ============================================

def check_abuseipdb(ip):
    print(f"[*] Checking AbuseIPDB for {ip}")
    try:
        response = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            headers={
                "Key": ABUSEIPDB_KEY,
                "Accept": "application/json"
            },
            params={
                "ipAddress": ip,
                "maxAgeInDays": 90,
                "verbose": True
            }
        )
        data = response.json().get("data", {})
        result = {
            "source": "AbuseIPDB",
            "ip": ip,
            "abuse_score": data.get("abuseConfidenceScore", 0),
            "country": data.get("countryCode", "Unknown"),
            "isp": data.get("isp", "Unknown"),
            "domain": data.get("domain", "Unknown"),
            "total_reports": data.get("totalReports", 0),
            "last_reported": data.get("lastReportedAt", "Never"),
            "is_tor": data.get("isTor", False),
            "is_public": data.get("isPublic", True),
            "threat_level": "HIGH" if data.get("abuseConfidenceScore", 0) > 50 else "LOW"
        }
        print(f"[+] AbuseIPDB Score: {result['abuse_score']} — {result['threat_level']}")
        return result
    except Exception as e:
        print(f"[-] AbuseIPDB error: {e}")
        return {"error": str(e)}

# ============================================
# FUNCTION: CHECK VIRUSTOTAL
# ============================================

def check_virustotal(ip):
    print(f"[*] Checking VirusTotal for {ip}")
    try:
        response = requests.get(
            f"https://www.virustotal.com/api/v3/ip_addresses/{ip}",
            headers={"x-apikey": VIRUSTOTAL_KEY}
        )
        data = response.json().get("data", {})
        attributes = data.get("attributes", {})
        stats = attributes.get("last_analysis_stats", {})

        result = {
            "source": "VirusTotal",
            "ip": ip,
            "malicious_votes": stats.get("malicious", 0),
            "suspicious_votes": stats.get("suspicious", 0),
            "harmless_votes": stats.get("harmless", 0),
            "country": attributes.get("country", "Unknown"),
            "owner": attributes.get("as_owner", "Unknown"),
            "threat_level": "HIGH" if stats.get("malicious", 0) > 3 else "LOW"
        }
        print(f"[+] VirusTotal Malicious: {result['malicious_votes']} — {result['threat_level']}")
        return result
    except Exception as e:
        print(f"[-] VirusTotal error: {e}")
        return {"error": str(e)}

# ============================================
# FUNCTION: CHECK IP GEOLOCATION
# ============================================

def check_geolocation(ip):
    print(f"[*] Getting geolocation for {ip}")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        result = {
            "source": "ip-api",
            "ip": ip,
            "country": data.get("country", "Unknown"),
            "city": data.get("city", "Unknown"),
            "region": data.get("regionName", "Unknown"),
            "isp": data.get("isp", "Unknown"),
            "org": data.get("org", "Unknown"),
            "lat": data.get("lat", 0),
            "lon": data.get("lon", 0),
            "timezone": data.get("timezone", "Unknown")
        }
        print(f"[+] Location: {result['city']}, {result['country']}")
        return result
    except Exception as e:
        print(f"[-] Geolocation error: {e}")
        return {"error": str(e)}

# ============================================
# FUNCTION: FULL IP ENRICHMENT
# ============================================

def enrich_ip_full(ip):
    print(f"\n{'='*40}")
    print(f"  ENRICHING IP: {ip}")
    print(f"{'='*40}")

    enrichment = {
        "ip": ip,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "abuseipdb": check_abuseipdb(ip),
        "virustotal": check_virustotal(ip),
        "geolocation": check_geolocation(ip)
    }

    # Calculate overall threat score
    abuse_score = enrichment["abuseipdb"].get("abuse_score", 0)
    vt_malicious = enrichment["virustotal"].get("malicious_votes", 0)

    if abuse_score > 75 or vt_malicious > 5:
        overall_threat = "CRITICAL"
    elif abuse_score > 50 or vt_malicious > 3:
        overall_threat = "HIGH"
    elif abuse_score > 25 or vt_malicious > 1:
        overall_threat = "MEDIUM"
    else:
        overall_threat = "LOW"

    enrichment["overall_threat"] = overall_threat
    print(f"\n[!] OVERALL THREAT LEVEL: {overall_threat}")

    return enrichment

# ============================================
# MAIN — TEST WITH SAMPLE IP
# ============================================

if __name__ == "__main__":
    # Test with a known malicious IP
    test_ip = "185.220.101.1"
    result = enrich_ip_full(test_ip)
    print(f"\n{json.dumps(result, indent=2)}")
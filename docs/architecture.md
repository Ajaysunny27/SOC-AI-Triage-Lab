# SOC AI Triage Lab — Full Architecture Documentation

## Author: Ajay Kancherla
## Location: Nellore, Andhra Pradesh
## Goal: SOC Analyst / Detection Engineer

---

## Project Summary

This project is a fully functional AI-powered
Security Operations Center home lab built on
open source tools.

The unique feature is the AI triage bot —
it reads Wazuh security alerts automatically,
classifies severity using a local LLM (Ollama
+ Mistral), enriches indicators with OSINT,
and opens incident cases in TheHive without
any human involvement.

This eliminates manual L1 triage — the biggest
pain point in every SOC worldwide.

---

## Full Architecture Flow
ATTACKER LAYER
──────────────
Kali Linux VM
│
│  (runs attacks using Metasploit,
│   Atomic Red Team, Nmap, Hydra)
│
▼
TARGET LAYER
────────────
Windows 10 VM
│  (Wazuh agent installed)
│  (Sysmon installed)
│  (generates Windows event logs)
│
▼
DETECTION LAYER
───────────────
Wazuh Manager (Ubuntu VM)
│  (receives agent logs)
│  (applies detection rules)
│  (fires alerts on suspicious activity)
│
▼
LOG PIPELINE
────────────
Logstash
│  (parses raw logs)
│  (enriches with GeoIP data)
│  (routes to both SIEMs)
│
├──────────────┐
▼              ▼
ELK Stack     Splunk Free
(Primary)     (Secondary)
Kibana        Splunk UI
Dashboard     Dashboard
│              │
└──────┬───────┘
│
▼
AI TRIAGE LAYER
───────────────
Ollama + Mistral (Windows Host)
│  (reads Wazuh alerts via API)
│  (classifies severity with AI)
│  (identifies MITRE technique)
│  (enriches IP with AbuseIPDB)
│  (enriches IP with VirusTotal)
│
▼
CASE MANAGEMENT LAYER
─────────────────────
TheHive
│  (auto case created by bot)
│  (tasks assigned to analyst)
│  (observables added automatically)
│  (IR playbook triggered)
│
▼
SOC ANALYST
───────────
You
(review AI triage results)
(investigate true positives)
(close false positives)
(document incident)
(write final report)

---

## Virtual Machine Specifications

### VM 1 — Wazuh ELK Server
- OS: Ubuntu Server 22.04 LTS
- RAM: 6 GB
- CPU: 4 cores
- Disk: 80 GB
- Services running:
  - Wazuh Manager
  - Elasticsearch
  - Kibana
  - Logstash
  - TheHive
  - Cassandra
  - Splunk Free

### VM 2 — Windows Target
- OS: Windows 10
- RAM: 2 GB
- CPU: 2 cores
- Disk: 50 GB
- Services running:
  - Wazuh Agent
  - Sysmon
  - Winlogbeat

### Host Machine — Windows 11
- Processor: AMD Ryzen 7 7435HS
- RAM: 16 GB
- GPU: RTX 2050 (used by Ollama)
- Services running:
  - Ollama + Mistral AI
  - VirtualBox
  - VS Code

### Attack Machine — Kali Linux (existing VM)
- Used for: attack simulation
- Tools: Metasploit, Nmap, Hydra, Atomic Red Team

---

## Tools and Purpose

| Tool | Version | Purpose |
|------|---------|---------|
| Wazuh | 4.7 | SIEM + XDR + HIDS |
| Elasticsearch | 8.x | Log storage and search |
| Kibana | 8.x | Primary dashboard |
| Logstash | 8.x | Log pipeline |
| Splunk | Free | Secondary dashboard |
| Ollama | Latest | Run AI locally |
| Mistral | 7B | AI model for triage |
| TheHive | 5.2 | Case management |
| Cassandra | 4.0 | TheHive database |
| Sysmon | 15.x | Windows telemetry |
| Winlogbeat | 8.x | Windows log shipper |
| Kali Linux | 2025.4 | Attack simulation |
| Atomic Red Team | Latest | MITRE TTP simulation |

---

## MITRE ATT&CK Coverage

| ID | Technique | Detection Method |
|----|-----------|-----------------|
| T1110 | Brute Force | Wazuh rule + Sigma |
| T1078 | Valid Accounts | Wazuh rule |
| T1059 | Command Scripting | Sysmon + Sigma |
| T1055 | Process Injection | Sysmon + Sigma |
| T1486 | Data Encrypted | Wazuh FIM |
| T1046 | Network Scanning | Zeek + Suricata |
| T1003 | Credential Dumping | Sysmon + Sigma |
| T1190 | Exploit Public App | Suricata rules |

---

## Data Flow Explanation

### Step 1 — Attack Happens
Kali Linux runs an attack against Windows 10 VM.
Example: SSH brute force, port scan, malware execution.

### Step 2 — Agent Detects
Wazuh agent on Windows 10 detects suspicious
activity and sends logs to Wazuh Manager.

### Step 3 — Alert Generated
Wazuh Manager matches logs against detection
rules and generates a security alert.

### Step 4 — Logs Shipped
Logstash collects the alert, enriches it with
GeoIP data, and sends it to both ELK and Splunk.

### Step 5 — AI Reads Alert
The triage bot running on Windows host polls
Wazuh API every 60 seconds for new alerts.

### Step 6 — AI Classifies
Ollama + Mistral reads the alert and responds
with severity, attack type, MITRE technique,
and recommended action in JSON format.

### Step 7 — OSINT Enrichment
The bot checks the source IP against
AbuseIPDB and VirusTotal for threat intel.

### Step 8 — Case Auto Created
TheHive case is automatically created with
full AI analysis, OSINT data, and response
tasks already populated.

### Step 9 — Analyst Reviews
SOC analyst (you) reviews the case in TheHive,
confirms true positive, takes action, and
closes the case with documentation.

---

## Key Innovation

No other home SOC lab on GitHub combines:
- Local AI (Ollama) for alert triage
- Dual SIEM (ELK + Splunk)
- Automatic TheHive case creation
- OSINT enrichment pipeline
- Full MITRE ATT&CK mapping
- Complete IR workflow

This is what makes this project unique and
outstanding for SOC analyst job applications.

---

## Project Completed By

- Name: Ajay Kancherla
- Date: May 2026
- LinkedIn: (add your LinkedIn)
- GitHub: (add your GitHub)
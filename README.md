# SOC-AI-Triage-Lab

An AI-powered Security Operations Center (SOC) home lab that automatically triages alerts using a local LLM (Ollama + Mistral), detects threats via Wazuh, visualizes logs in ELK Stack and Splunk, and auto-creates incident cases in TheHive.

## Project Overview

This project simulates a real enterprise SOC environment built entirely on open-source tools. The AI triage bot reads Wazuh security alerts, classifies severity, enriches indicators with OSINT, and automatically opens cases in TheHive — eliminating manual L1 triage.

## Architecture
Kali Linux (Attacker)
↓
Windows 10 Target VM (Wazuh Agent)
↓
Wazuh Manager (Detection Engine)
↓
Logstash (Log Pipeline)
↙        ↘
ELK Stack    Splunk Free
(Primary)   (Secondary)
↓
Ollama + Mistral (AI Triage Bot)
↓
TheHive (Case Management)
## Tools Used

| Tool | Purpose |
|------|---------|
| Wazuh | SIEM + XDR + HIDS |
| Elasticsearch | Log indexing and search |
| Kibana | Dashboard and visualization |
| Splunk Free | Secondary SIEM dashboard |
| Ollama + Mistral | Local AI for alert triage |
| TheHive | Case management and IR |
| Logstash | Log pipeline and enrichment |
| Kali Linux | Attack simulation |
| Atomic Red Team | MITRE ATT&CK TTP simulation |
| Suricata | Network IDS |

## Lab Specifications

- Host OS: Windows 11
- Hypervisor: VirtualBox
- VM 1: Ubuntu 22.04 (Wazuh + ELK + TheHive) — 6GB RAM
- VM 2: Windows 10 (Target machine) — 2GB RAM
- Ollama runs on host Windows directly using RTX 2050 GPU

## Project Structure
SOC-AI-Triage-Lab/
├── README.md
├── setup/
│   ├── 01_ubuntu_vm.md
│   ├── 02_wazuh.md
│   ├── 03_elk.md
│   ├── 04_ollama.md
│   ├── 05_thehive.md
│   └── 06_splunk.md
├── scripts/
│   ├── triage_bot.py
│   ├── alert_enricher.py
│   └── case_creator.py
├── detections/
│   └── sigma_rules/
├── dashboards/
│   └── kibana_export.json
└── docs/
└── architecture.png
## MITRE ATT&CK Coverage

- T1078 — Valid Accounts
- T1110 — Brute Force
- T1003 — OS Credential Dumping
- T1059 — Command and Scripting Interpreter
- T1055 — Process Injection
- T1190 — Exploit Public-Facing Application

## Setup Guide

Follow the setup guides in order inside the `/setup` folder:

1. Create Ubuntu VM
2. Install Wazuh
3. Install ELK Stack
4. Install Ollama on Windows host
5. Install TheHive
6. Install Splunk Free

## Author

- Name: AJAY KANCHERLA 
- Location: Chitvel, Andhra Pradesh
- Goal: SOC Analyst / Detection Engineer

## License

MIT License
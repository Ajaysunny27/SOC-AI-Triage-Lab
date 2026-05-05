# Sigma Detection Rules

## What are Sigma Rules

Sigma rules are standardized detection rules
used by real SOC teams worldwide.
They work across any SIEM — Wazuh, Splunk, ELK.

## Rule 1 — SSH Brute Force Detection

```yaml
title: SSH Brute Force Attack
id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
status: stable
description: Detects multiple failed SSH login attempts from single IP
author: Ajay Kancherla
date: 2026/05/05
tags:
  - attack.credential_access
  - attack.t1110
logsource:
  product: linux
  service: auth
detection:
  selection:
    EventID: 4625
    LogonType: 10
  timeframe: 5m
  condition: selection | count() by srcip > 5
falsepositives:
  - Legitimate admin forgot password
level: high
```

## Rule 2 — Windows Failed Login Detection

```yaml
title: Multiple Windows Login Failures
id: b2c3d4e5-f6a7-8901-bcde-f12345678901
status: stable
description: Detects brute force against Windows accounts
author: Ajay Kancherla
date: 2026/05/05
tags:
  - attack.credential_access
  - attack.t1110.001
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4625
  timeframe: 5m
  condition: selection | count() by TargetUserName > 5
falsepositives:
  - User forgot password
level: high
```

## Rule 3 — Privilege Escalation Detection

```yaml
title: Suspicious Privilege Escalation
id: c3d4e5f6-a7b8-9012-cdef-123456789012
status: stable
description: Detects attempts to escalate privileges on Windows
author: Ajay Kancherla
date: 2026/05/05
tags:
  - attack.privilege_escalation
  - attack.t1055
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4672
    SubjectUserName|endswith: '$'
  condition: selection
falsepositives:
  - Legitimate admin activity
level: critical
```

## Rule 4 — Malicious PowerShell Detection

```yaml
title: Malicious PowerShell Execution
id: d4e5f6a7-b8c9-0123-defa-234567890123
status: stable
description: Detects suspicious PowerShell commands used by attackers
author: Ajay Kancherla
date: 2026/05/05
tags:
  - attack.execution
  - attack.t1059.001
logsource:
  product: windows
  service: powershell
detection:
  selection:
    EventID: 4104
    ScriptBlockText|contains:
      - 'Invoke-Mimikatz'
      - 'IEX'
      - 'DownloadString'
      - 'EncodedCommand'
      - 'bypass'
  condition: selection
falsepositives:
  - Legitimate admin scripts
level: critical
```

## Rule 5 — Ransomware File Encryption Detection

```yaml
title: Ransomware File Encryption Behaviour
id: e5f6a7b8-c9d0-1234-efab-345678901234
status: stable
description: Detects mass file modifications typical of ransomware
author: Ajay Kancherla
date: 2026/05/05
tags:
  - attack.impact
  - attack.t1486
logsource:
  product: windows
  service: sysmon
detection:
  selection:
    EventID: 11
    TargetFilename|endswith:
      - '.encrypted'
      - '.locked'
      - '.crypto'
      - '.ransomware'
  timeframe: 1m
  condition: selection | count() > 20
falsepositives:
  - Legitimate encryption software
level: critical
```

## Rule 6 — Network Port Scan Detection

```yaml
title: Network Port Scan Detected
id: f6a7b8c9-d0e1-2345-fabc-456789012345
status: stable
description: Detects Nmap or other port scanning activity
author: Ajay Kancherla
date: 2026/05/05
tags:
  - attack.discovery
  - attack.t1046
logsource:
  product: zeek
  service: conn
detection:
  selection:
    proto: tcp
    conn_state: 'S0'
  timeframe: 1m
  condition: selection | count() by id.orig_h > 100
falsepositives:
  - Network monitoring tools
level: medium
```

## MITRE ATT&CK Coverage Map

| Rule | Technique | Tactic |
|------|-----------|--------|
| SSH Brute Force | T1110 | Credential Access |
| Windows Login Failure | T1110.001 | Credential Access |
| Privilege Escalation | T1055 | Privilege Escalation |
| Malicious PowerShell | T1059.001 | Execution |
| Ransomware Detection | T1486 | Impact |
| Port Scan Detection | T1046 | Discovery |
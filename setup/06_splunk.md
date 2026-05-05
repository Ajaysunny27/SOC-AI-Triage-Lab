# Step 06 — Install Splunk Free on Ubuntu VM

## What is Splunk

Splunk is an enterprise SIEM used by large
companies worldwide. We add it as a secondary
dashboard alongside ELK Stack.

Having both ELK and Splunk in one project
makes your resume extremely strong.

## Download Splunk Free

On your Windows PC:
1. Go to: https://www.splunk.com/en_us/download/splunk-enterprise.html
2. Create a free Splunk account
3. Download Splunk Enterprise (free 60 day trial)
4. Choose Linux .deb package
5. Copy the .deb file to your Ubuntu VM

## Copy File to Ubuntu VM

On Windows open Command Prompt:
```bash
scp C:\Users\Ajay\Downloads\splunk-*.deb socadmin@YOUR-VM-IP:/home/socadmin/
```

## Install Splunk on Ubuntu VM

```bash
sudo dpkg -i splunk-*.deb
```

## Start Splunk

```bash
sudo /opt/splunk/bin/splunk start --accept-license
```

When asked:
- Admin username: admin
- Admin password: SOClab@2026

## Enable Splunk on Boot

```bash
sudo /opt/splunk/bin/splunk enable boot-start
```

## Access Splunk Dashboard

1. Open browser on Windows PC
2. Go to: http://YOUR-VM-IP:8000
3. Login with admin / SOClab@2026
4. You should see Splunk dashboard

## Connect Wazuh Logs to Splunk

Install Splunk Universal Forwarder on Ubuntu:

```bash
sudo /opt/splunk/bin/splunk add monitor /var/ossec/logs/alerts/alerts.json -index wazuh -sourcetype wazuh
```

## Restart Splunk

```bash
sudo /opt/splunk/bin/splunk restart
```

## Verify Logs Coming In

1. In Splunk dashboard
2. Click Search and Reporting
3. Type in search box:
   index=wazuh
4. You should see Wazuh alerts appearing

## Create Splunk Dashboard

1. Click Dashboards
2. Click Create New Dashboard
3. Name: SOC Overview
4. Add panels:
   - Alert count by severity
   - Top attacking IPs
   - Alert timeline
5. Save dashboard

## Take Screenshots

Take screenshots of:
- Splunk dashboard with alerts
- Search results showing Wazuh logs
- Your custom dashboard

These screenshots go in your GitHub docs folder.

## All Setup Complete

You now have:
- Wazuh running and detecting threats
- ELK Stack collecting and visualizing logs
- Splunk showing same logs differently
- TheHive ready for case management
- Ollama AI ready on Windows host

## Next Step

Go to scripts/triage_bot.py to run the AI
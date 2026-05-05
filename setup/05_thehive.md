# Step 05 — Install TheHive on Ubuntu VM

## What is TheHive

TheHive is a case management platform used by
real SOC teams to track security incidents.

In our lab the AI triage bot automatically
creates cases in TheHive when it detects threats.

## Go Back to Your Ubuntu VM

1. Open VirtualBox
2. Start Wazuh-ELK-Server VM
3. Login with socadmin / SOClab@2026

## Install Java First

```bash
sudo apt-get install -y openjdk-11-jre-headless
```

## Install Cassandra Database

```bash
wget -qO - https://downloads.apache.org/cassandra/KEYS | sudo gpg --dearmor -o /usr/share/keyrings/cassandra-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/cassandra-archive-keyring.gpg] https://debian.cassandra.apache.org 40x main" | sudo tee /etc/apt/sources.list.d/cassandra.sources.list

sudo apt-get update
sudo apt-get install cassandra -y
```

## Configure Cassandra

```bash
sudo nano /etc/cassandra/cassandra.yaml
```

Find and change:
cluster_name: 'thehive'
listen_address: localhost
rpc_address: localhost

Press Ctrl+X then Y then Enter to save.

## Start Cassandra

```bash
sudo systemctl start cassandra
sudo systemctl enable cassandra
```

## Install TheHive

```bash
wget -O- https://archives.strangebee.com/keys/strangebee.gpg | sudo gpg --dearmor -o /usr/share/keyrings/strangebee-archive-keyring.gpg

echo 'deb [signed-by=/usr/share/keyrings/strangebee-archive-keyring.gpg] https://deb.strangebee.com thehive-5.2 main' | sudo tee /etc/apt/sources.list.d/strangebee.list

sudo apt-get update
sudo apt-get install -y thehive
```

## Configure TheHive

```bash
sudo nano /etc/thehive/application.conf
```

Find and change:
db.janusgraph.storage.hostname = ["127.0.0.1"]
index.search.hostname = ["127.0.0.1"]
application.baseUrl = "http://YOUR-VM-IP:9000"

Press Ctrl+X then Y then Enter to save.

## Start TheHive

```bash
sudo systemctl start thehive
sudo systemctl enable thehive
```

## Access TheHive Dashboard

1. Open browser on Windows PC
2. Go to: http://YOUR-VM-IP:9000
3. Default login:
   - Email: admin@thehive.local
   - Password: secret

## Change Default Password

1. Login to TheHive
2. Go to Settings
3. Change password immediately
4. New password: SOClab@2026

## Create SOC Analyst Account

1. Go to Users section
2. Click Add User
3. Fill in your details
4. Role: Analyst

## Verify TheHive Working

1. Click New Case button
2. Create a test case
3. If it saves successfully TheHive is working

## Next Step

Go to 06_splunk.md to install Splunk Free

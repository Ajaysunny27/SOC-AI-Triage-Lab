# Step 03 — Install ELK Stack

## What is ELK

- E = Elasticsearch (stores all logs)
- L = Logstash (processes and routes logs)
- K = Kibana (dashboard to see everything)

All 3 install on your same Ubuntu VM.

## Install Elasticsearch

```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list

sudo apt-get update
sudo apt-get install elasticsearch -y
```

## Configure Elasticsearch

```bash
sudo nano /etc/elasticsearch/elasticsearch.yml
```

Find and change these lines:
network.host: 0.0.0.0
http.port: 9200
xpack.security.enabled: false

Press Ctrl+X then Y then Enter to save.

## Start Elasticsearch

```bash
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch
```

## Verify Elasticsearch Running

```bash
curl http://localhost:9200
```

You should see JSON output with cluster info.

## Install Kibana

```bash
sudo apt-get install kibana -y
```

## Configure Kibana

```bash
sudo nano /etc/kibana/kibana.yml
```

Find and change these lines:
server.port: 5601
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://localhost:9200"]

Press Ctrl+X then Y then Enter to save.

## Start Kibana

```bash
sudo systemctl enable kibana
sudo systemctl start kibana
```

## Install Logstash

```bash
sudo apt-get install logstash -y
```

## Create Logstash Pipeline

```bash
sudo nano /etc/logstash/conf.d/wazuh.conf
```

Paste this:
input {
beats {
port => 5044
}
}
filter {
if [agent][type] == "wazuh" {
mutate {
add_tag => ["wazuh"]
}
}
}
output {
elasticsearch {
hosts => ["localhost:9200"]
index => "wazuh-alerts-%{+YYYY.MM.dd}"
}
}

Press Ctrl+X then Y then Enter to save.

## Start Logstash

```bash
sudo systemctl enable logstash
sudo systemctl start logstash
```

## Access Kibana Dashboard

1. Open browser on Windows PC
2. Go to: http://YOUR-VM-IP:5601
3. You should see Kibana dashboard

## Verify All Services Running

```bash
sudo systemctl status elasticsearch
sudo systemctl status kibana
sudo systemctl status logstash
```

All should show: active (running)

## Next Step

Go to 04_ollama.md to install Ollama AI
# Step 04 — Install Ollama on Windows Host

## What is Ollama

Ollama runs AI models locally on your PC.
We use it to automatically read Wazuh alerts
and classify them using AI.

Your RTX 2050 GPU will make it run very fast.

## Download Ollama

1. Go to: https://ollama.com/download
2. Click Download for Windows
3. Install it like a normal Windows app
4. Click Next, Next, Finish

## Verify Ollama Installed

Open Command Prompt on Windows and type:
```bash
ollama --version
```

You should see a version number.

## Download Mistral AI Model

In Command Prompt type:
```bash
ollama pull mistral
```

This downloads the Mistral AI model.
Size is about 4GB — wait for it to finish.

## Test Ollama is Working

```bash
ollama run mistral "Hello, are you working?"
```

You should get a response from the AI.

## Enable Ollama API

Ollama runs as an API on port 11434.
Test it by opening browser and going to:
http://localhost:11434

You should see: Ollama is running

## Test AI Alert Triage Manually

Open Command Prompt and paste this:
```bash
curl http://localhost:11434/api/generate -d "{\"model\": \"mistral\", \"prompt\": \"A Wazuh alert says: Multiple failed SSH login attempts from IP 192.168.1.105. Classify severity as Critical, High, Medium or Low and explain why.\", \"stream\": false}"
```

You should get an AI response classifying the alert.

## GPU Acceleration Verify

Open Task Manager on Windows:
1. Press Ctrl + Shift + Esc
2. Click Performance tab
3. Click GPU
4. When Ollama runs you should see GPU usage spike

This confirms RTX 2050 is being used.

## Configure Ollama for SOC Lab

Create a file called socanalyst.txt on Desktop
with this content:
You are an expert SOC analyst with 10 years experience.
When given a security alert you must:

Classify severity: Critical, High, Medium or Low
Explain what the attack is
Give recommended response action
State which MITRE ATT&CK technique this matches
Always respond in JSON format.

## Next Step

Go to 05_thehive.md to install TheHive

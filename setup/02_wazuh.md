# Step 02 — Install Wazuh on Ubuntu VM

## First — Start Your Ubuntu VM

1. Open VirtualBox
2. Start your Wazuh-ELK-Server VM
3. Login with:
   - Username: socadmin
   - Password: SOClab@2026

## Update Ubuntu First

Type these commands one by one:

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

## Install Wazuh Manager

Copy and paste these commands one by one:

```bash
curl -sO https://packages.wazuh.com/4.7/wazuh-install.sh
curl -sO https://packages.wazuh.com/4.7/config.yml
```

## Edit Config File

```bash
nano config.yml
```

Change this line:
- Replace `<wazuh-manager-ip>` with `127.0.0.1`

Press Ctrl+X then Y then Enter to save.

## Run the Installer

```bash
sudo bash wazuh-install.sh -a
```

This will take 10-15 minutes. Wait for it to finish.

## Save Your Credentials

When installation finishes you will see:
- Wazuh username: admin
- Wazuh password: (auto generated)

**COPY AND SAVE THIS PASSWORD SOMEWHERE SAFE**

## Access Wazuh Dashboard

1. Open browser on your Windows PC
2. Go to: https://YOUR-VM-IP
3. Login with admin credentials
4. You should see Wazuh dashboard

## Find Your VM IP Address

In the Ubuntu terminal type:
```bash
ip a
```

Look for the number next to `inet` — that is your VM IP.

## Install Wazuh Agent on Windows 10 Target VM

On your Windows 10 VM:
1. Go to: https://packages.wazuh.com/4.x/windows/wazuh-agent-4.7.0-1.msi
2. Download and install
3. During install enter your Ubuntu VM IP as manager address
4. Start the agent service

## Verify Agent Connected

In Wazuh dashboard:
- Go to Agents section
- You should see your Windows VM listed as Active

## Next Step

Go to 03_elk.md to install ELK Stack
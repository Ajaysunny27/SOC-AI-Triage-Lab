# Step 01 — Create Ubuntu VM in VirtualBox

## Download Ubuntu 22.04

1. Go to: https://ubuntu.com/download/server
2. Download Ubuntu Server 22.04 LTS (the .iso file)
3. Save it to your C: drive

## Create New VM in VirtualBox

1. Open VirtualBox
2. Click New button
3. Fill in these details exactly:
   - Name: Wazuh-ELK-Server
   - Type: Linux
   - Version: Ubuntu (64-bit)
   - Click Next

## RAM and CPU Settings

- RAM: 6144 MB (6GB)
- CPU: 4 cores
- Click Next

## Hard Disk Settings

- Select: Create a virtual hard disk now
- Size: 80 GB
- Type: VDI
- Storage: Dynamically allocated
- Click Create

## Attach the Ubuntu ISO

1. Click on your new VM
2. Click Settings
3. Go to Storage
4. Click the empty CD icon
5. Click the small disc icon on the right
6. Choose your downloaded Ubuntu .iso file
7. Click OK

## Start the VM

1. Click Start
2. Ubuntu installer will load
3. Follow installation steps:
   - Choose English
   - Choose Install Ubuntu Server
   - Network: leave default (DHCP)
   - Storage: Use entire disk
   - Username: socadmin
   - Password: SOClab@2026
   - Hostname: wazuh-server
4. Wait for installation to complete
5. Reboot when asked

## After Installation — Take Snapshot

1. In VirtualBox click Machine
2. Click Take Snapshot
3. Name it: Fresh Install
4. This saves your clean state

## Next Step


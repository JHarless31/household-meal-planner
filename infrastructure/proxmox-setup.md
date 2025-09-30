# Proxmox VM Setup Guide

Complete guide for deploying the Household Meal Planning System on a Proxmox VM.

## Overview

This guide walks you through:
1. Creating a VM in Proxmox
2. Installing Ubuntu Server 22.04 LTS
3. Configuring network (static IP, firewall)
4. Installing Docker and Docker Compose
5. Deploying the application
6. Setting up backups and maintenance

**Estimated time:** 60-90 minutes

---

## Prerequisites

- Proxmox VE 7.0+ installed and running
- Ubuntu Server 22.04 LTS ISO uploaded to Proxmox
- Access to Proxmox web interface
- Basic familiarity with Linux command line

---

## Part 1: Create VM in Proxmox

### Step 1.1: Open Proxmox Web Interface

1. Navigate to your Proxmox server: `https://proxmox-ip:8006`
2. Login with your credentials
3. Select your node from the left sidebar

### Step 1.2: Create New VM

1. Click **"Create VM"** button (top right)
2. **General Tab:**
   - **Node:** Select your Proxmox node
   - **VM ID:** Auto-assigned (or choose custom, e.g., 100)
   - **Name:** `meal-planning-vm`
   - **Resource Pool:** (optional)
   - Check **"Start at boot"**

3. **OS Tab:**
   - **Use CD/DVD disc image file (iso)**
   - **Storage:** Select storage containing Ubuntu ISO
   - **ISO image:** Select `ubuntu-22.04-server-amd64.iso`
   - **Type:** Linux
   - **Version:** 6.x - 2.6 Kernel

4. **System Tab:**
   - **Graphic card:** Default
   - **Machine:** Default (i440fx)
   - **BIOS:** Default (SeaBIOS)
   - **SCSI Controller:** VirtIO SCSI
   - **Qemu Agent:** ✓ Check (we'll install later)

5. **Disks Tab:**
   - **Bus/Device:** SCSI 0
   - **Storage:** Select your storage
   - **Disk size (GiB):** **50** (minimum)
   - **Cache:** Default (No cache)
   - **Discard:** ✓ Check (if using SSD)
   - **SSD emulation:** ✓ Check (if using SSD)

6. **CPU Tab:**
   - **Sockets:** 1
   - **Cores:** **4** (recommended minimum)
   - **Type:** host (for best performance)

7. **Memory Tab:**
   - **Memory (MiB):** **8192** (8 GB recommended minimum)
   - **Minimum memory (MiB):** 2048 (for ballooning)
   - **Ballooning Device:** ✓ Check

8. **Network Tab:**
   - **Bridge:** vmbr0 (or your main bridge)
   - **Model:** VirtIO (paravirtualized)
   - **Firewall:** ✓ Check (optional)

9. **Confirm Tab:**
   - Review all settings
   - ✓ Check **"Start after created"**
   - Click **"Finish"**

---

## Part 2: Install Ubuntu Server

### Step 2.1: Start Installation

1. Select your VM in Proxmox sidebar
2. Click **"Console"** to open VNC console
3. Ubuntu installer should boot automatically

### Step 2.2: Ubuntu Installation Steps

**Language Selection:**
- Select: **English**

**Installer Update:**
- Select: **Continue without updating** (faster)

**Keyboard Configuration:**
- Layout: **English (US)** or your preference

**Network Connections:**
- Use DHCP for now (we'll set static IP later)
- Select: **Done**

**Proxy Configuration:**
- Leave blank (local network)
- Select: **Done**

**Ubuntu Archive Mirror:**
- Use default
- Select: **Done**

**Guided Storage Configuration:**
- Select: **Use an entire disk**
- Select disk: `/dev/sda` (50GB)
- ✓ Check **Set up this disk as an LVM group**
- Select: **Done**
- Confirm: **Continue** (will erase disk)

**Storage Configuration:**
- Review layout
- Select: **Done**
- Confirm: **Continue**

**Profile Setup:**
- **Your name:** Your name
- **Your server's name:** `meal-planning-server`
- **Pick a username:** `admin` (or your preference)
- **Choose a password:** Strong password
- **Confirm your password:** Re-enter password
- Select: **Done**

**SSH Setup:**
- ✓ Check **Install OpenSSH server**
- **Import SSH identity:** No (unless you have GitHub/Launchpad keys)
- Select: **Done**

**Featured Server Snaps:**
- Do not select any
- Select: **Done**

**Installation Progress:**
- Wait for installation to complete (5-10 minutes)
- When complete: **Reboot Now**

### Step 2.3: First Boot

1. VM will reboot
2. Remove installation media (Proxmox does this automatically)
3. Login with your username and password
4. You should see the Ubuntu command prompt

---

## Part 3: Initial System Configuration

### Step 3.1: Update System

```bash
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
```

### Step 3.2: Install Useful Tools

```bash
sudo apt install -y \
    curl \
    wget \
    git \
    vim \
    htop \
    net-tools \
    ca-certificates \
    gnupg \
    lsb-release
```

### Step 3.3: Install QEMU Guest Agent

```bash
sudo apt install -y qemu-guest-agent
sudo systemctl enable qemu-guest-agent
sudo systemctl start qemu-guest-agent
```

**Verify in Proxmox:**
- Go to VM Summary page
- You should now see IP address and other info

### Step 3.4: Configure Static IP

**Find current IP and gateway:**
```bash
ip addr show
ip route show
```

**Edit netplan configuration:**
```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

**Replace contents with:**
```yaml
network:
  version: 2
  ethernets:
    ens18:  # Your interface name (might be different)
      addresses:
        - 192.168.1.100/24  # Choose an IP in your network range
      routes:
        - to: default
          via: 192.168.1.1  # Your gateway
      nameservers:
        addresses:
          - 192.168.1.1  # Your DNS server
          - 8.8.8.8      # Google DNS (backup)
```

**Apply configuration:**
```bash
sudo netplan apply
```

**Verify:**
```bash
ip addr show
ping -c 4 google.com
```

### Step 3.5: Configure Hostname

**Edit hosts file:**
```bash
sudo hostnamectl set-hostname meal-planner.local
sudo nano /etc/hosts
```

**Add line:**
```
192.168.1.100   meal-planner.local meal-planner
```

---

## Part 4: Install Docker & Docker Compose

### Step 4.1: Install Docker

**Remove old versions (if any):**
```bash
sudo apt remove docker docker-engine docker.io containerd runc
```

**Add Docker's official GPG key:**
```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

**Set up Docker repository:**
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**Install Docker Engine:**
```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

**Verify installation:**
```bash
sudo docker --version
sudo docker compose version
```

### Step 4.2: Configure Docker

**Add your user to docker group:**
```bash
sudo usermod -aG docker $USER
newgrp docker  # Activate group (or logout/login)
```

**Verify docker works without sudo:**
```bash
docker ps
```

**Enable Docker to start on boot:**
```bash
sudo systemctl enable docker
```

---

## Part 5: Configure Firewall (UFW)

### Step 5.1: Install and Configure UFW

```bash
sudo apt install -y ufw
```

**Set default policies:**
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

**Allow SSH (important!):**
```bash
sudo ufw allow ssh
```

**Allow HTTP and HTTPS (local network only):**
```bash
# Replace 192.168.1.0/24 with your network
sudo ufw allow from 192.168.1.0/24 to any port 80
sudo ufw allow from 192.168.1.0/24 to any port 443
```

**Enable firewall:**
```bash
sudo ufw enable
```

**Verify status:**
```bash
sudo ufw status verbose
```

---

## Part 6: Deploy Application

### Step 6.1: Clone Repository

```bash
cd ~
git clone <your-repository-url> meal-planning-system
cd meal-planning-system
```

### Step 6.2: Configure Environment Variables

```bash
cp .env.example .env
nano .env
```

**Edit the following (REQUIRED):**
```env
# Database
DB_PASSWORD=<generate-strong-password>

# Authentication
JWT_SECRET=<generate-strong-secret>
SESSION_SECRET=<generate-strong-secret>

# Application
ENVIRONMENT=production
```

**Generate secrets:**
```bash
# For DB_PASSWORD, JWT_SECRET, SESSION_SECRET:
openssl rand -base64 32
```

### Step 6.3: Generate SSL Certificate

```bash
cd infrastructure
./generate-ssl.sh
```

**Follow instructions to trust certificate on your devices.**

### Step 6.4: Build and Start Containers

```bash
cd infrastructure
docker compose up -d --build
```

**This will:**
- Build backend image (~5 minutes)
- Build frontend image (~5 minutes)
- Pull PostgreSQL and Nginx images
- Start all containers
- Initialize database

**Monitor progress:**
```bash
docker compose logs -f
```

**Press Ctrl+C to exit logs (containers keep running)**

### Step 6.5: Verify Deployment

**Check container status:**
```bash
docker compose ps
```

All containers should show `Up` status.

**Check logs:**
```bash
docker compose logs backend
docker compose logs frontend
docker compose logs postgres
```

**Test API:**
```bash
curl http://localhost:8000/api/health
```

Should return: `{"status": "healthy"}`

### Step 6.6: Access Application

From another device on your network:
- **HTTP:** http://192.168.1.100 (redirects to HTTPS)
- **HTTPS:** https://192.168.1.100
- **or:** https://meal-planner.local (if DNS/mDNS configured)

**First time:** Browser will show security warning (self-signed cert).
- Click "Advanced" → "Accept Risk and Continue"

---

## Part 7: Create Admin User

Currently, there's no admin user. You'll need to create one via API or database.

**Option 1: Via API (if registration is open):**
```bash
curl -X POST https://meal-planner.local/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "YourSecurePassword123!"
  }'
```

**Then manually promote to admin in database:**
```bash
docker compose exec postgres psql -U household_app -d household_db -c \
  "UPDATE shared.users SET role='admin' WHERE username='admin';"
```

**Option 2: Via database directly:**
```bash
# Generate bcrypt hash of password
docker compose exec backend python -c \
  "from passlib.hash import bcrypt; print(bcrypt.hash('YourSecurePassword123!'))"

# Copy the hash output, then:
docker compose exec postgres psql -U household_app -d household_db

INSERT INTO shared.users (username, email, password_hash, role)
VALUES ('admin', 'admin@example.com', '<paste-hash-here>', 'admin');
\q
```

---

## Part 8: Backup Configuration

### Step 8.1: Create Backup Script

```bash
sudo nano /usr/local/bin/backup-meal-planner.sh
```

**Paste:**
```bash
#!/bin/bash
BACKUP_DIR="/backups/meal-planner"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
docker compose -f /home/admin/meal-planning-system/infrastructure/docker-compose.yml \
  exec -T postgres pg_dump -U household_app household_db \
  > "$BACKUP_DIR/db_$DATE.sql"

# Backup uploads
tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" \
  -C /var/lib/docker/volumes/meal_planner_uploads/_data .

# Backup environment
cp /home/admin/meal-planning-system/.env "$BACKUP_DIR/env_$DATE"

# Cleanup old backups (keep last 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "env_*" -mtime +30 -delete

echo "Backup completed: $DATE"
```

**Make executable:**
```bash
sudo chmod +x /usr/local/bin/backup-meal-planner.sh
```

### Step 8.2: Schedule Daily Backups

```bash
sudo crontab -e
```

**Add line:**
```
0 2 * * * /usr/local/bin/backup-meal-planner.sh >> /var/log/meal-planner-backup.log 2>&1
```

**Test backup:**
```bash
sudo /usr/local/bin/backup-meal-planner.sh
```

---

## Part 9: Maintenance

### Update Application

```bash
cd ~/meal-planning-system
git pull
cd infrastructure
docker compose down
docker compose up -d --build
```

### View Logs

```bash
cd ~/meal-planning-system/infrastructure
docker compose logs -f [service_name]
```

### Restart Services

```bash
docker compose restart [service_name]
```

### Stop Application

```bash
docker compose down
```

### Start Application

```bash
docker compose up -d
```

---

## Part 10: Troubleshooting

### Container won't start

```bash
docker compose logs [service_name]
docker compose ps
```

### Database connection errors

```bash
docker compose exec postgres psql -U household_app -d household_db -c "\l"
```

### Disk space issues

```bash
df -h
docker system prune -a
```

### Reset everything (CAUTION: Deletes all data)

```bash
docker compose down -v
docker compose up -d --build
```

---

## Part 11: Optional Enhancements

### Configure mDNS (Avahi)

For `meal-planner.local` to work across network:

```bash
sudo apt install -y avahi-daemon
sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon
```

### Enable Automatic Security Updates

```bash
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

---

## Success Criteria

✅ VM created and running
✅ Ubuntu Server installed
✅ Static IP configured
✅ Docker installed and running
✅ Application accessible via HTTPS
✅ Admin user created
✅ Backups scheduled

**You're done!** Your Household Meal Planning System is now running on Proxmox.

---

## Support

For issues or questions:
- Check logs: `docker compose logs`
- Review documentation: `docs/`
- Open GitHub issue

---

**Congratulations!** You've successfully deployed the application. 🎉

# Deployment Guide

## Table of Contents

1. [Overview](#overview)
2. [Deployment Options](#deployment-options)
3. [Prerequisites](#prerequisites)
4. [Local Development Deployment](#local-development-deployment)
5. [Production Deployment (Proxmox VM)](#production-deployment-proxmox-vm)
6. [Cloud Deployment Options](#cloud-deployment-options)
7. [Docker Deployment](#docker-deployment)
8. [Database Migration](#database-migration)
9. [Continuous Deployment](#continuous-deployment)
10. [Post-Deployment](#post-deployment)
11. [Troubleshooting Deployment](#troubleshooting-deployment)

---

## Overview

This guide provides step-by-step instructions for deploying the Household Meal Planning System in various environments.

### Architecture Diagram

```
┌──────────────┐
│   Client     │
│  (Browser)   │
└──────┬───────┘
       │ HTTPS
       ▼
┌──────────────┐
│    Nginx     │ ← Reverse Proxy
│  (Port 443)  │
└──┬───────────┘
   │
   ├─────────────────┐
   │                 │
   ▼                 ▼
┌────────┐      ┌──────────┐
│Frontend│      │ Backend  │
│Next.js │      │ FastAPI  │
│Port 3000      │ Port 8000│
└────────┘      └─────┬────┘
                      │
                      ▼
               ┌──────────────┐
               │  PostgreSQL  │
               │  Port 5432   │
               └──────────────┘
```

All services run in Docker containers.

### Deployment Timeline

- **Local Development**: 30 minutes
- **Proxmox VM**: 60-90 minutes
- **Cloud Deployment**: 45-60 minutes

---

## Deployment Options

### Option 1: Local Development

**Best for:**
- Development and testing
- Local experimentation
- Learning the system

**Requirements:**
- Docker Desktop or Docker Engine
- 4 GB RAM
- 10 GB disk space

---

### Option 2: Production (Proxmox VM)

**Best for:**
- Home lab deployment
- On-premises hosting
- Full control over environment

**Requirements:**
- Proxmox VE 7.0+
- Ubuntu Server 22.04 LTS
- 8 GB RAM, 50 GB SSD
- Local network

See [infrastructure/proxmox-setup.md](../infrastructure/proxmox-setup.md) for detailed Proxmox VM setup.

---

### Option 3: Cloud Deployment

**Best for:**
- Remote access
- High availability
- Managed infrastructure

**Providers:**
- AWS (EC2 + RDS)
- DigitalOcean (Droplet + Managed Database)
- Google Cloud Platform
- Microsoft Azure

---

## Prerequisites

### Software Requirements

**Required:**
- Docker 24+
- Docker Compose 2.20+
- Git
- Text editor

**Optional:**
- Nginx (for reverse proxy)
- Certbot (for SSL certificates)

### Installation Commands

**Install Docker (Ubuntu/Debian):**

```bash
# Update package index
sudo apt update

# Install prerequisites
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect
```

**Install Docker Compose:**

```bash
# Docker Compose v2 is included with Docker
docker compose version

# If not installed, install manually
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

---

## Local Development Deployment

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd meal-planning-system
```

### Step 2: Configure Environment

```bash
# Navigate to infrastructure directory
cd infrastructure

# Copy example environment file
cp .env.example .env

# Edit .env file
nano .env
```

**Important:** The `.env` file must be in the `infrastructure/` directory where `docker-compose.yml` is located.

**Required variables:**

```bash
# Database
DATABASE_URL=postgresql://meal_planner:devpassword@postgres:5432/household_db

# Authentication
SECRET_KEY=your-secret-key-here  # Generate with: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Application
APP_NAME=Household Meal Planning
DEBUG=True
```

### Step 3: Build and Start Services

```bash
# Build Docker images
docker compose build

# Start all services
docker compose up -d

# View logs
docker compose logs -f
```

### Step 4: Initialize Database

```bash
# Run database initialization
docker compose exec backend python scripts/init_db.py

# Or manually run SQL files
docker compose exec postgres psql -U meal_planner -d household_db -f /docker-entrypoint-initdb.d/01_shared_schema.sql
docker compose exec postgres psql -U meal_planner -d household_db -f /docker-entrypoint-initdb.d/02_meal_planning_schema.sql
```

### Step 5: Create Admin User

```bash
# Using script
docker compose exec backend python scripts/create_admin.py

# Follow prompts to enter username, email, password
```

### Step 6: Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Test the deployment:**

```bash
# Check health
curl http://localhost:8000/api/health

# Should return: {"status":"healthy"}
```

---

## Production Deployment (Proxmox VM)

### Overview

This section covers deploying to a Proxmox VM with Ubuntu Server 22.04 LTS.

For detailed Proxmox VM creation, see [infrastructure/proxmox-setup.md](../infrastructure/proxmox-setup.md).

### Step 1: Server Preparation

#### 1.1 Create and Configure VM

Follow [infrastructure/proxmox-setup.md](../infrastructure/proxmox-setup.md) to:

- Create Proxmox VM
- Install Ubuntu Server 22.04
- Configure network (static IP)
- Set up SSH access

#### 1.2 Update System

```bash
# Update package lists
sudo apt update

# Upgrade packages
sudo apt upgrade -y

# Install essential tools
sudo apt install -y curl wget git vim htop net-tools
```

#### 1.3 Configure Firewall

```bash
# Enable firewall
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS from local network only
sudo ufw allow from 192.168.1.0/24 to any port 80
sudo ufw allow from 192.168.1.0/24 to any port 443

# Check status
sudo ufw status verbose
```

### Step 2: Install Docker

```bash
# Install Docker (see Prerequisites section for commands)
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version
docker compose version
```

### Step 3: Deploy Application

#### 3.1 Clone Repository

```bash
# Create application directory
sudo mkdir -p /opt/meal-planning-system
sudo chown $USER:$USER /opt/meal-planning-system

# Clone repository
cd /opt/meal-planning-system
git clone <repository-url> .
```

#### 3.2 Configure Environment

```bash
# Navigate to infrastructure directory
cd /opt/meal-planning-system/infrastructure

# Copy example environment file
cp .env.example .env

# Generate secret key
openssl rand -hex 32

# Edit environment file
nano .env
```

**Important:** The `.env` file must be in the `infrastructure/` directory where `docker-compose.yml` is located.

**Production environment:**

```bash
# Database
DATABASE_URL=postgresql://meal_planner:STRONG_PASSWORD_HERE@postgres:5432/household_db

# Authentication
SECRET_KEY=<generated-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS - Use your server's IP or domain
BACKEND_CORS_ORIGINS=https://192.168.1.100,https://meal-planner.local

# Application
APP_NAME=Household Meal Planning
DEBUG=False  # IMPORTANT: Set to False in production

# Scraper
SCRAPER_RATE_LIMIT_SECONDS=5
```

#### 3.3 Build and Start Services

```bash
# Build Docker images
docker compose -f docker-compose.yml build

# Start services in detached mode
docker compose up -d

# Check service status
docker compose ps
```

### Step 4: Initialize Database

```bash
# Initialize database schema
docker compose exec backend python scripts/init_db.py

# Or run SQL files manually
docker compose exec postgres psql -U meal_planner -d household_db < database/schemas/01_shared_schema.sql
docker compose exec postgres psql -U meal_planner -d household_db < database/schemas/02_meal_planning_schema.sql
docker compose exec postgres psql -U meal_planner -d household_db < database/seed_data.sql
```

### Step 5: Create Admin User

```bash
docker compose exec backend python scripts/create_admin.py

# Enter admin username (e.g., admin)
# Enter admin email (e.g., admin@localhost)
# Enter strong password (min 8 chars)
```

### Step 6: Set Up Nginx Reverse Proxy

#### 6.1 Install Nginx

```bash
sudo apt install -y nginx
```

#### 6.2 Configure Nginx

```bash
# Copy nginx configuration
sudo cp infrastructure/nginx.conf /etc/nginx/sites-available/meal-planning

# Create symbolic link
sudo ln -s /etc/nginx/sites-available/meal-planning /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

**Nginx Configuration (`infrastructure/nginx.conf`):**

```nginx
upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name 192.168.1.100;  # Replace with your IP

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name 192.168.1.100;  # Replace with your IP

    # SSL certificates
    ssl_certificate /etc/ssl/certs/meal-planning.crt;
    ssl_certificate_key /etc/ssl/private/meal-planning.key;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Backend API
    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 7: Generate SSL Certificate

#### Option A: Self-Signed Certificate (Local Network)

```bash
# Use provided script
cd /opt/meal-planning-system/infrastructure
chmod +x generate-ssl.sh
sudo ./generate-ssl.sh

# Or manually
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/meal-planning.key \
  -out /etc/ssl/certs/meal-planning.crt

# Set permissions
sudo chmod 600 /etc/ssl/private/meal-planning.key
```

**Note:** Browsers will show a security warning for self-signed certificates. This is normal for local deployments.

#### Option B: Let's Encrypt (If Publicly Accessible)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d meal-planner.yourdomain.com

# Certbot will automatically configure Nginx
```

### Step 8: Configure Systemd Service

Create service file for auto-start:

```bash
sudo nano /etc/systemd/system/meal-planning.service
```

```ini
[Unit]
Description=Meal Planning Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/meal-planning-system
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
# Enable service
sudo systemctl enable meal-planning.service

# Start service
sudo systemctl start meal-planning.service

# Check status
sudo systemctl status meal-planning.service
```

### Step 9: Set Up Automated Backups

```bash
# Create backup script
sudo nano /opt/meal-planning-system/scripts/backup.sh
```

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/meal-planning"
DATE=$(date +%Y%m%d_%H%M%S)
KEEP_DAYS=30

mkdir -p $BACKUP_DIR

# Backup database
docker exec meal-planning-db pg_dump -U meal_planner household_db | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Backup application files
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz /opt/meal-planning-system/.env

# Delete old backups
find $BACKUP_DIR -name "*.gz" -mtime +$KEEP_DAYS -delete

echo "Backup completed: $DATE"
```

```bash
# Make script executable
chmod +x /opt/meal-planning-system/scripts/backup.sh

# Add to crontab
crontab -e

# Add line (daily backup at 2 AM):
0 2 * * * /opt/meal-planning-system/scripts/backup.sh >> /var/log/meal-planning-backup.log 2>&1
```

### Step 10: Verify Deployment

```bash
# Check all services are running
docker compose ps

# Test backend health
curl -k https://localhost/api/health

# Test frontend
curl -k https://localhost

# Check logs
docker compose logs -f
```

**Access the application:**

- Navigate to: `https://<your-server-ip>`
- Accept the self-signed certificate warning (if applicable)
- Log in with admin credentials

---

## Cloud Deployment Options

### AWS Deployment

#### Architecture

- **EC2 Instance**: Application host (t3.medium)
- **RDS PostgreSQL**: Managed database
- **S3**: Backups
- **CloudWatch**: Monitoring and logs

#### Steps

1. **Launch EC2 Instance:**
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t3.medium (2 vCPU, 4 GB RAM)
   - Storage: 50 GB gp3
   - Security Group: Allow 22, 80, 443

2. **Set Up RDS Database:**
   - Engine: PostgreSQL 15
   - Instance: db.t3.micro
   - Storage: 20 GB
   - Enable automated backups

3. **Deploy Application:**
   ```bash
   # SSH to EC2 instance
   ssh -i key.pem ubuntu@<ec2-ip>

   # Follow production deployment steps
   # Update DATABASE_URL to RDS endpoint
   DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/household_db
   ```

4. **Configure Load Balancer (Optional):**
   - Application Load Balancer
   - Target: EC2 instance on port 443
   - SSL certificate from ACM

5. **Set Up S3 Backups:**
   ```bash
   # Install AWS CLI
   sudo apt install -y awscli

   # Configure AWS credentials
   aws configure

   # Modify backup script to upload to S3
   aws s3 cp $BACKUP_DIR/db_backup_$DATE.sql.gz s3://meal-planning-backups/
   ```

### DigitalOcean Deployment

#### Architecture

- **Droplet**: Application host (2 GB RAM, 2 vCPU)
- **Managed Database**: PostgreSQL cluster
- **Spaces**: Backups (S3-compatible)

#### Steps

1. **Create Droplet:**
   - OS: Ubuntu 22.04 LTS
   - Plan: Basic ($12/month)
   - Enable monitoring

2. **Create Managed Database:**
   - Engine: PostgreSQL 15
   - Plan: $15/month
   - Enable automated backups

3. **Deploy Application:**
   ```bash
   # SSH to Droplet
   ssh root@<droplet-ip>

   # Follow production deployment steps
   # Update DATABASE_URL to managed database
   DATABASE_URL=postgresql://user:pass@managed-db-host:25060/household_db?sslmode=require
   ```

4. **Configure Firewall:**
   ```bash
   # DigitalOcean Cloud Firewall
   # Inbound: 22 (SSH), 80 (HTTP), 443 (HTTPS)
   # Outbound: All
   ```

5. **Set Up Spaces for Backups:**
   ```bash
   # Install s3cmd
   sudo apt install -y s3cmd

   # Configure for Spaces
   s3cmd --configure

   # Upload backups
   s3cmd put $BACKUP_DIR/db_backup_$DATE.sql.gz s3://meal-planning-backups/
   ```

---

## Docker Deployment

### Docker Compose Configuration

**File: `docker-compose.yml`**

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: meal-planning-db
    environment:
      POSTGRES_USER: meal_planner
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: household_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/schemas:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U meal_planner"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: meal-planning-backend
    environment:
      DATABASE_URL: ${DATABASE_URL}
      SECRET_KEY: ${SECRET_KEY}
      ALGORITHM: ${ALGORITHM}
      ACCESS_TOKEN_EXPIRE_MINUTES: ${ACCESS_TOKEN_EXPIRE_MINUTES}
      BACKEND_CORS_ORIGINS: ${BACKEND_CORS_ORIGINS}
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: meal-planning-frontend
    environment:
      NEXT_PUBLIC_API_URL: ${NEXT_PUBLIC_API_URL}
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    ports:
      - "3000:3000"
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    container_name: meal-planning-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infrastructure/nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/ssl/certs/meal-planning.crt:/etc/ssl/certs/meal-planning.crt:ro
      - /etc/ssl/private/meal-planning.key:/etc/ssl/private/meal-planning.key:ro
    depends_on:
      - backend
      - frontend

volumes:
  postgres_data:
```

### Backend Dockerfile

**File: `backend/Dockerfile`**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

**File: `frontend/Dockerfile`**

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Build application
RUN npm run build

# Expose port
EXPOSE 3000

# Run application
CMD ["npm", "start"]
```

---

## Database Migration

### Initial Schema Setup

```bash
# Run schema files
docker compose exec postgres psql -U meal_planner -d household_db < database/schemas/01_shared_schema.sql
docker compose exec postgres psql -U meal_planner -d household_db < database/schemas/02_meal_planning_schema.sql
```

### Schema Changes (Alembic)

If using Alembic for migrations:

```bash
# Initialize Alembic (first time)
cd backend
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new column"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Data Migration

```bash
# Export data from old system
pg_dump -U old_user old_db > old_data.sql

# Transform data (if needed)
# Edit old_data.sql to match new schema

# Import to new system
docker compose exec -T postgres psql -U meal_planner -d household_db < old_data.sql
```

---

## Continuous Deployment

### GitHub Actions CI/CD

**File: `.github/workflows/deploy.yml`**

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /opt/meal-planning-system
          git pull origin main
          docker compose down
          docker compose up -d --build
          docker compose exec backend python scripts/migrate.py
```

### Automated Deployment Script

```bash
#!/bin/bash

# deploy.sh

echo "Pulling latest code..."
git pull origin main

echo "Building Docker images..."
docker compose build

echo "Stopping services..."
docker compose down

echo "Starting services..."
docker compose up -d

echo "Running migrations..."
docker compose exec backend python scripts/migrate.py

echo "Deployment complete!"
```

---

## Post-Deployment

### Health Checks

```bash
# Backend health
curl -k https://your-server/api/health

# Database connection
docker compose exec postgres pg_isready -U meal_planner

# All services
docker compose ps
```

### Verification Checklist

- [ ] All Docker containers are running
- [ ] Database is accessible and initialized
- [ ] Backend API responds at /api/health
- [ ] Frontend loads in browser
- [ ] Can log in with admin account
- [ ] Can create a recipe
- [ ] Can add inventory item
- [ ] Can create menu plan
- [ ] HTTPS is working (if configured)
- [ ] Backups are configured and running
- [ ] Logs are being written
- [ ] Firewall rules are correct

### Performance Testing

```bash
# Test API response time
time curl -k https://your-server/api/health

# Load testing (if ab is installed)
ab -n 1000 -c 10 https://your-server/api/recipes
```

### Monitoring Setup

```bash
# View logs in real-time
docker compose logs -f

# Check resource usage
docker stats

# Check disk space
df -h
```

---

## Troubleshooting Deployment

### Services Won't Start

```bash
# Check logs
docker compose logs

# Check specific service
docker compose logs backend

# Rebuild containers
docker compose down
docker compose up -d --build
```

### Database Connection Errors

```bash
# Test database connection
docker compose exec postgres psql -U meal_planner -d household_db -c "SELECT 1;"

# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL

# Verify postgres container is running
docker compose ps postgres
```

### Port Conflicts

```bash
# Check what's using ports
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :5432

# Change ports in docker-compose.yml if needed
```

### SSL Certificate Issues

```bash
# Regenerate certificate
sudo ./infrastructure/generate-ssl.sh

# Check certificate
sudo openssl x509 -in /etc/ssl/certs/meal-planning.crt -noout -text

# Test Nginx configuration
sudo nginx -t
```

### Permission Issues

```bash
# Fix file permissions
sudo chown -R $USER:$USER /opt/meal-planning-system

# Fix Docker socket permissions
sudo chmod 666 /var/run/docker.sock
```

---

## Additional Resources

**Related Documentation:**
- [Admin Guide](ADMIN_GUIDE.md) - System administration
- [User Guide](USER_GUIDE.md) - End-user documentation
- [Developer Guide](DEVELOPER_GUIDE.md) - Development setup
- [Proxmox Setup](../infrastructure/proxmox-setup.md) - Detailed VM creation

**External Resources:**
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

**Support:**
- GitHub Issues: Report deployment issues
- Documentation: Check guides for information

---

**Document Version:** 1.0
**Last Updated:** October 1, 2025
**Application Version:** 1.0.0

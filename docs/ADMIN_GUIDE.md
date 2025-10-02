# Administrator Guide

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Initial Setup](#initial-setup)
4. [User Management](#user-management)
5. [System Configuration](#system-configuration)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)
7. [Data Management](#data-management)
8. [Notification Management](#notification-management)
9. [Troubleshooting](#troubleshooting)
10. [Security](#security)
11. [Backup and Recovery](#backup-and-recovery)
12. [Performance Optimization](#performance-optimization)

---

## Introduction

### Purpose

This guide is for system administrators responsible for installing, configuring, maintaining, and troubleshooting the Household Meal Planning System.

### Target Audience

- System administrators
- IT staff managing the deployment
- Technical users responsible for system maintenance

### Scope

This guide covers:
- System installation and configuration
- User and permission management
- Routine maintenance tasks
- Troubleshooting common issues
- Backup and recovery procedures
- Performance optimization

For deployment instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).
For end-user documentation, see [USER_GUIDE.md](USER_GUIDE.md).

---

## System Requirements

### Hardware Requirements

**Minimum Requirements:**
- CPU: 2 cores
- RAM: 4 GB
- Storage: 20 GB
- Network: 100 Mbps Ethernet

**Recommended for Production:**
- CPU: 4 cores
- RAM: 8 GB
- Storage: 50 GB SSD
- Network: 1 Gbps Ethernet

**Storage Planning:**
- Database: 2-5 GB (for typical household use)
- Application files: 2 GB
- Logs: 1-2 GB
- Docker images: 5-10 GB
- Reserve: 20-30 GB for growth

### Software Requirements

**Operating System:**
- Ubuntu Server 22.04 LTS (recommended)
- Debian 11+
- CentOS 8+
- RHEL 8+

**Required Software:**
- Docker 24+
- Docker Compose 2.20+
- PostgreSQL 15+ (via Docker or standalone)

**Optional Software:**
- Nginx (reverse proxy)
- Certbot (SSL certificates)
- Backup tools (rsync, duplicity, etc.)

### Network Requirements

- Static IP address (recommended)
- Access to local network
- No external internet exposure (for security)
- Ports needed:
  - 80 (HTTP, optional)
  - 443 (HTTPS)
  - 5432 (PostgreSQL, if external access needed)
  - 8000 (Backend, internal)
  - 3000 (Frontend, internal)

---

## Initial Setup

### Installation Overview

The installation process consists of:

1. **Server Preparation**: OS installation, network configuration
2. **Docker Installation**: Install Docker and Docker Compose
3. **Application Deployment**: Clone repository, configure environment
4. **Database Initialization**: Create schemas, seed data
5. **Admin User Creation**: Create first admin account
6. **Service Configuration**: Set up systemd services, reverse proxy
7. **SSL/TLS Setup**: Generate certificates for HTTPS
8. **Verification**: Test all components

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed step-by-step instructions.

### Post-Installation Checklist

After installation, verify:

- [ ] Server is accessible on network
- [ ] Docker services are running
- [ ] Database is accessible
- [ ] Backend API is responding (`/api/health`)
- [ ] Frontend is loading
- [ ] Admin user can log in
- [ ] SSL/HTTPS is working (if configured)
- [ ] Firewall rules are correct
- [ ] Backups are configured
- [ ] Logs are being written

### Creating the First Admin User

**Method 1: Using Database Script**

```bash
cd /opt/meal-planning-system/backend
python scripts/create_admin.py
```

Follow the prompts to enter:
- Username (e.g., `admin`)
- Email (e.g., `admin@localhost`)
- Password (minimum 8 characters)

**Method 2: Manual SQL**

```bash
# Connect to database
docker exec -it meal-planning-db psql -U meal_planner -d household_db
```

```sql
-- Generate password hash for "admin123" (example)
-- Use a password hashing tool or bcrypt library

INSERT INTO shared.users (id, username, email, password_hash, role, is_active)
VALUES (
  gen_random_uuid(),
  'admin',
  'admin@localhost',
  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzJGOEL8bW',
  'admin',
  true
);
```

**Important:** Change the default password immediately after first login.

---

## User Management

### Accessing User Management

1. Log in as admin user
2. Navigate to **Admin** → **Users**
3. View list of all users

### Creating Users

**Via Admin UI:**

1. Go to **Admin** → **Users** → **Create User**
2. Fill in the form:
   - **Username**: 3-50 characters, unique
   - **Email**: Valid email address, unique
   - **Password**: Minimum 8 characters
   - **Role**: Select role (admin, user, child)
   - **Active**: Check to activate immediately
3. Click **Create User**
4. Provide credentials to the user

**Via API:**

```bash
curl -X POST http://localhost:8000/api/admin/users \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "new_user",
    "email": "user@example.com",
    "password": "SecurePassword123",
    "role": "user",
    "is_active": true
  }'
```

**Via Database:**

```sql
INSERT INTO shared.users (id, username, email, password_hash, role, is_active)
VALUES (
  gen_random_uuid(),
  'new_user',
  'user@example.com',
  '<bcrypt-hashed-password>',
  'user',
  true
);
```

### User Roles

The system has three user roles:

#### Admin Role

**Permissions:**
- Full access to all features
- User management (create, edit, delete users)
- System settings configuration
- View system statistics
- Generate notifications manually
- Access admin dashboard

**Use Cases:**
- System administrators
- Household managers
- Technical staff

#### User Role

**Permissions:**
- Create and manage recipes
- Manage inventory
- Plan menus
- Generate shopping lists
- Rate recipes
- View notifications
- Access all user features

**Restrictions:**
- Cannot create/manage other users
- Cannot change system settings
- Cannot view system statistics
- Cannot access admin dashboard

**Use Cases:**
- Family members
- Regular household users

#### Child Role (Future Feature)

**Planned Permissions:**
- View recipes and menus
- View shopping lists
- Limited or no editing permissions

### Editing Users

**Change User Role:**

1. Find user in **Admin** → **Users**
2. Click **Edit**
3. Select new role from dropdown
4. Click **Save**

**Activate/Deactivate User:**

1. Find user in user list
2. Click **Edit**
3. Check or uncheck **Active** status
4. Click **Save**

**Deactivation Effects:**
- User cannot log in
- Existing sessions are invalidated
- User data is preserved
- Can be reactivated at any time

**Change User Email:**

1. Edit user
2. Update email field
3. Ensure email is unique
4. Save

### Resetting User Passwords

**Admin Reset (Recommended):**

1. Go to **Admin** → **Users**
2. Find the user
3. Click **Reset Password**
4. Enter new password (or generate random)
5. Click **Save**
6. Provide new password to user securely

**Database Reset:**

```sql
-- Update password for user
UPDATE shared.users
SET password_hash = '<new-bcrypt-hash>'
WHERE username = 'username';
```

**Self-Service Reset:**

Currently, users must contact an admin to reset passwords. Email-based password reset is a planned future feature.

### Deleting Users

**Soft Delete (Recommended):**

1. Deactivate the user instead of deleting
2. User cannot log in but data is preserved
3. Can be reactivated if needed

**Hard Delete (Not Recommended):**

Only delete users if absolutely necessary, as this may affect:
- Recipe ownership
- Rating history
- Activity logs

To delete via database:

```sql
-- This will cascade to related records
DELETE FROM shared.users WHERE id = '<user-id>';
```

**Better Approach:** Deactivate users rather than deleting them.

### Viewing User Activity

**Via Admin Dashboard:**

1. Go to **Admin** → **Dashboard**
2. View **Recent Activity** section
3. See user actions, timestamps

**Via Database:**

```sql
-- View recent user activity
SELECT u.username, a.action, a.entity_type, a.timestamp
FROM shared.user_activity_log a
JOIN shared.users u ON a.user_id = u.id
ORDER BY a.timestamp DESC
LIMIT 50;
```

---

## System Configuration

### Accessing System Settings

1. Log in as admin
2. Go to **Admin** → **Settings**
3. View and edit configuration

### Configuration Options

#### Favorites Configuration

**Favorites Threshold Percentage**

- **Description**: Minimum percentage of positive ratings for a recipe to be marked as a favorite
- **Default**: 75%
- **Range**: 50-100%
- **Example**: 75% means at least 3 out of 4 ratings must be thumbs up

**When to Adjust:**
- Lower for small households (e.g., 60%)
- Raise for larger households wanting stricter criteria (e.g., 80-90%)

**Favorites Minimum Raters**

- **Description**: Minimum number of users who must rate a recipe before it can be a favorite
- **Default**: 2
- **Range**: 1-10
- **Example**: 2 means at least 2 people must rate the recipe

**When to Adjust:**
- Lower to 1 for small households
- Raise to 3-5 for larger households

#### Inventory Configuration

**Low Stock Threshold Days**

- **Description**: Number of days of stock that triggers a low stock alert
- **Default**: 3 days
- **Range**: 1-30 days
- **Note**: This is a system-wide default; individual items can override with their own thresholds

**When to Adjust:**
- Lower for frequent shoppers (1-2 days)
- Raise for infrequent shoppers (5-7 days)

**Expiration Warning Days**

- **Description**: How many days before expiration to generate a warning notification
- **Default**: 7 days
- **Range**: 1-30 days

**When to Adjust:**
- Lower for users who shop frequently (3-5 days)
- Raise for advance planning (10-14 days)

#### Recipe Scraper Configuration

**Scraper Rate Limit Seconds**

- **Description**: Minimum seconds to wait between scrape requests to the same domain
- **Default**: 5 seconds
- **Range**: 1-60 seconds
- **Purpose**: Prevents overloading recipe websites, respects robots.txt

**When to Adjust:**
- Don't lower below 5 seconds (be a good web citizen)
- Raise if experiencing issues with specific sites

### Updating Settings

**Via Admin UI:**

1. Go to **Admin** → **Settings**
2. Modify values
3. Click **Save Settings**
4. Changes take effect immediately

**Via API:**

```bash
curl -X PUT http://localhost:8000/api/admin/settings \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "favorites_threshold_percentage": 80,
    "favorites_min_raters": 3,
    "expiration_warning_days": 5
  }'
```

**Via Database:**

```sql
-- Update settings in meal_planning.admin_settings
UPDATE meal_planning.admin_settings
SET favorites_threshold_percentage = 80,
    favorites_min_raters = 3,
    expiration_warning_days = 5
WHERE id = 1;
```

### Environment Variables

Key environment variables in `.env` file:

**Database:**
```bash
DATABASE_URL=postgresql://meal_planner:password@localhost:5432/household_db
```

**Authentication:**
```bash
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
```

**CORS:**
```bash
BACKEND_CORS_ORIGINS=http://localhost:3000,http://192.168.1.100:3000
```

**Application:**
```bash
APP_NAME=Household Meal Planning
APP_VERSION=1.0.0
DEBUG=False  # Set to True for development
```

**After changing environment variables:**

```bash
# Restart services
docker-compose down
docker-compose up -d
```

---

## Monitoring and Maintenance

### Health Checks

**Backend Health Check:**

```bash
curl http://localhost:8000/api/health

# Expected response:
{"status":"healthy"}
```

**Database Health Check:**

```bash
docker exec meal-planning-db pg_isready -U meal_planner

# Expected output:
/var/run/postgresql:5432 - accepting connections
```

**Frontend Health Check:**

```bash
curl http://localhost:3000

# Should return HTML of the login page
```

**Docker Services Status:**

```bash
docker-compose ps

# All services should show "Up"
```

### Viewing System Statistics

**Via Admin Dashboard:**

1. Go to **Admin** → **Dashboard** or **Statistics**
2. View metrics:
   - Total users (active/inactive)
   - Total recipes
   - Most cooked recipes
   - Most favorited recipes
   - Inventory statistics
   - Menu plan statistics

**Via API:**

```bash
curl http://localhost:8000/api/admin/statistics \
  -H "Authorization: Bearer <admin-token>"
```

**Via Database:**

```sql
-- User statistics
SELECT
  COUNT(*) as total_users,
  COUNT(*) FILTER (WHERE is_active = true) as active_users,
  COUNT(*) FILTER (WHERE role = 'admin') as admin_users
FROM shared.users;

-- Recipe statistics
SELECT
  COUNT(*) as total_recipes,
  COUNT(*) FILTER (WHERE is_deleted = false) as active_recipes
FROM meal_planning.recipes;

-- Most cooked recipes
SELECT r.title, r.times_cooked
FROM meal_planning.recipes r
WHERE r.is_deleted = false
ORDER BY r.times_cooked DESC
LIMIT 10;
```

### Log Management

**Log Locations:**

- Backend logs: `/var/log/meal-planning/backend.log` or Docker logs
- Frontend logs: Docker logs
- Database logs: `/var/log/postgresql/` or Docker logs
- Nginx logs: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`

**Viewing Logs:**

```bash
# Backend logs
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend

# All services
docker-compose logs --tail=50 -f

# Database logs
docker-compose logs postgres

# Nginx logs (if using Docker)
docker-compose logs nginx
```

**Log Rotation:**

Configure log rotation to prevent disk space issues:

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/meal-planning
```

```
/var/log/meal-planning/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
}
```

**Docker Logs Cleanup:**

```bash
# Clear all Docker logs
truncate -s 0 /var/lib/docker/containers/*/*-json.log

# Or configure Docker daemon to limit log size
# Edit /etc/docker/daemon.json:
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### Performance Monitoring

**Database Performance:**

```sql
-- Active connections
SELECT count(*) FROM pg_stat_activity;

-- Slow queries
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 seconds'
  AND state = 'active';

-- Database size
SELECT pg_size_pretty(pg_database_size('household_db'));

-- Table sizes
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname IN ('shared', 'meal_planning')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

**System Resource Usage:**

```bash
# CPU and memory usage
docker stats

# Disk usage
df -h

# Disk usage by directory
du -sh /var/lib/docker /opt/meal-planning-system

# Check for disk issues
docker system df
```

**API Performance:**

Monitor API response times through:
- Application logs
- Nginx access logs
- Application Performance Monitoring (APM) tools (if configured)

### Routine Maintenance Tasks

**Daily:**
- [ ] Check service health
- [ ] Review error logs
- [ ] Monitor disk space

**Weekly:**
- [ ] Review user activity
- [ ] Check backup status
- [ ] Review system statistics
- [ ] Clean up old logs (if not auto-rotated)

**Monthly:**
- [ ] Database maintenance (VACUUM, ANALYZE)
- [ ] Review and update system settings
- [ ] Test backup restoration
- [ ] Update software packages
- [ ] Review SSL certificate expiration

**Quarterly:**
- [ ] Performance optimization
- [ ] Security audit
- [ ] Capacity planning
- [ ] Review and update documentation

---

## Data Management

### Database Backups

**Manual Backup:**

```bash
# Full database backup
docker exec meal-planning-db pg_dump -U meal_planner household_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Compressed backup
docker exec meal-planning-db pg_dump -U meal_planner household_db | gzip > backup_$(date +%Y%m%d).sql.gz

# Specific schema backup
docker exec meal-planning-db pg_dump -U meal_planner -n meal_planning household_db > meal_planning_backup.sql
```

**Automated Backup Script:**

Create `/opt/meal-planning-system/scripts/backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/meal-planning"
DATE=$(date +%Y%m%d_%H%M%S)
KEEP_DAYS=30

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
docker exec meal-planning-db pg_dump -U meal_planner household_db | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Backup application files
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz /opt/meal-planning-system/.env

# Delete old backups
find $BACKUP_DIR -name "*.gz" -mtime +$KEEP_DAYS -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +$KEEP_DAYS -delete

echo "Backup completed: $DATE"
```

**Schedule with cron:**

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /opt/meal-planning-system/scripts/backup.sh >> /var/log/meal-planning-backup.log 2>&1
```

### Restoring from Backup

**Restore Database:**

```bash
# Stop application
docker-compose down

# Restore from SQL file
gunzip < backup_20251001.sql.gz | docker exec -i meal-planning-db psql -U meal_planner household_db

# Or from uncompressed file
docker exec -i meal-planning-db psql -U meal_planner household_db < backup.sql

# Restart application
docker-compose up -d
```

**Restore Application Files:**

```bash
# Extract backup
tar -xzf app_backup_20251001.tar.gz -C /
```

### Database Maintenance

**VACUUM and ANALYZE:**

```bash
# Connect to database
docker exec -it meal-planning-db psql -U meal_planner household_db
```

```sql
-- Vacuum and analyze all tables
VACUUM ANALYZE;

-- Vacuum specific table
VACUUM ANALYZE meal_planning.recipes;

-- Full vacuum (requires exclusive lock, run during maintenance window)
VACUUM FULL;
```

**Schedule regular maintenance:**

```bash
# Add to crontab
# Run VACUUM ANALYZE weekly on Sunday at 3 AM
0 3 * * 0 docker exec meal-planning-db psql -U meal_planner -d household_db -c "VACUUM ANALYZE;" >> /var/log/meal-planning-vacuum.log 2>&1
```

### Bulk Data Import

**Import Recipes (CSV):**

Create script to import recipes from CSV file:

```python
# scripts/import_recipes.py
import csv
import requests

API_URL = "http://localhost:8000/api"
TOKEN = "admin-token-here"

with open('recipes.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        recipe_data = {
            "title": row['title'],
            "description": row['description'],
            "servings": int(row['servings']),
            "prep_time_minutes": int(row['prep_time']),
            "cook_time_minutes": int(row['cook_time']),
            "difficulty": row['difficulty'],
            "ingredients": [],  # Parse from CSV
            "instructions": [],  # Parse from CSV
            "tags": row['tags'].split(',')
        }

        response = requests.post(
            f"{API_URL}/recipes",
            json=recipe_data,
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        print(f"Imported: {row['title']}")
```

**Export Data:**

```bash
# Export all recipes to CSV
docker exec meal-planning-db psql -U meal_planner -d household_db \
  -c "COPY (SELECT * FROM meal_planning.recipes WHERE is_deleted = false) TO STDOUT WITH CSV HEADER" \
  > recipes_export.csv

# Export inventory
docker exec meal-planning-db psql -U meal_planner -d household_db \
  -c "COPY (SELECT * FROM meal_planning.inventory) TO STDOUT WITH CSV HEADER" \
  > inventory_export.csv
```

### Data Cleanup

**Delete Old Notifications:**

```sql
-- Delete notifications older than 90 days
DELETE FROM shared.notifications
WHERE created_at < NOW() - INTERVAL '90 days';
```

**Delete Old Activity Logs:**

```sql
-- Delete activity logs older than 1 year
DELETE FROM shared.user_activity_log
WHERE timestamp < NOW() - INTERVAL '1 year';
```

**Clean Up Deleted Recipes:**

```sql
-- Permanently delete recipes marked as deleted more than 30 days ago
DELETE FROM meal_planning.recipes
WHERE is_deleted = true
  AND updated_at < NOW() - INTERVAL '30 days';
```

**Schedule cleanup:**

```bash
# Monthly cleanup on first of month at 4 AM
0 4 1 * * docker exec meal-planning-db psql -U meal_planner -d household_db -f /path/to/cleanup.sql >> /var/log/meal-planning-cleanup.log 2>&1
```

---

## Notification Management

### Generating Notifications Manually

**Via Admin UI:**

1. Go to **Admin** → **Notifications**
2. Click **Generate Notifications**
3. Select type:
   - Low Stock Alerts
   - Expiring Item Alerts
   - Meal Reminders
4. Click **Generate**

**Via API:**

```bash
# Generate low stock notifications
curl -X POST http://localhost:8000/api/admin/notifications/generate/low-stock \
  -H "Authorization: Bearer <admin-token>"

# Generate expiring item notifications
curl -X POST http://localhost:8000/api/admin/notifications/generate/expiring \
  -H "Authorization: Bearer <admin-token>"

# Generate meal reminders
curl -X POST http://localhost:8000/api/admin/notifications/generate/meal-reminders \
  -H "Authorization: Bearer <admin-token>"
```

### Automated Notification Generation

**Set up cron jobs:**

```bash
# Edit crontab
crontab -e

# Generate low stock notifications daily at 8 AM
0 8 * * * curl -X POST http://localhost:8000/api/admin/notifications/generate/low-stock -H "Authorization: Bearer <token>" >> /var/log/meal-planning-notifications.log 2>&1

# Generate expiring item notifications daily at 8 AM
5 8 * * * curl -X POST http://localhost:8000/api/admin/notifications/generate/expiring -H "Authorization: Bearer <token>" >> /var/log/meal-planning-notifications.log 2>&1

# Generate meal reminders daily at 7 AM
0 7 * * * curl -X POST http://localhost:8000/api/admin/notifications/generate/meal-reminders -H "Authorization: Bearer <token>" >> /var/log/meal-planning-notifications.log 2>&1
```

### Cleaning Up Notifications

```sql
-- Delete read notifications older than 30 days
DELETE FROM shared.notifications
WHERE is_read = true
  AND created_at < NOW() - INTERVAL '30 days';

-- Delete all notifications for a specific user
DELETE FROM shared.notifications
WHERE user_id = '<user-id>';
```

---

## Troubleshooting

### Common Issues

#### Application Won't Start

**Symptom:** Docker containers fail to start

**Check:**

```bash
# View service status
docker-compose ps

# Check logs
docker-compose logs

# Check specific service
docker-compose logs backend
```

**Common Causes:**

1. **Port conflicts**: Another service using ports 80, 443, 8000, 3000, or 5432
   ```bash
   # Check what's using a port
   sudo netstat -tulpn | grep :8000
   ```

2. **Environment variables not set**: Missing or incorrect `.env` file
   ```bash
   # Verify .env file exists
   cat .env
   ```

3. **Database connection failure**: DATABASE_URL incorrect
   ```bash
   # Test database connection
   docker exec meal-planning-db psql -U meal_planner -d household_db -c "SELECT 1;"
   ```

**Solutions:**

```bash
# Stop all services
docker-compose down

# Remove old containers
docker-compose rm -f

# Rebuild and start
docker-compose up -d --build
```

#### Database Connection Errors

**Symptom:** Backend cannot connect to database

**Check:**

```bash
# Is database running?
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Test connection
docker exec meal-planning-db psql -U meal_planner -d household_db
```

**Solutions:**

1. Verify DATABASE_URL in `.env`
2. Ensure database container is running
3. Check network connectivity
4. Verify credentials

#### Authentication Not Working

**Symptom:** Users cannot log in, or sessions expire immediately

**Check:**

1. SECRET_KEY is set in `.env`
2. Token expiration settings
3. Clock synchronization (JWT tokens are time-sensitive)

**Solutions:**

```bash
# Check system time
date

# Sync time
sudo ntpdate pool.ntp.org

# Verify SECRET_KEY
grep SECRET_KEY .env
```

#### Recipe Scraper Failing

**Symptom:** Cannot scrape recipes from websites

**Common Causes:**

1. Website not supported
2. Rate limit exceeded
3. Network connectivity issues
4. Website blocking automated access

**Solutions:**

1. Use supported websites
2. Wait 5+ seconds between scrapes
3. Check internet connectivity
4. Manually enter recipe if scraping fails

#### Performance Issues

**Symptom:** Slow response times, high latency

**Check:**

```bash
# System resources
docker stats

# Database performance
docker exec meal-planning-db psql -U meal_planner -d household_db -c "SELECT * FROM pg_stat_activity;"

# Disk space
df -h
```

**Solutions:**

1. **Increase resources**: Allocate more RAM/CPU to Docker
2. **Database optimization**: Run VACUUM ANALYZE
3. **Clear logs**: Rotate and compress old logs
4. **Restart services**: `docker-compose restart`

### Diagnostic Commands

**Test Backend API:**

```bash
# Health check
curl http://localhost:8000/api/health

# Get API docs
curl http://localhost:8000/docs
```

**Test Database:**

```bash
# Connect to database
docker exec -it meal-planning-db psql -U meal_planner household_db

# Check tables
\dt shared.*
\dt meal_planning.*

# Check connections
SELECT count(*) FROM pg_stat_activity;
```

**Test Frontend:**

```bash
# Check if frontend is serving
curl http://localhost:3000

# Check frontend logs
docker-compose logs frontend
```

**Check Docker:**

```bash
# List containers
docker ps -a

# View resource usage
docker stats

# Check networks
docker network ls

# Inspect container
docker inspect meal-planning-backend
```

---

## Security

### Security Best Practices

**System Security:**

1. **Keep software updated**
   ```bash
   # Update system packages
   sudo apt update && sudo apt upgrade

   # Update Docker images
   docker-compose pull
   docker-compose up -d
   ```

2. **Use strong passwords**
   - Minimum 12 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - Use password manager

3. **Limit access**
   - Only allow local network access
   - No external internet exposure
   - Use firewall rules

4. **Regular backups**
   - Daily automated backups
   - Test restoration quarterly
   - Store backups securely

### Firewall Configuration

**Using UFW (Ubuntu):**

```bash
# Enable firewall
sudo ufw enable

# Allow SSH (if needed)
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS from local network only
sudo ufw allow from 192.168.1.0/24 to any port 80
sudo ufw allow from 192.168.1.0/24 to any port 443

# Deny external access
sudo ufw deny from any to any port 80
sudo ufw deny from any to any port 443

# Check status
sudo ufw status verbose
```

### SSL/TLS Configuration

**Generate Self-Signed Certificate:**

```bash
# Use provided script
cd /opt/meal-planning-system/infrastructure
./generate-ssl.sh
```

**Or manually:**

```bash
# Generate certificate
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/meal-planning.key \
  -out /etc/ssl/certs/meal-planning.crt

# Set permissions
sudo chmod 600 /etc/ssl/private/meal-planning.key
```

**Configure Nginx:**

See `infrastructure/nginx.conf` for SSL configuration example.

### Security Auditing

**Check for Vulnerabilities:**

```bash
# Scan Python dependencies
cd backend
pip install safety
safety check

# Scan Node dependencies
cd frontend
npm audit

# Update vulnerable packages
npm audit fix
```

**Review Logs:**

```bash
# Check for failed login attempts
docker-compose logs backend | grep "401"

# Check for suspicious activity
docker-compose logs backend | grep -E "(DELETE|admin)"
```

---

## Backup and Recovery

### Backup Strategy

**3-2-1 Backup Rule:**

- **3** copies of data
- **2** different media types
- **1** off-site backup

**Backup Types:**

1. **Daily Incremental**: Changed data only
2. **Weekly Full**: Complete system backup
3. **Monthly Archive**: Long-term storage

### Backup Script

See [Data Management](#database-backups) section for backup scripts.

### Disaster Recovery Plan

**Scenario 1: Database Corruption**

1. Stop application
2. Restore from most recent backup
3. Verify data integrity
4. Restart application
5. Test functionality

**Scenario 2: Complete System Failure**

1. Provision new server
2. Install Docker and dependencies
3. Restore application files
4. Restore database
5. Restart services
6. Verify functionality

**Recovery Time Objective (RTO):** 2-4 hours
**Recovery Point Objective (RPO):** 24 hours (daily backups)

---

## Performance Optimization

### Database Optimization

**Indexes:**

```sql
-- Add indexes for frequently queried columns
CREATE INDEX IF NOT EXISTS idx_recipes_title ON meal_planning.recipes(title);
CREATE INDEX IF NOT EXISTS idx_recipes_last_cooked ON meal_planning.recipes(last_cooked_date);
CREATE INDEX IF NOT EXISTS idx_inventory_name ON meal_planning.inventory(name);
```

**Query Optimization:**

```sql
-- Use EXPLAIN to analyze query performance
EXPLAIN ANALYZE SELECT * FROM meal_planning.recipes WHERE title ILIKE '%chicken%';
```

**Connection Pooling:**

Configure in `backend/src/core/database.py`:

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### Application Optimization

**Caching:**

Consider adding Redis for caching:

```yaml
# docker-compose.yml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
```

**Resource Allocation:**

```yaml
# docker-compose.yml
backend:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 2G
      reservations:
        cpus: '1'
        memory: 1G
```

### Monitoring Tools

**Prometheus + Grafana:**

For advanced monitoring, consider setting up:

- Prometheus for metrics collection
- Grafana for visualization
- AlertManager for notifications

---

## Additional Resources

**Related Documentation:**
- [User Guide](USER_GUIDE.md) - End-user documentation
- [Developer Guide](DEVELOPER_GUIDE.md) - Development setup
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Deployment instructions
- [API Documentation](API_DOCUMENTATION.md) - API reference

**External Resources:**
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)

**Support:**
- GitHub Issues: Report bugs, request features
- Documentation: Check guides for information

---

**Document Version:** 1.0
**Last Updated:** October 1, 2025
**Application Version:** 1.0.2

# Infrastructure Configuration

This directory contains the Docker Compose configuration and deployment files for the Household Meal Planning System.

## Quick Start

### 1. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your settings
nano .env
```

**Important:** Generate secure secrets for production:
```bash
# Generate secure passwords/secrets
openssl rand -hex 32
```

### 2. Start Services

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Check status
docker compose ps
```

### 3. Initialize Database

The database will be automatically initialized on first start using the SQL files in `../database/`.

### 4. Access Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **PostgreSQL:** localhost:5432

## Files

- **docker-compose.yml** - Main Docker Compose configuration
- **.env** - Environment variables (create from .env.example)
- **.env.example** - Example environment configuration
- **nginx.conf** - Nginx reverse proxy configuration
- **generate-ssl.sh** - Script to generate self-signed SSL certificates
- **proxmox-setup.md** - Proxmox VM deployment guide

## Environment Variables

See `.env.example` for all available configuration options. Key variables:

### Required
- `DB_PASSWORD` - PostgreSQL password (generate secure value)
- `JWT_SECRET` - JWT signing secret (generate with openssl)
- `SESSION_SECRET` - Session signing secret (generate with openssl)

### Optional
- `DB_HOST` - Database host (default: postgres)
- `DB_PORT` - Database port (default: 5432)
- `DB_NAME` - Database name (default: household_db)
- `DB_USER` - Database user (default: household_app)

## Common Commands

```bash
# Stop services
docker compose down

# Restart services
docker compose restart

# Rebuild images
docker compose build

# View logs for specific service
docker compose logs backend
docker compose logs frontend
docker compose logs postgres

# Execute command in container
docker compose exec backend python --version
docker compose exec postgres psql -U household_app -d household_db
```

## Troubleshooting

### Services won't start
- Check `.env` file exists in this directory
- Verify all required environment variables are set
- Check Docker logs: `docker compose logs`

### Database connection errors
- Ensure PostgreSQL is healthy: `docker compose ps`
- Verify DATABASE_URL is correct
- Check database logs: `docker compose logs postgres`

### Frontend build fails
- Clear Docker cache: `docker compose build --no-cache frontend`
- Check package.json syntax
- Verify all dependencies are listed

## Production Deployment

For production deployment, see:
- `../docs/DEPLOYMENT_GUIDE.md` - Complete deployment guide
- `proxmox-setup.md` - Proxmox-specific setup
- `nginx.conf` - Production Nginx configuration

## Security Notes

**Never commit `.env` files to version control!**

The `.env` file contains sensitive credentials and should be:
- Listed in `.gitignore`
- Backed up securely
- Unique per environment (dev, staging, prod)

## Support

For detailed documentation, see:
- [Deployment Guide](../docs/DEPLOYMENT_GUIDE.md)
- [Admin Guide](../docs/ADMIN_GUIDE.md)
- [Developer Guide](../docs/DEVELOPER_GUIDE.md)

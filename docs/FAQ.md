# Frequently Asked Questions (FAQ)

## Table of Contents

1. [General Questions](#general-questions)
2. [User Questions](#user-questions)
3. [Developer Questions](#developer-questions)
4. [Administrator Questions](#administrator-questions)
5. [Troubleshooting](#troubleshooting)

---

## General Questions

### What is the Household Meal Planning System?

The Household Meal Planning System is a locally-hosted web application designed to help families manage recipes, track kitchen inventory, plan weekly menus, and generate shopping lists. It provides features like recipe versioning, web scraping, inventory tracking with expiration alerts, intelligent recipe suggestions, and more.

### Who should use this application?

- **Families** looking to organize meal planning
- **Home cooks** who want to manage their recipe collection
- **Household managers** tracking inventory and shopping
- **Anyone** wanting to reduce food waste and plan meals efficiently

### What platforms does it run on?

The application is platform-independent and runs in Docker containers. It can be deployed on:

- Local servers (Proxmox VM, home server)
- Cloud platforms (AWS, DigitalOcean, Azure, GCP)
- Development machines (Windows, macOS, Linux with Docker)

### Is it free to use?

Yes, the application is open source and free to use. There are no subscription fees or licensing costs.

### Can I use it offline?

The application runs on your local network, so you don't need internet access for day-to-day use. However, internet is required for:
- Recipe web scraping (importing recipes from websites)
- Initial software updates
- Installing dependencies

### How many users can it support?

The system is designed for household use (5-10 concurrent users). With proper hardware, it can support more users, but it's optimized for family-sized deployments.

### What browsers are supported?

The application works with modern browsers:
- **Chrome** (recommended)
- **Firefox**
- **Safari**
- **Edge**

Internet Explorer is not supported.

### Is my data secure?

Yes. The application:
- Runs on your local network (no external exposure)
- Uses HTTPS encryption
- Stores passwords with bcrypt hashing
- Implements JWT-based authentication
- Follows security best practices

For maximum security, keep it on your local network without internet exposure.

### Can I access it from my phone?

Yes! The web interface is responsive and works on mobile browsers. You can access it from any device on your local network by navigating to the application URL.

---

## User Questions

### How do I create an account?

**If you're the first user:**
1. The system administrator will create the first admin account during installation
2. Contact your admin to get your credentials

**For subsequent users:**
1. An admin user must create your account
2. Go to the login page
3. If registration is enabled, click "Register" and fill in the form
4. Otherwise, contact your admin to create an account for you

### I forgot my password. How do I reset it?

Currently, password reset must be done by an administrator:

1. Contact your system administrator
2. They can reset your password through the admin panel or database
3. You'll receive a new temporary password
4. Log in and immediately change to a new password in your profile

Self-service password reset is planned for a future version.

### How do I add a recipe from a website?

1. Go to **Recipes** → **Import from Web**
2. Enter the recipe URL (e.g., from AllRecipes, Food Network, etc.)
3. Click **"Scrape Recipe"**
4. Review the imported data
5. Make any necessary edits
6. Click **"Save Recipe"**

**Note:** Not all websites are supported. If scraping fails, you can manually enter the recipe.

### Why isn't my recipe scraping working?

Common reasons:

1. **Website not supported**: The scraper works with sites that follow standard recipe schema markup
2. **Rate limit**: You may need to wait 5 seconds between scrape requests
3. **robots.txt blocking**: Some sites don't allow automated scraping
4. **Network issues**: Check your internet connection
5. **Incorrect URL**: Ensure you're using the direct recipe page URL

**Solution:** Try a different recipe site or manually enter the recipe.

### How does recipe versioning work?

Every time you edit a recipe, a new version is created:

1. Old versions are preserved (never deleted)
2. The version number increments (v1 → v2 → v3)
3. You can view version history
4. You can revert to a previous version
5. Menu plans always use the latest version

This allows you to track changes and undo mistakes.

### What happens when I mark a meal as cooked?

Several things happen automatically:

1. Recipe's **times_cooked** counter increments
2. Recipe's **last_cooked_date** updates to today
3. **Inventory is auto-deducted** (ingredients are removed from stock)
4. **Inventory history** records the deduction
5. You may receive a prompt to rate the recipe

### How are favorites calculated?

A recipe becomes a "favorite" when:

1. At least **X users** have rated it (default: 2)
2. At least **Y%** of ratings are positive (default: 75%)

**Example:**
- 4 users rate a recipe
- 3 thumbs up, 1 thumbs down
- 75% positive (3/4) → Recipe becomes a favorite

Admins can adjust the threshold and minimum raters in system settings.

### How do recipe suggestions work?

The system uses 6 different suggestion strategies:

1. **Rotation**: Suggests recipes not cooked recently or never tried
2. **Favorites**: Household favorites based on ratings
3. **Never Tried**: Recipes you've never cooked (times_cooked = 0)
4. **Available Inventory**: Recipes you can make with current stock
5. **Seasonal**: Recipes tagged for the current season
6. **Quick Meals**: Recipes under 30 minutes total time

You can switch between strategies to get different suggestions.

### Can I customize suggestion strategies?

The 6 built-in strategies cover most use cases, but you can influence suggestions by:

- **Rating recipes**: Affects the "Favorites" strategy
- **Cooking recipes**: Affects "Rotation" (recently cooked are deprioritized)
- **Updating inventory**: Affects "Available Inventory"
- **Tagging recipes**: Affects "Seasonal" (add season tags)
- **Setting cook times**: Affects "Quick Meals"

Custom strategies require code changes (see Developer Guide).

### How do I print my shopping list?

1. Generate a shopping list from your menu plan
2. Click the **"Print"** button
3. Your browser's print dialog will open
4. Select your printer or **"Save as PDF"**
5. Click **"Print"**

The list is formatted for easy reading and includes checkboxes.

### Why am I seeing low stock alerts?

Low stock alerts are triggered when:

1. An inventory item's quantity drops below its **minimum threshold**
2. The threshold is set when you add/edit the inventory item
3. Example: You set milk minimum to 1 gallon, current stock is 0.5 gallons

**To stop alerts:** Adjust or remove the minimum threshold for that item.

### How do I turn off notifications?

Currently, notifications are system-wide and cannot be disabled per-user. However, you can:

1. **Mark as read**: Click notifications to dismiss them
2. **Mark all as read**: Use the "Mark All Read" button
3. **Delete**: Remove individual notifications

Per-user notification preferences are planned for a future version.

### Can I share recipes with other users?

All recipes are shared automatically within the household. Any user can:
- View all recipes
- Use recipes in their menu plans
- Rate recipes
- See recipe statistics

Individual users cannot have "private" recipes in the current version.

---

## Developer Questions

### How do I set up the development environment?

See the [Developer Guide](DEVELOPER_GUIDE.md#development-environment-setup) for complete instructions. Quick summary:

1. Install Python 3.12+, Node 18+, PostgreSQL 15+, Docker
2. Clone the repository
3. Set up backend (create venv, install deps, configure .env)
4. Set up frontend (npm install, configure .env.local)
5. Initialize database (run schema SQL files)
6. Create admin user
7. Start backend (`uvicorn src.main:app --reload`)
8. Start frontend (`npm run dev`)

### What's the tech stack?

**Backend:**
- FastAPI (Python 3.12)
- SQLAlchemy 2.0 ORM
- PostgreSQL 15
- JWT authentication
- BeautifulSoup4 for web scraping

**Frontend:**
- Next.js 14 (App Router)
- React 18
- TypeScript (strict mode)
- Tailwind CSS
- TanStack Query for data fetching
- Zustand for state management

**Infrastructure:**
- Docker + Docker Compose
- Nginx (reverse proxy)
- PostgreSQL multi-schema design

### How do I run tests?

**Backend:**
```bash
cd backend
pytest
pytest --cov=src --cov-report=html
```

**Frontend:**
```bash
cd frontend
npm test
npm run test:coverage
```

See [Testing Guide](TESTING.md) for details.

### How do I add a new API endpoint?

1. **Create/update model** in `backend/src/models/`
2. **Create Pydantic schemas** in `backend/src/schemas/`
3. **Create service method** in `backend/src/services/`
4. **Create API route** in `backend/src/api/`
5. **Add tests** in `backend/tests/`
6. **Update API spec** in `docs/API_SPEC.yaml`

See [Developer Guide](DEVELOPER_GUIDE.md#adding-new-features) for detailed steps.

### How do I add a new page to the frontend?

1. **Create types** in `frontend/src/types/`
2. **Create API client methods** in `frontend/src/lib/api/`
3. **Create components** in `frontend/src/components/`
4. **Create page** in `frontend/src/app/` following Next.js App Router conventions
5. **Add navigation** link if needed

### What's the database schema?

The database uses a **multi-schema design**:

- **shared**: Users, sessions, notifications, activity logs
- **meal_planning**: Recipes, inventory, ratings, menu plans, shopping lists

Key tables:
- `recipes` and `recipe_versions` (version control)
- `inventory` and `inventory_history` (change tracking)
- `ratings` (thumbs up/down)
- `menu_plans` and `planned_meals` (weekly planning)

See [Database Schema](DATABASE_SCHEMA.md) for complete details.

### How does authentication work?

1. User logs in with username/password
2. Backend validates credentials (bcrypt password check)
3. Backend generates JWT token (includes user_id, role, expiration)
4. Token stored in httpOnly cookie
5. Frontend includes cookie in API requests
6. Backend validates token on protected routes

See [Developer Guide](DEVELOPER_GUIDE.md#authentication--authorization) for implementation.

### How do I debug issues?

**Backend:**
```bash
# View logs
docker-compose logs backend

# Use debugger
import pdb; pdb.set_trace()

# Check database
docker exec -it meal-planning-db psql -U meal_planner household_db
```

**Frontend:**
```bash
# View logs
docker-compose logs frontend

# Use browser DevTools (Console, Network, React DevTools)
```

See [Developer Guide](DEVELOPER_GUIDE.md#debugging) for more.

### How do I contribute?

1. Fork the repository
2. Create a feature branch (`feature/my-new-feature`)
3. Make your changes
4. Add tests
5. Update documentation
6. Commit with conventional commit messages
7. Push and create a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## Administrator Questions

### How do I deploy the application?

See the [Deployment Guide](DEPLOYMENT_GUIDE.md) for complete instructions.

**Quick summary for production:**
1. Set up server (Ubuntu Server 22.04 on Proxmox VM)
2. Install Docker and Docker Compose
3. Clone repository
4. Configure environment variables (`.env`)
5. Build and start services (`docker-compose up -d`)
6. Initialize database
7. Create admin user
8. Set up Nginx reverse proxy
9. Generate SSL certificate
10. Configure backups

### How do I create an admin user?

**Method 1 (Recommended):**
```bash
docker-compose exec backend python scripts/create_admin.py
```

**Method 2 (Manual SQL):**
```bash
docker exec -it meal-planning-db psql -U meal_planner household_db
```

```sql
INSERT INTO shared.users (id, username, email, password_hash, role, is_active)
VALUES (
  gen_random_uuid(),
  'admin',
  'admin@localhost',
  '<bcrypt-hash>',
  'admin',
  true
);
```

See [Admin Guide](ADMIN_GUIDE.md#creating-the-first-admin-user) for details.

### How do I back up the database?

**Manual backup:**
```bash
docker exec meal-planning-db pg_dump -U meal_planner household_db | gzip > backup_$(date +%Y%m%d).sql.gz
```

**Automated backup:**
Create a cron job:
```bash
0 2 * * * /opt/meal-planning-system/scripts/backup.sh >> /var/log/meal-planning-backup.log 2>&1
```

See [Admin Guide](ADMIN_GUIDE.md#database-backups) for backup scripts.

### How do I update the application?

```bash
# Pull latest code
cd /opt/meal-planning-system
git pull origin main

# Rebuild containers
docker-compose down
docker-compose up -d --build

# Run migrations (if needed)
docker-compose exec backend python scripts/migrate.py

# Verify
docker-compose ps
curl -k https://localhost/api/health
```

### How do I monitor system health?

**Check service status:**
```bash
docker-compose ps
```

**View logs:**
```bash
docker-compose logs -f
```

**Check resources:**
```bash
docker stats
```

**Database health:**
```bash
docker exec meal-planning-db pg_isready -U meal_planner
```

See [Admin Guide](ADMIN_GUIDE.md#monitoring-and-maintenance) for more monitoring options.

### How do I configure settings?

1. Log in as admin
2. Go to **Admin** → **Settings**
3. Adjust:
   - Favorites threshold and minimum raters
   - Low stock threshold days
   - Expiration warning days
   - Scraper rate limit
4. Click **Save Settings**

Or edit via database:
```sql
UPDATE meal_planning.admin_settings
SET favorites_threshold_percentage = 80;
```

See [Admin Guide](ADMIN_GUIDE.md#system-configuration) for all settings.

### What are the server requirements?

**Minimum:**
- 2 CPU cores
- 4 GB RAM
- 20 GB storage
- 100 Mbps network

**Recommended:**
- 4 CPU cores
- 8 GB RAM
- 50 GB SSD
- 1 Gbps network

See [Admin Guide](ADMIN_GUIDE.md#system-requirements) for details.

---

## Troubleshooting

### Application won't start

**Check Docker services:**
```bash
docker-compose ps
docker-compose logs
```

**Common causes:**
1. Port conflicts (80, 443, 8000, 3000, 5432)
2. Missing or incorrect `.env` file
3. Database connection failure

**Solution:**
```bash
docker-compose down
docker-compose up -d --build
```

### Database connection errors

**Test connection:**
```bash
docker exec meal-planning-db psql -U meal_planner -d household_db -c "SELECT 1;"
```

**Check DATABASE_URL:**
```bash
cat .env | grep DATABASE_URL
```

**Verify container is running:**
```bash
docker-compose ps postgres
```

### Authentication not working

**Check:**
1. SECRET_KEY is set in `.env`
2. Token expiration settings
3. System clock is synchronized (JWT tokens are time-sensitive)

**Solution:**
```bash
# Verify SECRET_KEY
grep SECRET_KEY .env

# Sync time
sudo ntpdate pool.ntp.org
```

### Recipe scraper failing

**Common causes:**
1. Website not supported
2. Rate limit exceeded (5 seconds between requests)
3. No internet connection
4. Website blocking automated access

**Solution:**
1. Use supported websites (AllRecipes, Food Network, etc.)
2. Wait between scrape attempts
3. Manually enter recipe if scraping fails

### Performance issues

**Check resources:**
```bash
docker stats
df -h
```

**Optimize database:**
```bash
docker exec meal-planning-db psql -U meal_planner -d household_db -c "VACUUM ANALYZE;"
```

**Restart services:**
```bash
docker-compose restart
```

### Tests failing

**Backend tests:**
```bash
cd backend
pip install -r requirements-test.txt
pytest -v
```

**Frontend tests:**
```bash
cd frontend
npm install
npm test
```

**Check test database:**
- Tests use in-memory SQLite by default
- Ensure test fixtures are set up correctly

### Docker issues

**Remove all containers and rebuild:**
```bash
docker-compose down -v
docker-compose up -d --build
```

**Clean Docker system:**
```bash
docker system prune -a
```

**Check disk space:**
```bash
docker system df
df -h
```

---

## Additional Help

### Where can I find more information?

**Documentation:**
- [User Guide](USER_GUIDE.md) - Complete user documentation
- [Developer Guide](DEVELOPER_GUIDE.md) - Development setup and architecture
- [Admin Guide](ADMIN_GUIDE.md) - System administration
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Deployment instructions
- [API Documentation](API_DOCUMENTATION.md) - API reference
- [Testing Guide](TESTING.md) - Testing documentation

**External Resources:**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

### How do I report bugs?

1. Check if the issue is already reported in GitHub Issues
2. If not, create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, browser, version)
   - Relevant logs or screenshots
3. Label appropriately (bug, enhancement, question, etc.)

### How do I request features?

1. Check if the feature is already requested
2. Create a new GitHub Issue with:
   - Clear feature description
   - Use case and benefits
   - Proposed implementation (optional)
   - Label as "enhancement"

### How do I get support?

1. **Check documentation**: Most questions are answered in the guides
2. **Search FAQ**: This document covers common issues
3. **GitHub Issues**: Search for similar issues or create a new one
4. **Community**: Check discussions for community help

---

**Document Version:** 1.0
**Last Updated:** October 1, 2025
**Application Version:** 1.0.0

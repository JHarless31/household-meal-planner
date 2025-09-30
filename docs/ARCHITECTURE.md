# System Architecture

## Overview

The Household Meal Planning System is a full-stack web application designed for local deployment on a Proxmox VM. It uses a microservices-inspired architecture with separate backend (API), frontend (UI), database, and reverse proxy services.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Local Network                        │
│                                                               │
│  ┌──────────┐         ┌─────────────────────────────────┐  │
│  │  Client  │────────▶│      Nginx (Reverse Proxy)      │  │
│  │ (Browser)│         │   - HTTPS (SSL/TLS)              │  │
│  └──────────┘         │   - Route /api/* → Backend       │  │
│                        │   - Route /* → Frontend         │  │
│                        └──────────────┬──────────────────┘  │
│                                       │                      │
│                        ┌──────────────┴──────────────┐      │
│                        │                              │      │
│               ┌────────▼────────┐         ┌─────────▼───────┐
│               │   Frontend      │         │    Backend      │
│               │   (Next.js)     │         │   (FastAPI)     │
│               │   - React UI    │         │   - REST API    │
│               │   - TypeScript  │         │   - Business    │
│               │   - SSR/CSR     │         │     Logic       │
│               └─────────────────┘         └────────┬────────┘
│                                                      │
│                                         ┌────────────▼────────┐
│                                         │   PostgreSQL 15     │
│                                         │   - Multi-schema    │
│                                         │   - meal_planning   │
│                                         │   - shared          │
│                                         │   - chores (future) │
│                                         │   - learning (future)│
│                                         │   - rewards (future)│
│                                         └─────────────────────┘
│                                                               │
└─────────────────────────────────────────────────────────────┘
              All services run in Docker containers
              on Ubuntu VM in Proxmox hypervisor
```

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.12)
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL 15
- **Authentication**: JWT tokens with httpOnly cookies
- **Password Hashing**: bcrypt
- **Migrations**: Alembic
- **Web Scraping**: BeautifulSoup4 + requests
- **Testing**: pytest, pytest-cov
- **Linting**: flake8 or pylint
- **Formatting**: black

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **UI Library**: React 18
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **Forms**: React Hook Form
- **API Client**: React Query (TanStack Query)
- **State Management**: Zustand or React Context
- **Drag-and-Drop**: react-dnd or dnd-kit
- **Testing**: Jest, React Testing Library, Playwright
- **Linting**: ESLint
- **Formatting**: Prettier

### Database
- **RDBMS**: PostgreSQL 15
- **Architecture**: Multi-schema design
- **Schemas**:
  - `shared` - Users, auth, admin tables
  - `meal_planning` - Recipes, inventory, menus, ratings
  - `chores` - Future chores tracking app
  - `learning` - Future learning app
  - `rewards` - Future rewards/allowance app

### Infrastructure
- **Containerization**: Docker 24+
- **Orchestration**: Docker Compose 2.20+
- **Reverse Proxy**: Nginx 1.24+
- **SSL/TLS**: Self-signed certificates for local HTTPS
- **CI/CD**: GitHub Actions
- **Deployment Target**: Ubuntu Server 22.04 LTS on Proxmox VM

## Database Schema Design

### Multi-Schema Approach

The database uses PostgreSQL schemas to logically separate different applications while maintaining a single database instance. This enables:
- **Cross-schema queries** for dashboard aggregation
- **Easier backup management** (single database)
- **Better resource utilization** (shared connection pool)
- **Clear separation of concerns**

### Core Schemas

#### `shared` Schema
Contains tables shared across all household applications:
- `users` - User accounts (family members)
- `sessions` - Authentication sessions
- `admin_settings` - System-wide configuration

#### `meal_planning` Schema
Contains meal planning app tables:
- `recipes` - Recipe metadata with current_version
- `recipe_versions` - Full version history with snapshots
- `ingredients` - Linked to recipe_versions
- `inventory` - Current kitchen inventory
- `inventory_history` - Track quantity changes
- `ratings` - User-specific thumbs up/down ratings
- `menu_plans` - Weekly menu planning
- `planned_meals` - Individual meals in menu
- `admin_settings` - App-specific settings (favorites threshold, etc.)

#### Future Schemas
- `chores` - Task assignments, completion tracking
- `learning` - Educational modules, progress
- `rewards` - Allowance, rewards, point tracking

*Detailed schema diagrams will be in `docs/DATABASE_SCHEMA.md` (Agent 1)*

## API Design

### RESTful API Endpoints

Base URL: `/api`

**Authentication:**
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/logout`
- `GET /auth/me`

**Recipes:**
- `GET /recipes` - List with pagination, filters
- `GET /recipes/:id` - Get latest version
- `GET /recipes/:id/versions/:version` - Get specific version
- `POST /recipes` - Create recipe
- `PUT /recipes/:id` - Update (creates new version)
- `DELETE /recipes/:id` - Delete recipe
- `POST /recipes/scrape` - Scrape from URL

**Inventory:**
- `GET /inventory` - List items
- `POST /inventory` - Add item
- `PUT /inventory/:id` - Update item
- `DELETE /inventory/:id` - Remove item
- `GET /inventory/low-stock` - Low stock alerts
- `GET /inventory/expiring` - Items expiring soon

**Ratings:**
- `POST /recipes/:id/ratings` - Rate recipe
- `PUT /recipes/:id/ratings/:ratingId` - Update rating
- `DELETE /recipes/:id/ratings/:ratingId` - Remove rating

**Menu Planning:**
- `GET /menu-plans` - List menu plans
- `GET /menu-plans/:id` - Get specific plan
- `POST /menu-plans` - Create plan
- `PUT /menu-plans/:id` - Update plan
- `DELETE /menu-plans/:id` - Delete plan
- `POST /menu-plans/:id/meals/:mealId/cooked` - Mark as cooked (triggers inventory deduction)

**Shopping Lists:**
- `GET /shopping-list/:menuPlanId` - Generate list
- `POST /shopping-list/:id/items/:itemId/check` - Mark purchased

**Admin:**
- `GET /admin/users` - List users
- `POST /admin/users` - Create user
- `PUT /admin/users/:id` - Update user
- `DELETE /admin/users/:id` - Delete user
- `GET /admin/settings` - Get settings
- `PUT /admin/settings` - Update settings

*Complete OpenAPI 3.0 specification will be in `docs/API_SPEC.yaml` (Agent 1)*

## Authentication & Authorization

### JWT-Based Authentication
- User logs in with username/password
- Backend validates credentials (bcrypt password check)
- Backend generates JWT token (includes user_id, role, expiration)
- Token stored in httpOnly cookie (XSS protection)
- Frontend includes cookie in all API requests
- Backend validates token on protected endpoints

### Role-Based Access Control (RBAC)
- **Admin**: Full access to all features + user management + settings
- **User**: Standard access to meal planning features
- **Child** (future): Limited access (view-only for certain features)

### Session Management
- Configurable session timeout (default: 24 hours)
- Refresh token mechanism (optional)
- Logout invalidates token

## Security Considerations

### API Security
- **SQL Injection**: SQLAlchemy ORM with parameterized queries
- **XSS**: Output escaping, Content Security Policy headers
- **CSRF**: CSRF tokens on state-changing operations
- **Rate Limiting**: Limit login attempts (5 per 15 minutes)
- **Input Validation**: Pydantic models validate all inputs
- **HTTPS**: All traffic encrypted (even locally)

### Web Scraping Ethics
- Check `robots.txt` before scraping
- Rate limiting: Max 1 request per 5 seconds per domain
- User-Agent: Identifies application
- Handle errors gracefully (don't DOS websites)
- Display warning if robots.txt disallows

### Password Security
- Bcrypt hashing (12 rounds minimum)
- Password requirements: min 8 chars, complexity
- Optional: password reset via email

## Performance Optimization

### Backend
- Database connection pooling (SQLAlchemy)
- Query optimization (indexes, avoid N+1)
- Response caching (Redis optional for Phase 2+)
- Async/await for I/O operations (FastAPI)

### Frontend
- Code splitting (Next.js automatic)
- Image optimization (Next.js Image component)
- Lazy loading (React.lazy)
- API response caching (React Query)
- Virtual scrolling for long lists (react-window)

### Database
- Indexes on frequently queried columns
- Foreign key constraints for referential integrity
- VACUUM and ANALYZE scheduled maintenance

## Scalability Considerations

### Current Architecture (Phase 1)
- Single VM deployment
- Suitable for household use (5-10 concurrent users)
- All services in Docker containers

### Future Scaling (if needed)
- **Horizontal scaling**: Multiple backend containers behind load balancer
- **Database replication**: Read replicas for scaling reads
- **Caching layer**: Redis for frequently accessed data
- **CDN**: For static assets (images, CSS, JS)

## Monitoring & Logging

### Application Logging
- Structured logging (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Log rotation (daily, keep 30 days)
- Error tracking with stack traces

### Health Checks
- `/api/health` - Backend health
- Docker health checks for all services
- Monitor: CPU, memory, disk usage

### Optional: Observability
- Grafana + Prometheus for metrics
- Dashboards for API response times, error rates, database query times

## Deployment Architecture

### Proxmox VM
- **OS**: Ubuntu Server 22.04 LTS
- **Resources**: 4 cores, 8GB RAM, 50GB storage
- **Network**: Bridge to local network, static IP
- **Firewall**: UFW (allow 80, 443 from local only)

### Docker Containers
```yaml
services:
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - frontend
      - backend
```

### Network Configuration
- Local access only (no external internet exposure)
- Static IP on local network
- Optional: mDNS (meal-planner.local) for easy access
- SSL/TLS with self-signed certificate

## Backup Strategy

### Automated Backups
- **Frequency**: Daily at 2 AM
- **Contents**: PostgreSQL dump, uploads folder, configs
- **Retention**: 7 daily, 4 weekly, 12 monthly
- **Location**: Network-attached storage or separate volume
- **Testing**: Quarterly restore test

### Manual Backups
- Script: `infrastructure/backup-script.sh`
- Command: `./backup-script.sh manual`

## Development Workflow

### Local Development
1. Clone repository
2. Copy `.env.example` to `.env`
3. Run `docker-compose up -d`
4. Backend: `http://localhost:8000`
5. Frontend: `http://localhost:3000`
6. Database: `localhost:5432`

### Multi-Agent Development
- Agents work in parallel where possible
- Feature branches per agent: `feature/agent-X-feature-name`
- Pull requests reviewed before merge
- CI/CD runs tests automatically
- See `docs/AGENT_COORDINATION.md` for details

## Future Enhancements

### Additional Household Apps
- **Chores App**: Task assignments, recurring schedules
- **Learning App**: Educational modules, progress tracking
- **Rewards App**: Allowance, points, purchases

### Dashboard Integration
- Unified dashboard showing data from all apps
- Cross-app notifications
- Consolidated reports

### Advanced Features
- Mobile native apps (React Native)
- Voice assistant integration (recipe reading)
- Meal prep timers
- Smart home integration
- AI meal suggestions (ML-based)
- Nutrition tracking
- Grocery delivery API integration

---

*This architecture is designed for reliability, security, and extensibility while remaining accessible for household deployment.*

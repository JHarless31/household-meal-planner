# Household Meal Planning & Inventory System

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-org/meal-planning-system/releases)
[![License](https://img.shields.io/badge/license-TBD-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-138%20passing-success.svg)](docs/TESTING.md)
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)](docs/TESTING.md)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Node](https://img.shields.io/badge/node-18%2B-green.svg)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/docker-24%2B-blue.svg)](https://www.docker.com/)

A comprehensive, locally-hosted web application for managing recipes, tracking kitchen inventory, planning weekly menus, and generating shopping lists. Built for families who want to organize meals, reduce food waste, and streamline grocery shopping.

---

## Key Features

### Recipe Management
- **Version Control**: Full version history for every recipe edit
- **Web Scraping**: Import recipes automatically from popular recipe websites
- **Smart Search**: Search by title, ingredients, tags, difficulty, or prep time
- **Tag Organization**: Categorize by cuisine, meal type, dietary restrictions, season, and more

### Intelligent Suggestions
Six strategies to help you decide what to cook:
- **Rotation**: Recipes you haven't cooked recently
- **Favorites**: Household favorites based on ratings
- **Never Tried**: New recipes to explore
- **Available Inventory**: What you can make right now
- **Seasonal**: Recipes for the current season
- **Quick Meals**: Fast recipes under 30 minutes

### Inventory Tracking
- **Low Stock Alerts**: Get notified when items run low
- **Expiration Warnings**: Track items nearing expiration
- **Auto-Deduction**: Inventory updates automatically when you cook
- **History Tracking**: See how inventory changes over time

### Menu Planning
- **Weekly Planning**: Plan meals for the entire week
- **Copy Plans**: Duplicate successful weeks
- **Auto-Generate**: Let the system suggest a week's worth of meals
- **Mark as Cooked**: Track which meals you've prepared

### Shopping Lists
- **Auto-Generated**: Create lists from your menu plans
- **Smart Quantities**: Calculates what you need minus current stock
- **Category Grouping**: Organized by grocery store layout
- **Print-Friendly**: Easy to print or save as PDF

### Multi-User Support
- **Role-Based Access**: Admin, user, and child roles
- **Household Ratings**: Everyone can rate recipes
- **Shared Recipes**: All recipes available to all family members
- **Activity Tracking**: Audit log of user actions

---

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy 2.0** - Powerful ORM
- **PostgreSQL 15** - Robust relational database
- **JWT Authentication** - Secure token-based auth
- **BeautifulSoup4** - Web scraping
- **pytest** - Comprehensive testing

### Frontend
- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first styling
- **TanStack Query** - Data fetching and caching
- **Zustand** - State management

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy
- **PostgreSQL** - Multi-schema database design

---

## Quick Start

### Prerequisites
- Docker 24+ and Docker Compose 2.20+
- 4 GB RAM minimum (8 GB recommended)
- 20 GB disk space minimum (50 GB recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd meal-planning-system
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your settings
   ```

3. **Start the application**
   ```bash
   docker compose up -d
   ```

4. **Initialize the database**
   ```bash
   docker compose exec backend python scripts/init_db.py
   ```

5. **Create an admin user**
   ```bash
   docker compose exec backend python scripts/create_admin.py
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

For detailed installation instructions, see the [Deployment Guide](docs/DEPLOYMENT_GUIDE.md).

---

## Documentation

### User Documentation
- **[User Guide](docs/USER_GUIDE.md)** - Complete guide for end users
  - Getting started and navigation
  - Recipe management and suggestions
  - Inventory tracking
  - Menu planning workflow
  - Shopping lists
  - Troubleshooting

### Developer Documentation
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - For developers and contributors
  - Development environment setup
  - Project structure
  - Backend and frontend architecture
  - Adding new features
  - Code style standards
  - Testing guide

- **[API Documentation](docs/API_DOCUMENTATION.md)** - API reference
  - All endpoints with examples
  - Request/response formats
  - Authentication guide
  - Error handling

- **[Testing Guide](docs/TESTING.md)** - Testing infrastructure
  - Running tests
  - Writing tests
  - Coverage requirements
  - CI/CD integration

### Administrator Documentation
- **[Administrator Guide](docs/ADMIN_GUIDE.md)** - For system administrators
  - Installation and configuration
  - User management
  - System settings
  - Monitoring and maintenance
  - Backup and recovery
  - Security hardening

- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Deployment instructions
  - Local development
  - Production deployment (Proxmox VM)
  - Cloud deployment (AWS, DigitalOcean)
  - Docker configuration
  - SSL/TLS setup

### Architecture Documentation
- **[Architecture](docs/ARCHITECTURE.md)** - System architecture overview
- **[Database Schema](docs/DATABASE_SCHEMA.md)** - Complete database design
- **[API Specification](docs/API_SPEC.yaml)** - OpenAPI 3.0 specification

### Additional Resources
- **[FAQ](docs/FAQ.md)** - Frequently asked questions
- **[CHANGELOG](CHANGELOG.md)** - Version history and release notes
- **[CONTRIBUTING](CONTRIBUTING.md)** - How to contribute to the project

---

## Project Structure

```
meal-planning-system/
├── backend/                  # FastAPI backend
│   ├── src/                  # Source code
│   │   ├── api/              # API routes
│   │   ├── core/             # Core functionality
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── utils/            # Utilities
│   └── tests/                # Backend tests
├── frontend/                 # Next.js frontend
│   ├── src/                  # Source code
│   │   ├── app/              # Next.js pages
│   │   ├── components/       # React components
│   │   ├── contexts/         # React contexts
│   │   └── lib/              # Utilities and API clients
│   └── public/               # Static assets
├── database/                 # Database schemas
│   ├── schemas/              # SQL schema files
│   └── seed_data.sql         # Initial data
├── docs/                     # Documentation
├── infrastructure/           # Docker and deployment configs
│   ├── docker-compose.yml    # Docker Compose config
│   ├── nginx.conf            # Nginx configuration
│   └── proxmox-setup.md      # Proxmox deployment guide
└── tests/                    # End-to-end tests
```

---

## Multi-Agent Development

This project was built using a multi-agent development methodology with **6 specialized AI agents**:

1. **Database & Architecture Agent** - Database design, API contracts
2. **Backend API Agent** - FastAPI implementation, business logic
3. **Frontend UI Agent** - React/Next.js UI, accessibility
4. **DevOps & Infrastructure Agent** - Docker, deployment, CI/CD
5. **Testing & QA Agent** - Test suites, quality assurance
6. **Documentation Agent** - User/admin/developer documentation

Each agent specializes in specific aspects of the project, ensuring high-quality implementation across all areas.

See [Agent Coordination](docs/AGENT_COORDINATION.md) for details on the multi-agent workflow.

---

## Development Phases

- ✅ **Phase 0**: Multi-agent framework setup
- ✅ **Phase 1**: Database schema and Docker infrastructure
- ✅ **Phase 2**: Complete backend API (42 files, 4,300+ lines)
- ✅ **Phase 3**: Complete frontend UI (67 files, 5,135+ lines)
- ✅ **Phase 4**: Advanced features (26 files, 3,134+ lines)
  - Recipe suggestions (6 strategies)
  - Notification system
  - Enhanced menu planning
  - Admin dashboard
- ✅ **Phase 5**: Comprehensive testing (18 files, 4,122+ lines, 138+ tests, 85% coverage)
- ✅ **Phase 6**: Complete documentation (11,000+ lines across 10+ documents)
- ✅ **Phase 7**: Production readiness & quality improvements
  - Critical Docker build fixes
  - Code modernization (FastAPI lifespan, SQLAlchemy 2.0)
  - Security documentation enhancements
  - Code formatting standardization

**Total**: 150+ files, 16,600+ lines of code, 50+ API endpoints, 24 database tables

---

## Statistics

### Code
- **Backend**: 42 files, 4,300+ lines
- **Frontend**: 67 files, 5,135+ lines
- **Advanced Features**: 26 files, 3,134+ lines
- **Tests**: 18 files, 4,122+ lines (138+ test functions)
- **Total**: 150+ files, 16,600+ lines of code

### Features
- **API Endpoints**: 50+ RESTful endpoints
- **Database Tables**: 24 tables across multiple schemas
- **Test Coverage**: 85%+ coverage
- **Documentation**: 11,000+ lines across 10+ comprehensive documents

### Performance
- **Recipes**: Support for thousands of recipes with versioning
- **Users**: Optimized for household use (5-10 concurrent users)
- **Response Time**: <100ms for most API calls
- **Database**: Multi-schema design for scalability

---

## Security

- **Authentication**: JWT tokens with httpOnly cookies
- **Password Hashing**: bcrypt (12 rounds minimum)
- **SQL Injection**: Parameterized queries (SQLAlchemy ORM)
- **XSS Protection**: Output escaping, CSP headers
- **CSRF Protection**: Token-based CSRF prevention
- **Rate Limiting**: Login attempt throttling
- **HTTPS/SSL**: Encrypted communication
- **RBAC**: Role-based access control

---

## Screenshots

> **Note**: Add screenshots here for:
> - Dashboard
> - Recipe management
> - Inventory tracking
> - Menu planning
> - Shopping list
> - Admin dashboard

---

## Deployment Options

### Local Development
Perfect for development and testing
- **Requirements**: Docker Desktop
- **Setup Time**: 30 minutes
- **See**: [Deployment Guide](docs/DEPLOYMENT_GUIDE.md#local-development-deployment)

### Production (Proxmox VM)
Ideal for home lab deployment
- **Requirements**: Proxmox VE, Ubuntu Server 22.04
- **Setup Time**: 60-90 minutes
- **See**: [Deployment Guide](docs/DEPLOYMENT_GUIDE.md#production-deployment-proxmox-vm) and [Proxmox Setup](infrastructure/proxmox-setup.md)

### Cloud Deployment
For remote access and managed infrastructure
- **Providers**: AWS, DigitalOcean, Azure, GCP
- **Setup Time**: 45-60 minutes
- **See**: [Deployment Guide](docs/DEPLOYMENT_GUIDE.md#cloud-deployment-options)

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development workflow (Gitflow)
- Branching strategy
- Commit message standards (Conventional Commits)
- Pull request process
- Code style guidelines
- Testing requirements

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`feature/your-feature-name`)
3. Make your changes and add tests
4. Commit with conventional commit messages
5. Push and create a pull request
6. Wait for review and feedback

---

## Testing

The project includes comprehensive testing:

### Backend Tests
- **Unit Tests**: Service layer, business logic
- **Integration Tests**: API endpoints, database operations
- **Security Tests**: Authentication, authorization, input validation
- **Performance Tests**: Query optimization, load testing
- **Coverage**: 85%+ code coverage

### Frontend Tests
- **Component Tests**: React component testing
- **Integration Tests**: Page and workflow testing
- **Accessibility Tests**: WCAG 2.1 compliance

### Running Tests

```bash
# Backend tests
cd backend
pytest --cov=src --cov-report=html

# Frontend tests
cd frontend
npm test
npm run test:coverage
```

See [Testing Guide](docs/TESTING.md) for comprehensive testing documentation.

---

## Roadmap

### Version 1.1 (Planned)
- Email-based password reset
- Per-user notification preferences
- Recipe import/export (CSV, JSON)
- Advanced search with filters
- Recipe categories and collections

### Version 1.2 (Planned)
- Private/personal recipes
- Meal prep tracking
- Recipe sharing between households
- Cooking timers and reminders

### Version 2.0 (Planned)
- Additional household apps:
  - Chores management
  - Learning modules
  - Rewards and allowance
- Unified cross-app dashboard
- Mobile native apps (React Native)
- Voice assistant integration
- Nutrition tracking

See [CHANGELOG.md](CHANGELOG.md) for complete version history and planned features.

---

## Support

### Getting Help

1. **Check Documentation**: Start with [User Guide](docs/USER_GUIDE.md) or [FAQ](docs/FAQ.md)
2. **Search Issues**: Look for similar issues on GitHub
3. **Create Issue**: Report bugs or request features
4. **Community**: Join discussions for community help

### Reporting Issues

When reporting bugs, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, browser, version)
- Relevant logs or screenshots

---

## License

[License Type TBD]

---

## Acknowledgments

### Technology Credits
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework
- [PostgreSQL](https://www.postgresql.org/) - Powerful database
- [Docker](https://www.docker.com/) - Containerization platform
- [recipe-scrapers](https://github.com/hhursev/recipe-scrapers) - Recipe extraction library

### Development Team
Built using a multi-agent AI development approach with 6 specialized agents.

### Contributors
Thank you to all contributors who have helped improve this project!

---

## Contact

- **Repository**: https://github.com/your-org/meal-planning-system
- **Issues**: https://github.com/your-org/meal-planning-system/issues
- **Documentation**: https://github.com/your-org/meal-planning-system/tree/main/docs

---

**Version**: 1.0.2
**Last Updated**: October 1, 2025
**Status**: Production Ready

---

<p align="center">
  Made with ❤️ by the Multi-Agent Development Team
</p>

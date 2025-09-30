# Household Meal Planning & Inventory System

A locally-hosted meal planning application for managing recipes, tracking inventory, planning weekly menus, and integrating with other household management applications.

## Project Overview

This application helps families:
- Store and organize recipes (manual entry or web scraping)
- Track kitchen inventory with expiration dates and low-stock alerts
- Plan weekly menus with drag-and-drop interface
- Generate shopping lists automatically
- Rate recipes and track household favorites
- Rotate recipes for variety

## Technology Stack

- **Backend**: FastAPI (Python 3.12), SQLAlchemy, PostgreSQL
- **Frontend**: Next.js 14+, React 18, TypeScript, Tailwind CSS
- **Database**: PostgreSQL 15 (multi-schema design)
- **Infrastructure**: Docker, Docker Compose, Nginx
- **Deployment**: Proxmox VM (Ubuntu Server 22.04)

## Multi-Agent Development

This project is being built using a multi-agent approach with 6 specialized AI agents:

1. **Database & Architecture Agent** - Database design, API contracts
2. **Backend API Agent** - FastAPI implementation, business logic
3. **Frontend UI Agent** - React/Next.js UI, accessibility
4. **DevOps & Infrastructure Agent** - Docker, deployment, CI/CD
5. **Testing & QA Agent** - Test suites, security audits
6. **Documentation Agent** - User/admin/developer documentation

### Running the Agent Orchestrator

```bash
# Activate virtual environment
source ma/bin/activate

# Initialize project structure
python orchestrator.py init

# Run Phase 1 (Database & Infrastructure)
python orchestrator.py phase1

# Check project status
python orchestrator.py status
```

## Project Structure

```
meal-planning-system/
├── agents_config.py        # Agent definitions
├── orchestrator.py          # Multi-agent coordinator
├── backend/                 # FastAPI backend
├── frontend/                # Next.js frontend
├── database/                # Database schemas and migrations
├── docs/                    # Documentation
├── infrastructure/          # Docker and deployment configs
└── tests/                   # End-to-end tests
```

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- Docker and Docker Compose
- Git

### Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd meal-planning-system
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

3. Follow the detailed setup guide in `docs/LOCAL_SETUP.md`

## Documentation

- [User Guide](docs/USER_GUIDE.md) - How to use the application
- [Admin Guide](docs/ADMIN_GUIDE.md) - System administration
- [Developer Guide](docs/DEVELOPER_GUIDE.md) - Development setup and contribution
- [API Specification](docs/API_SPEC.md) - REST API documentation
- [Database Schema](docs/DATABASE_SCHEMA.md) - Database design
- [Deployment Guide](docs/DEPLOYMENT.md) - Proxmox VM deployment

## Development Phases

- [x] **Phase 0a**: Multi-agent framework setup
- [x] **Phase 0b**: Project initialization and Git setup
- [ ] **Phase 1**: Database schema and Docker infrastructure
- [ ] **Phase 2**: Backend API development
- [ ] **Phase 3**: Frontend UI development
- [ ] **Phase 4**: Advanced features and integration
- [ ] **Phase 5**: Testing and QA
- [ ] **Phase 6**: Documentation
- [ ] **Phase 7**: Production deployment

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow and coding standards.

## License

[License type to be determined]

## Contact

For questions or issues, please open a GitHub issue.

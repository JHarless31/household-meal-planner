# Agent Coordination Protocol

## Overview

This project uses 6 specialized AI agents working together to build the Household Meal Planning System. This document defines how agents coordinate their work.

## Agent Roles & Responsibilities

### Agent 1: Database & Architecture Agent
**Responsibilities:**
- Design PostgreSQL multi-schema database structure
- Create database migrations (Alembic)
- Define API contracts (OpenAPI specification)
- Set up database connection pooling
- Design indexes for performance

**Deliverables:**
- `database/schemas/*.sql` - Schema definitions
- `database/migrations/` - Migration scripts
- `docs/DATABASE_SCHEMA.md` - Schema documentation with ERD
- `docs/API_SPEC.yaml` - OpenAPI 3.0 specification
- `docs/API_SPEC.md` - Human-readable API docs

**Branch Prefix:** `feature/agent-1-*`

### Agent 2: Backend API Agent
**Responsibilities:**
- Implement FastAPI REST API endpoints
- Business logic for all features
- Authentication system (JWT)
- Recipe scraping service (ethical compliance)
- Shopping list generation algorithm
- Unit and integration tests

**Deliverables:**
- `backend/src/` - All backend code
- `backend/tests/` - Test suites
- API endpoint implementations
- 80%+ test coverage

**Dependencies:** Requires Agent 1's API contracts

**Branch Prefix:** `feature/agent-2-*`

### Agent 3: Frontend UI Agent
**Responsibilities:**
- React/Next.js frontend application
- Responsive design (mobile + desktop)
- Accessibility compliance (WCAG 2.1 AA)
- Drag-and-drop interfaces
- Component tests and E2E tests

**Deliverables:**
- `frontend/src/` - All frontend code
- `frontend/tests/` - Test suites
- UI components library
- 80%+ test coverage

**Dependencies:** Requires Agent 1's API contracts

**Branch Prefix:** `feature/agent-3-*`

### Agent 4: DevOps & Infrastructure Agent
**Responsibilities:**
- Docker containerization
- docker-compose orchestration
- Nginx configuration
- CI/CD pipelines (GitHub Actions)
- Proxmox deployment documentation
- Backup scripts

**Deliverables:**
- `backend/Dockerfile`, `frontend/Dockerfile`
- `infrastructure/docker-compose.yml`
- `infrastructure/nginx.conf`
- `.github/workflows/*.yml` - CI/CD configs
- `infrastructure/proxmox-setup.md`
- `infrastructure/backup-script.sh`

**Branch Prefix:** `feature/agent-4-*`

### Agent 5: Testing & QA Agent
**Responsibilities:**
- Comprehensive test suites
- Security audits (OWASP, SQL injection, XSS)
- Performance testing
- Accessibility testing (axe-core, manual)
- Cross-browser/device testing

**Deliverables:**
- Test plans and test cases
- Security audit reports
- Performance benchmark reports
- Accessibility compliance reports
- Test coverage reports

**Branch Prefix:** `feature/agent-5-*`

### Agent 6: Documentation Agent
**Responsibilities:**
- User documentation (beginner-friendly)
- Administrator documentation
- Developer documentation
- API documentation
- Deployment guides

**Deliverables:**
- `docs/USER_GUIDE.md`
- `docs/ADMIN_GUIDE.md`
- `docs/DEVELOPER_GUIDE.md`
- `docs/DEPLOYMENT.md`
- Inline code documentation

**Branch Prefix:** `feature/agent-6-*`

## Communication Protocol

### Shared Resources

**1. API Contracts (Agent 1 → Agents 2 & 3)**
- Agent 1 publishes: `docs/API_SPEC.yaml`
- Agents 2 & 3 implement according to this contract
- Any deviations must be discussed via GitHub Issues

**2. Database Schema (Agent 1 → Agent 2)**
- Agent 1 publishes: `database/schemas/*.sql`
- Agent 2 uses SQLAlchemy models based on this schema
- Schema changes require migration scripts

**3. Docker Environment (Agent 4 → All)**
- Agent 4 provides: `infrastructure/docker-compose.yml`
- All agents test their code in this environment
- Local development setup in `docs/LOCAL_SETUP.md`

### Task Tracking

**GitHub Issues:**
- Each phase has associated GitHub Issues
- Issues labeled with agent number: `agent-1`, `agent-2`, etc.
- Issues include:
  - Clear description
  - Acceptance criteria
  - Dependencies on other agents
  - Deliverables

**GitHub Project Board:**
- Columns: Backlog, In Progress, Review, Done
- Each agent moves their tasks through the board
- Blockers tagged with `blocked` label

### Dependency Management

**Agent Dependencies:**
```
Phase 1: Agent 1 + Agent 4 (parallel, independent)
  ├── Agent 1: Database schema, API contracts
  └── Agent 4: Docker setup

Phase 2-3: Agent 2 + Agent 3 (parallel, both depend on Agent 1)
  ├── Agent 2: Backend (needs API contracts from Agent 1)
  └── Agent 3: Frontend (needs API contracts from Agent 1)

Phase 4: Agent 2 + Agent 3 (integration)
  └── Both agents coordinate on advanced features

Phase 5-6: Agent 5 + Agent 6 (parallel, depend on Phases 1-4)
  ├── Agent 5: Testing (needs working application)
  └── Agent 6: Documentation (needs completed features)

Phase 7: Agent 4 (depends on all previous phases)
  └── Agent 4: Deployment
```

**Declaring Dependencies:**
When starting a task, agents declare dependencies in the Issue:
```markdown
## Dependencies
- [ ] Agent 1: API contracts complete (docs/API_SPEC.yaml)
- [ ] Agent 4: Docker environment ready
```

### Pull Request Workflow

1. **Agent creates feature branch:**
   ```bash
   git checkout -b feature/agent-2-recipe-api
   ```

2. **Agent implements feature with tests**

3. **Agent creates PR with template:**
   ```markdown
   ## What was implemented
   - Recipe CRUD endpoints
   - Recipe versioning system
   - Unit tests (85% coverage)

   ## Testing performed
   - All unit tests passing
   - Integration tests with test database
   - Manual API testing with Postman

   ## Dependencies satisfied
   - ✅ API contracts from Agent 1
   - ✅ Database schema from Agent 1

   ## Related Issues
   Closes #15, #16

   ## Screenshots
   (if applicable)
   ```

4. **CI pipeline runs automatically:**
   - Linting
   - Type checking
   - Unit tests
   - Integration tests

5. **Code review** (can be automated or manual)

6. **Merge to develop** when approved

7. **Delete feature branch**

### Conflict Resolution

**If agents disagree or encounter conflicts:**

1. **API Contract Issues:**
   - Agent 2 or 3 creates GitHub Issue: `api-contract-clarification`
   - Agent 1 responds and updates `docs/API_SPEC.yaml` if needed
   - Affected agents adjust their code

2. **Integration Issues:**
   - Create Issue with label `integration-issue`
   - Relevant agents discuss in Issue comments
   - Orchestrator (human or lead agent) makes final decision

3. **Technical Blockers:**
   - Label Issue as `blocked`
   - Document blocker reason
   - Request help from other agents or orchestrator

## Development Phases Timeline

| Phase | Agents | Duration | Key Deliverables |
|-------|--------|----------|------------------|
| 0a-0b | Orchestrator | Days 1-4 | Project setup, agent framework |
| 1 | 1, 4 | Weeks 1-2 | Database, Docker, API contracts |
| 2 | 2 | Weeks 2-3 | Backend API implementation |
| 3 | 3 | Weeks 2-3 | Frontend UI implementation |
| 4 | 2, 3 | Weeks 4-5 | Integration, advanced features |
| 5 | 5 | Weeks 6-7 | Testing, QA, security audit |
| 6 | 6 | Weeks 7-8 | Documentation |
| 7 | 4 | Week 9 | Production deployment |

## Quality Gates

Before moving to next phase:

**Phase 1 → Phase 2/3:**
- [ ] Database schema finalized and documented
- [ ] API contracts published (OpenAPI spec)
- [ ] Docker environment functional
- [ ] All Phase 1 PRs merged to develop

**Phase 2/3 → Phase 4:**
- [ ] Backend API endpoints implemented
- [ ] Frontend UI components implemented
- [ ] Basic authentication working
- [ ] Core features functional (recipes, inventory)

**Phase 4 → Phase 5:**
- [ ] Integration complete
- [ ] Advanced features working (ratings, menu planning, shopping lists)
- [ ] No critical bugs

**Phase 5 → Phase 6:**
- [ ] Test coverage > 80%
- [ ] Security audit passed (no critical vulnerabilities)
- [ ] Performance benchmarks met
- [ ] Accessibility compliance verified

**Phase 6 → Phase 7:**
- [ ] All documentation complete
- [ ] User guide with screenshots
- [ ] Deployment guide tested

## Tools and Automation

**GitHub Actions (CI/CD):**
- `.github/workflows/backend-tests.yml` - Backend tests on every PR
- `.github/workflows/frontend-tests.yml` - Frontend tests on every PR
- `.github/workflows/deploy.yml` - Deployment automation

**Code Quality:**
- `flake8`, `black` (Python)
- `ESLint`, `Prettier` (TypeScript/React)
- `pytest` (Backend tests)
- `Jest`, `Playwright` (Frontend tests)

**Agent Orchestrator:**
- `orchestrator.py` - Coordinates agent workflow
- Runs phases sequentially
- Manages agent task assignment
- Generates status reports

## Monitoring Progress

**Check status:**
```bash
python orchestrator.py status
```

**View GitHub Project Board:**
[Link to project board]

**Daily Standup (Async):**
Each agent (or orchestrator) posts to GitHub Discussions:
- What was completed yesterday
- What is planned for today
- Any blockers

## Contact and Support

For questions about agent coordination:
- Check this document first
- Open a GitHub Issue with label `coordination`
- Tag relevant agents (e.g., `@agent-1`, `@agent-2`)

---

*Last updated: Phase 0 - Initial setup*

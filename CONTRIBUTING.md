# Contributing to Household Meal Planning System

## Development Workflow

This project uses **Gitflow** branching strategy and is developed by specialized AI agents.

### Branching Strategy

- `main` - Production-ready code
- `develop` - Integration branch for ongoing development
- `feature/agent-[number]-[feature-name]` - Individual features

### Commit Standards

We follow **Conventional Commits** specification:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example:**
```
feat(recipe-api): add recipe versioning endpoint

- Implement POST /api/recipes/:id/versions
- Add version comparison logic
- Update recipe model with version tracking

Resolves: #42
```

### Pull Request Process

1. Create feature branch from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/agent-2-recipe-api
   ```

2. Implement feature with tests (80%+ coverage required)

3. Create pull request with description including:
   - What was implemented
   - Testing performed
   - Screenshots (if UI changes)
   - Related issues

4. Wait for CI pipeline to pass

5. Request code review

6. Merge to `develop` when approved

7. Delete feature branch

### Definition of Done

A feature is "done" when:

- [ ] Code is complete and follows style guide
- [ ] Unit tests written and passing
- [ ] Integration tests written and passing
- [ ] Code reviewed (if multi-person team)
- [ ] Documentation updated
- [ ] No linting errors
- [ ] No security vulnerabilities
- [ ] Merged to develop branch
- [ ] Deployed and tested in staging environment

### Code Quality Standards

**Backend (Python)**
- Linting: `flake8` or `pylint`
- Formatting: `black`
- Type hints: Required for all functions
- Docstrings: Google style for all functions/classes
- Test coverage: Minimum 80%

**Frontend (TypeScript/React)**
- Linting: `ESLint`
- Formatting: `Prettier`
- Type safety: TypeScript strict mode
- JSDoc: Document all components and functions
- Test coverage: Minimum 80%

### Running Tests

**Backend:**
```bash
cd backend
pytest
pytest --cov=src tests/
```

**Frontend:**
```bash
cd frontend
npm test
npm run test:coverage
```

**E2E Tests:**
```bash
cd tests/e2e
npx playwright test
```

### Code Review Guidelines

When reviewing code:
- Check for security vulnerabilities
- Verify test coverage
- Ensure accessibility standards (WCAG 2.1 AA)
- Confirm documentation is updated
- Test functionality manually if needed

### Agent Coordination

Each agent works on specific areas:

- **Agent 1 (Database)**: Schema changes, migrations, API contracts
- **Agent 2 (Backend)**: Python/FastAPI code
- **Agent 3 (Frontend)**: React/Next.js code
- **Agent 4 (DevOps)**: Docker, CI/CD, deployment
- **Agent 5 (Testing)**: Test suites, security audits
- **Agent 6 (Documentation)**: All documentation files

Agents communicate via:
- GitHub Issues for tasks
- Shared documentation in `docs/`
- Pull request comments
- API contracts (OpenAPI spec)

### Questions or Issues?

- Open a GitHub issue for bugs or feature requests
- Check `docs/DEVELOPER_GUIDE.md` for development setup help
- Review `docs/AGENT_COORDINATION.md` for agent workflow

Thank you for contributing!

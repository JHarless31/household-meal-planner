# Definition of Done

A feature or task is considered "Done" when all the following criteria are met:

## Code Quality

- [ ] **Code is complete** and implements all requirements from the Issue
- [ ] **Follows style guide**:
  - Python: Black formatting, Flake8/Pylint passing
  - TypeScript/React: ESLint + Prettier passing
  - No linting errors or warnings
- [ ] **Type safety**:
  - Python: Type hints on all functions
  - TypeScript: No `any` types (unless absolutely necessary with comment)
- [ ] **Code is readable**:
  - Clear variable and function names
  - Logical structure and organization
  - No duplicate code (DRY principle)

## Documentation

- [ ] **Code documentation**:
  - Python: Docstrings (Google style) for all functions/classes
  - TypeScript: JSDoc comments for components and functions
  - Complex logic explained with inline comments
- [ ] **README updated** (if new feature affects setup/usage)
- [ ] **API documentation updated** (if API changes)
- [ ] **User-facing documentation updated** (if UI/UX changes)

## Testing

- [ ] **Unit tests written** for all new code
- [ ] **Integration tests written** for API endpoints or component integration
- [ ] **Tests are passing** locally and in CI
- [ ] **Test coverage** ≥ 80% for the modified/new code
- [ ] **Edge cases covered**:
  - Empty data handling
  - Invalid inputs rejected with clear errors
  - Boundary conditions tested

## Security

- [ ] **No security vulnerabilities**:
  - SQL injection prevention (parameterized queries)
  - XSS prevention (output escaping)
  - CSRF tokens implemented (where applicable)
  - Input validation on all endpoints/forms
- [ ] **Authentication/Authorization** verified (if applicable)
- [ ] **Secrets not hardcoded** (use environment variables)
- [ ] **Dependencies scanned** (npm audit / pip-audit passing)

## Accessibility (Frontend only)

- [ ] **WCAG 2.1 Level AA compliance**:
  - Keyboard navigation works
  - Focus indicators visible
  - Screen reader compatible (tested with NVDA/VoiceOver)
  - ARIA labels where needed
  - Color contrast ≥ 4.5:1 for text
  - Alt text on all images

## Performance

- [ ] **Performance requirements met**:
  - API response time < 200ms (for most endpoints)
  - Page load time < 2 seconds
  - No N+1 database queries
  - Images optimized and lazy-loaded (frontend)
- [ ] **No memory leaks** detected

## Code Review

- [ ] **Code reviewed** by at least one other agent or developer
- [ ] **All review comments addressed** or discussed
- [ ] **Approved by reviewer(s)**

## Version Control

- [ ] **Branch naming convention followed**: `feature/agent-X-feature-name`
- [ ] **Commit messages follow Conventional Commits**:
  - Format: `type(scope): subject`
  - Clear and descriptive
- [ ] **No merge conflicts** with develop branch
- [ ] **Feature branch up-to-date** with latest develop

## CI/CD

- [ ] **CI pipeline passing**:
  - All automated tests passing
  - Linting checks passing
  - Type checking passing
  - Security scans passing
- [ ] **Build succeeds** (for Docker builds)

## Integration

- [ ] **Integrates correctly** with other components:
  - Backend matches API contracts
  - Frontend consumes API correctly
  - Database migrations run without errors
- [ ] **No breaking changes** to existing functionality (or properly documented)
- [ ] **Tested in Docker environment** (not just locally)

## Deployment Readiness

- [ ] **Environment variables documented** (in .env.example if new)
- [ ] **Database migrations created** (if schema changes)
- [ ] **Deployment instructions updated** (if deployment process changes)
- [ ] **Rollback plan documented** (for significant changes)

## User Acceptance

- [ ] **Tested by end user** or product owner (for user-facing features)
- [ ] **Meets acceptance criteria** defined in the Issue
- [ ] **No critical bugs** reported
- [ ] **User feedback incorporated** (if applicable)

## Cleanup

- [ ] **Debug code removed** (console.logs, print statements, etc.)
- [ ] **Commented-out code removed**
- [ ] **TODO comments addressed** or converted to Issues
- [ ] **Temporary files deleted**
- [ ] **Feature branch deleted** after merge

## Merge Criteria

- [ ] **Merged to develop branch** (not main)
- [ ] **PR description complete**:
  - What was implemented
  - Testing performed
  - Screenshots (if UI changes)
  - Related issues
- [ ] **GitHub Issue(s) closed** or updated

## Deployment (Phase 7 only)

For production deployment:

- [ ] **Deployed to staging environment** and tested
- [ ] **Smoke tests passed** in staging
- [ ] **Backup created** before deployment
- [ ] **Deployment successful** without errors
- [ ] **Post-deployment verification** completed
- [ ] **Monitoring and alerts** configured

---

## Quick Checklist Template

Copy this into your PR description:

```markdown
## Definition of Done Checklist

### Code Quality
- [ ] Code complete and follows style guide
- [ ] Type safety (type hints/TypeScript)
- [ ] Code is readable and well-organized

### Documentation
- [ ] Code documentation (docstrings/JSDoc)
- [ ] README/API docs updated

### Testing
- [ ] Unit tests written and passing
- [ ] Integration tests (if applicable)
- [ ] Coverage ≥ 80%
- [ ] Edge cases covered

### Security
- [ ] No vulnerabilities (SQL injection, XSS, etc.)
- [ ] Input validation implemented
- [ ] No hardcoded secrets

### Accessibility (Frontend)
- [ ] WCAG 2.1 AA compliant
- [ ] Keyboard navigation works
- [ ] Screen reader compatible

### Performance
- [ ] API < 200ms, Page load < 2s
- [ ] No N+1 queries
- [ ] Images optimized

### Code Review
- [ ] Reviewed and approved
- [ ] Comments addressed

### CI/CD
- [ ] All CI checks passing
- [ ] No merge conflicts

### Integration
- [ ] Integrates with other components
- [ ] Tested in Docker environment

### Cleanup
- [ ] Debug code removed
- [ ] Feature branch will be deleted after merge
```

---

*This Definition of Done ensures high-quality, production-ready code at every stage.*

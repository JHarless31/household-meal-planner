# Testing Documentation

Comprehensive testing guide for the Meal Planning Application.

## Table of Contents

- [Overview](#overview)
- [Testing Strategy](#testing-strategy)
- [Backend Testing](#backend-testing)
- [Frontend Testing](#frontend-testing)
- [End-to-End Testing](#end-to-end-testing)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Writing New Tests](#writing-new-tests)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

## Overview

This application uses a comprehensive testing strategy with multiple layers:

- **Unit Tests**: Test individual components and services in isolation
- **Integration Tests**: Test API endpoints and service interactions
- **End-to-End Tests**: Test complete user workflows
- **Performance Tests**: Ensure application meets performance requirements
- **Security Tests**: Validate security controls and authentication

### Coverage Targets

- **Backend**: 80%+ overall, 90%+ for critical services
- **Frontend**: 70%+ overall, 80%+ for components
- **Integration**: All critical user flows
- **E2E**: All major features

## Testing Strategy

### Test Pyramid

```
         /\
        /E2E\           (Few, slow, expensive)
       /------\
      /  Int.  \        (More, medium speed)
     /----------\
    /    Unit    \      (Many, fast, cheap)
   /--------------\
```

### Critical Areas (90%+ Coverage Required)

- Authentication and authorization
- Recipe versioning logic
- Inventory auto-deduction
- Menu plan suggestion algorithm
- Notification generation
- Shopping list calculation
- Rating and favorites logic

## Backend Testing

### Technology Stack

- **pytest**: Test framework
- **pytest-cov**: Coverage reporting
- **pytest-asyncio**: Async test support
- **httpx**: HTTP client for API testing
- **factory-boy**: Test data factories
- **faker**: Realistic test data

### Directory Structure

```
backend/tests/
├── conftest.py                  # Fixtures and configuration
├── test_auth.py                 # Authentication tests
├── test_recipe_service.py       # Recipe service tests
├── test_inventory_service.py    # Inventory service tests
├── test_rating_service.py       # Rating service tests
├── test_menu_plan_service.py    # Menu plan service tests
├── test_shopping_list_service.py # Shopping list tests
├── test_notification_service.py # Notification tests
├── test_recipe_suggestions.py   # Suggestion algorithm tests
├── integration/
│   └── test_api_endpoints.py    # Integration tests
├── performance/
│   └── test_query_performance.py # Performance tests
└── security/
    └── test_auth_security.py     # Security tests
```

### Running Backend Tests

```bash
# Install test dependencies
cd backend
pip install -r requirements-test.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_recipe_service.py

# Run specific test
pytest tests/test_recipe_service.py::TestRecipeService::test_create_recipe_success

# Run tests by marker
pytest -m unit           # Only unit tests
pytest -m integration    # Only integration tests
pytest -m performance    # Only performance tests
pytest -m security       # Only security tests

# Run tests in parallel
pytest -n auto

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

### Test Fixtures

Available fixtures in `conftest.py`:

**Database Fixtures:**
- `db`: Test database session (SQLite in-memory)
- `client`: FastAPI test client

**User Fixtures:**
- `test_user`: Standard user account
- `admin_user`: Admin user account
- `inactive_user`: Inactive user account
- `auth_headers`: Authentication headers for test_user
- `admin_headers`: Authentication headers for admin_user

**Recipe Fixtures:**
- `test_recipe`: Single recipe with version and ingredients
- `test_recipes`: Collection of 5 test recipes

**Inventory Fixtures:**
- `test_inventory_item`: Single inventory item
- `test_inventory_items`: Collection of inventory items

**Other Fixtures:**
- `test_rating`: Sample rating
- `test_menu_plan`: Sample menu plan
- `test_planned_meal`: Sample planned meal
- `test_notification`: Sample notification

### Example Unit Test

```python
import pytest
from src.services.recipe_service import RecipeService
from src.schemas.recipe import RecipeCreate, IngredientInput

@pytest.mark.unit
def test_create_recipe_success(db, test_user):
    """Test successful recipe creation"""
    recipe_data = RecipeCreate(
        title="New Recipe",
        description="Test description",
        prep_time_minutes=10,
        cook_time_minutes=20,
        servings=4,
        difficulty="easy",
        instructions="Test instructions",
        ingredients=[
            IngredientInput(
                name="ingredient1",
                quantity=100,
                unit="g",
                category="other"
            )
        ],
        tags=["tag1"]
    )

    recipe = RecipeService.create_recipe(db, recipe_data, test_user.id)

    assert recipe.id is not None
    assert recipe.title == "New Recipe"
    assert recipe.current_version == 1
```

## Frontend Testing

### Technology Stack

- **Jest**: Test framework
- **React Testing Library**: Component testing
- **@testing-library/user-event**: User interaction simulation
- **Playwright**: End-to-end testing
- **@axe-core/playwright**: Accessibility testing

### Running Frontend Tests

```bash
cd frontend

# Install dependencies
npm install

# Run unit tests
npm test

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e

# Run E2E tests in UI mode
npm run test:e2e:ui

# Run accessibility tests
npm run test:a11y
```

### Example Component Test

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '@/components/common/Button';

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click Me</Button>);

    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click Me</Button>);

    fireEvent.click(screen.getByText('Click Me'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('shows loading state', () => {
    render(<Button loading>Click Me</Button>);

    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

## End-to-End Testing

### Playwright Configuration

E2E tests are located in `frontend/e2e/`:

```
frontend/e2e/
├── auth.spec.ts           # Authentication flows
├── recipes.spec.ts        # Recipe management
├── menu-planning.spec.ts  # Menu planning
├── inventory.spec.ts      # Inventory management
├── admin.spec.ts          # Admin features
├── accessibility.spec.ts  # Accessibility checks
└── performance.spec.ts    # Performance metrics
```

### Example E2E Test

```typescript
import { test, expect } from '@playwright/test';

test.describe('Recipe Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('[name="username"]', 'testuser');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
  });

  test('should create new recipe', async ({ page }) => {
    await page.goto('/recipes/new');

    // Fill form
    await page.fill('[name="title"]', 'New E2E Recipe');
    await page.fill('[name="description"]', 'Test description');
    await page.selectOption('[name="difficulty"]', 'easy');

    // Submit
    await page.click('button[type="submit"]');

    // Verify success
    await expect(page).toHaveURL(/\/recipes\/[a-f0-9-]+$/);
    await expect(page.locator('h1')).toContainText('New E2E Recipe');
  });
});
```

## Test Coverage

### Viewing Coverage Reports

After running tests with coverage:

```bash
# Backend
cd backend
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Frontend
cd frontend
npm run test:coverage
open coverage/index.html
```

### Coverage Thresholds

Configuration in `backend/.coveragerc` and `frontend/jest.config.js`:

- **Minimum coverage**: 80% for backend, 70% for frontend
- **Critical services**: 90%+ required
- **CI/CD**: Fails if below threshold

## Writing New Tests

### Best Practices

1. **Follow AAA Pattern**: Arrange, Act, Assert
   ```python
   def test_example(db, test_user):
       # Arrange
       data = RecipeCreate(...)

       # Act
       result = RecipeService.create_recipe(db, data, test_user.id)

       # Assert
       assert result.id is not None
   ```

2. **Use Descriptive Names**: Test name should describe what it tests
   ```python
   def test_create_recipe_with_missing_title_returns_validation_error(db, test_user):
       ...
   ```

3. **Test One Thing**: Each test should verify one behavior
   ```python
   # Good
   def test_create_recipe_success(db, test_user):
       ...

   def test_create_recipe_missing_title_fails(db, test_user):
       ...

   # Bad
   def test_create_recipe(db, test_user):
       # Tests multiple scenarios
   ```

4. **Use Fixtures**: Reuse test data via fixtures
   ```python
   @pytest.fixture
   def sample_recipe_data():
       return RecipeCreate(
           title="Sample Recipe",
           ...
       )

   def test_something(db, test_user, sample_recipe_data):
       ...
   ```

5. **Mock External Dependencies**: Don't call real external services
   ```python
   def test_scrape_recipe(db, mocker):
       mock_response = mocker.patch('requests.get')
       mock_response.return_value.json.return_value = {...}
       ...
   ```

6. **Test Edge Cases**: Don't just test happy paths
   - Null values
   - Empty lists
   - Invalid inputs
   - Unauthorized access
   - Race conditions

### Adding New Test Files

1. Create test file in appropriate directory
2. Import necessary fixtures from `conftest.py`
3. Use `@pytest.mark.unit` or appropriate marker
4. Follow naming convention: `test_<module>_<feature>.py`

```python
"""
Unit Tests for New Service
Description of what this tests
"""

import pytest
from src.services.new_service import NewService

@pytest.mark.unit
class TestNewService:
    """Test cases for new service"""

    def test_method_success(self, db, test_user):
        """Test successful operation"""
        # Arrange
        ...

        # Act
        ...

        # Assert
        ...
```

## CI/CD Integration

### GitHub Actions Workflows

Tests run automatically on:
- Push to any branch
- Pull requests
- Scheduled daily runs

### Workflow Files

```
.github/workflows/
├── backend-tests.yml    # Backend tests + coverage
├── frontend-tests.yml   # Frontend tests + coverage
└── e2e-tests.yml       # End-to-end tests
```

### Status Checks

Pull requests require:
- All tests passing
- Coverage thresholds met
- No security vulnerabilities
- Linting passed

### Local Pre-commit

Setup pre-commit hooks:

```bash
# Backend
cd backend
pip install pre-commit
pre-commit install

# Frontend
cd frontend
npm run prepare
```

## Troubleshooting

### Common Issues

**Issue: Tests fail with "Database is locked"**
```bash
# Solution: Use in-memory database or check for leaked connections
# Ensure all fixtures properly close database sessions
```

**Issue: "ModuleNotFoundError" in tests**
```bash
# Solution: Ensure PYTHONPATH includes src directory
export PYTHONPATH="${PYTHONPATH}:${PWD}/backend"
```

**Issue: Frontend tests timeout**
```bash
# Solution: Increase timeout in jest.config.js
testTimeout: 10000
```

**Issue: E2E tests flaky**
```bash
# Solution: Add explicit waits
await page.waitForLoadState('networkidle');
await page.waitForSelector('[data-testid="element"]');
```

**Issue: Coverage not including all files**
```bash
# Solution: Check .coveragerc or jest.config.js
# Ensure all source directories are included
```

### Debug Mode

Run tests in debug mode:

```bash
# Backend
pytest --pdb  # Drop into debugger on failure

# Frontend
npm test -- --watch --verbose

# E2E
npm run test:e2e:debug
```

### Logs and Output

Enable detailed logging:

```bash
# Backend
pytest -v --log-cli-level=DEBUG

# Frontend
DEBUG=* npm test

# E2E
DEBUG=pw:api npm run test:e2e
```

## Performance Testing

### Load Testing

Use pytest-benchmark for performance tests:

```python
@pytest.mark.performance
def test_recipe_list_performance(db, test_recipes, benchmark):
    """Test recipe list query performance"""
    def run_query():
        return RecipeService.list_recipes(db, user_id, limit=100)

    result = benchmark(run_query)

    # Should complete in < 500ms
    assert benchmark.stats.mean < 0.5
```

### Performance Thresholds

- Recipe list query: < 500ms for 1000 recipes
- Suggestion algorithm: < 100ms
- Shopping list generation: < 200ms
- Admin statistics: < 300ms

## Security Testing

### Security Checklist

- [x] SQL injection prevention
- [x] XSS prevention
- [x] CSRF protection
- [x] Password complexity requirements
- [x] Session expiration
- [x] Rate limiting
- [x] JWT token validation
- [x] Authorization checks
- [x] Input validation
- [x] HTTPS enforcement

### Running Security Tests

```bash
pytest -m security

# With security scanner
bandit -r backend/src

# Dependency vulnerability check
safety check
```

## Continuous Improvement

### Monitoring Test Health

- Review flaky tests weekly
- Maintain test execution time < 5 minutes
- Keep coverage above thresholds
- Update tests when features change
- Remove obsolete tests

### Test Metrics to Track

- **Test count**: Total number of tests
- **Coverage**: Percentage of code covered
- **Execution time**: Time to run full suite
- **Flakiness rate**: Percentage of flaky tests
- **Failure rate**: Percentage of failing tests

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [React Testing Library](https://testing-library.com/react)
- [Playwright Documentation](https://playwright.dev/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

## Support

For testing questions or issues:
1. Check this documentation
2. Review existing test examples
3. Ask in team chat
4. Create issue in repository

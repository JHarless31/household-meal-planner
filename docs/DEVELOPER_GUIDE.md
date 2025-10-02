# Developer Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure](#project-structure)
4. [Backend Development](#backend-development)
5. [Frontend Development](#frontend-development)
6. [Key Features Implementation](#key-features-implementation)
7. [Adding New Features](#adding-new-features)
8. [Code Style and Standards](#code-style-and-standards)
9. [Testing](#testing)
10. [Debugging](#debugging)
11. [Contributing](#contributing)

---

## Introduction

### Project Overview

The Household Meal Planning System is a full-stack web application built to help families manage recipes, track inventory, plan menus, and generate shopping lists. The system is designed for local deployment on a home server or virtual machine.

### Technology Stack

**Backend:**
- **Framework**: FastAPI (Python 3.12)
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL 15
- **Authentication**: JWT + bcrypt
- **Web Scraping**: BeautifulSoup4, recipe-scrapers
- **Testing**: pytest, pytest-cov, httpx

**Frontend:**
- **Framework**: Next.js 14 (App Router)
- **UI Library**: React 18
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **State Management**: React Context + Zustand
- **Forms**: React Hook Form
- **API Client**: Axios + TanStack Query
- **Testing**: Jest, React Testing Library, Playwright

**Database:**
- **RDBMS**: PostgreSQL 15
- **Multi-schema design**: `shared`, `meal_planning`, future schemas

**Infrastructure:**
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **CI/CD**: GitHub Actions
- **Deployment**: Proxmox VM (Ubuntu Server 22.04)

### Architecture Overview

```
┌──────────────────────────────────────────────────────┐
│                    Client Browser                     │
└───────────────────────┬──────────────────────────────┘
                        │ HTTPS
                        ▼
┌──────────────────────────────────────────────────────┐
│              Nginx Reverse Proxy                      │
│  - Routes /api/* → Backend                            │
│  - Routes /* → Frontend                               │
└──────────────┬───────────────────────┬───────────────┘
               │                        │
               ▼                        ▼
┌──────────────────────┐    ┌─────────────────────────┐
│   Backend (FastAPI)  │    │  Frontend (Next.js)     │
│   - REST API         │    │  - React UI             │
│   - Business Logic   │    │  - SSR/CSR              │
│   - Authentication   │    │  - API Integration      │
└──────────┬───────────┘    └─────────────────────────┘
           │
           ▼
┌──────────────────────┐
│  PostgreSQL Database │
│  - Multi-schema      │
│  - Relational data   │
└──────────────────────┘
```

**Key Patterns:**
- **API Route → Service → Model**: Clean separation of concerns
- **Version control**: Recipes maintain full version history
- **Soft deletes**: Data is marked deleted, not removed
- **Auto-deduction**: Inventory automatically updated when meals cooked

### Multi-Agent Development Approach

This project was built using a multi-agent development methodology with 6 specialized AI agents:

1. **Database & Architecture Agent**: Schema design, API contracts
2. **Backend API Agent**: FastAPI implementation, business logic
3. **Frontend UI Agent**: React/Next.js, accessibility
4. **DevOps & Infrastructure Agent**: Docker, deployment, CI/CD
5. **Testing & QA Agent**: Test suites, quality assurance
6. **Documentation Agent**: User/admin/developer documentation

See [AGENT_COORDINATION.md](AGENT_COORDINATION.md) for details on the multi-agent workflow.

---

## Development Environment Setup

### Prerequisites

Before you begin, ensure you have the following installed:

**Required:**
- **Python 3.11+** (preferably 3.12)
- **Node.js 18+** (LTS version recommended)
- **PostgreSQL 15+**
- **Git** (for version control)

**Optional but Recommended:**
- **Docker** and **Docker Compose** (for containerized development)
- **pyenv** or **conda** (Python version management)
- **nvm** (Node version management)
- **PostgreSQL client tools** (psql, pgAdmin)

### Cloning the Repository

```bash
# Clone the repository
git clone <repository-url>
cd meal-planning-system

# Check the directory structure
ls -la
```

You should see:
```
meal-planning-system/
├── backend/           # FastAPI backend
├── frontend/          # Next.js frontend
├── database/          # Database schemas
├── docs/              # Documentation
├── infrastructure/    # Docker configs, deployment scripts
├── tests/             # End-to-end tests
├── .env.example       # Environment variables template
├── README.md
└── ...
```

### Backend Setup

#### 1. Create a Virtual Environment

```bash
cd backend

# Using venv (built-in)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n meal-planning python=3.12
conda activate meal-planning
```

#### 2. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development/testing dependencies
pip install -r requirements-test.txt
```

**Key Dependencies:**
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `sqlalchemy`: ORM
- `psycopg2-binary`: PostgreSQL driver
- `python-jose`: JWT handling
- `passlib[bcrypt]`: Password hashing
- `beautifulsoup4`, `recipe-scrapers`: Web scraping
- `pytest`, `pytest-cov`: Testing

#### 3. Set Up the Database

**Option A: Local PostgreSQL Installation**

```bash
# Install PostgreSQL 15 (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql-15 postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql

# In psql:
CREATE DATABASE household_db;
CREATE USER meal_planner WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE household_db TO meal_planner;
\q
```

**Option B: Docker PostgreSQL**

```bash
# Run PostgreSQL in Docker
docker run -d \
  --name meal-planning-db \
  -e POSTGRES_DB=household_db \
  -e POSTGRES_USER=meal_planner \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  postgres:15
```

#### 4. Initialize Database Schema

```bash
# From the project root
psql -U meal_planner -d household_db -f database/schemas/01_shared_schema.sql
psql -U meal_planner -d household_db -f database/schemas/02_meal_planning_schema.sql
psql -U meal_planner -d household_db -f database/seed_data.sql
```

Or using the initialization script:

```bash
cd database
./init_database.sh
```

#### 5. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

**Required environment variables:**

```bash
# Database
DATABASE_URL=postgresql://meal_planner:your_password@localhost:5432/household_db

# Authentication
SECRET_KEY=your-secret-key-here  # Generate with: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Application
APP_NAME=Household Meal Planning
APP_VERSION=1.0.0
DEBUG=True  # Set to False in production

# Recipe Scraper
SCRAPER_RATE_LIMIT_SECONDS=5
SCRAPER_USER_AGENT=MealPlanningApp/1.0
```

#### 6. Run the Backend Server

```bash
# From backend directory
cd backend

# Development mode (auto-reload)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using the provided script
./run_dev.sh
```

Backend should be running at: `http://localhost:8000`

**Verify it's working:**
```bash
curl http://localhost:8000/api/health
# Should return: {"status":"healthy"}
```

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

#### 1. Install Dependencies

```bash
cd frontend

# Install all dependencies
npm install

# Or using yarn
yarn install
```

**Key Dependencies:**
- `next`: Next.js framework
- `react`, `react-dom`: React library
- `typescript`: TypeScript compiler
- `tailwindcss`: Utility-first CSS
- `axios`: HTTP client
- `@tanstack/react-query`: Data fetching/caching
- `zustand`: State management
- `react-hook-form`: Form handling
- `@dnd-kit/*`: Drag-and-drop
- `recharts`: Charts
- `date-fns`: Date utilities

#### 2. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env.local

# Edit .env.local
nano .env.local
```

**Required environment variables:**

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Application
NEXT_PUBLIC_APP_NAME=Meal Planning System
NEXT_PUBLIC_APP_VERSION=1.0.0
```

#### 3. Run the Development Server

```bash
# Development mode (hot reload)
npm run dev

# Or using yarn
yarn dev
```

Frontend should be running at: `http://localhost:3000`

**Verify it's working:**
- Open `http://localhost:3000` in your browser
- You should see the login page

#### 4. Type Checking

```bash
# Run TypeScript type checking
npm run type-check

# Watch mode
npm run type-check -- --watch
```

### Docker Setup (Full Stack)

For a complete containerized environment:

#### 1. Ensure Docker is Installed

```bash
docker --version
docker-compose --version
```

#### 2. Configure Environment

```bash
# Copy example file
cp .env.example .env

# Edit with Docker-specific settings
nano .env
```

**Docker environment:**

```bash
DATABASE_URL=postgresql://meal_planner:password@postgres:5432/household_db
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

#### 3. Build and Run

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

**Services:**
- PostgreSQL: `localhost:5432`
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

#### 4. Initialize Database

```bash
# Execute init script inside container
docker-compose exec backend python scripts/init_db.py

# Or manually
docker-compose exec postgres psql -U meal_planner -d household_db -f /docker-entrypoint-initdb.d/01_shared_schema.sql
```

### Creating an Admin User

After setting up the database:

```bash
# Using the provided script
cd backend
python scripts/create_admin.py

# Or manually via psql
psql -U meal_planner -d household_db
```

```sql
-- In psql
INSERT INTO shared.users (id, username, email, password_hash, role, is_active)
VALUES (
  gen_random_uuid(),
  'admin',
  'admin@example.com',
  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzJGOEL8bW',  -- password: "admin123"
  'admin',
  true
);
```

**Default admin credentials:**
- Username: `admin`
- Password: `admin123`

**Important:** Change the admin password immediately after first login!

---

## Project Structure

### Repository Organization

```
meal-planning-system/
├── backend/                    # Backend application
│   ├── src/                    # Source code
│   │   ├── api/                # API routes
│   │   ├── core/               # Core functionality (database, security)
│   │   ├── models/             # SQLAlchemy models
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/           # Business logic
│   │   ├── scrapers/           # Web scraping utilities
│   │   └── utils/              # Helper functions
│   ├── tests/                  # Backend tests
│   ├── requirements.txt        # Production dependencies
│   ├── requirements-test.txt   # Test dependencies
│   ├── pytest.ini              # Pytest configuration
│   └── Dockerfile              # Backend Docker image
│
├── frontend/                   # Frontend application
│   ├── src/                    # Source code
│   │   ├── app/                # Next.js pages (App Router)
│   │   │   ├── (main)/         # Authenticated pages
│   │   │   ├── auth/           # Authentication pages
│   │   │   └── layout.tsx      # Root layout
│   │   ├── components/         # React components
│   │   │   ├── common/         # Shared components
│   │   │   ├── layout/         # Layout components
│   │   │   ├── recipes/        # Recipe components
│   │   │   └── ...
│   │   ├── contexts/           # React contexts
│   │   ├── lib/                # Utilities and API clients
│   │   │   ├── api/            # API client functions
│   │   │   └── utils/          # Helper functions
│   │   └── types/              # TypeScript type definitions
│   ├── public/                 # Static assets
│   ├── package.json            # Dependencies and scripts
│   ├── tsconfig.json           # TypeScript configuration
│   ├── tailwind.config.js      # Tailwind configuration
│   ├── next.config.js          # Next.js configuration
│   └── Dockerfile              # Frontend Docker image
│
├── database/                   # Database files
│   ├── schemas/                # SQL schema files
│   │   ├── 01_shared_schema.sql
│   │   └── 02_meal_planning_schema.sql
│   ├── migrations/             # Database migrations (if using Alembic)
│   ├── seed_data.sql           # Initial data
│   └── init_database.sh        # Initialization script
│
├── docs/                       # Documentation
│   ├── USER_GUIDE.md
│   ├── DEVELOPER_GUIDE.md      # This file
│   ├── API_DOCUMENTATION.md
│   ├── ADMIN_GUIDE.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── ARCHITECTURE.md
│   ├── DATABASE_SCHEMA.md
│   ├── API_SPEC.yaml
│   ├── TESTING.md
│   └── ...
│
├── infrastructure/             # Infrastructure files
│   ├── docker-compose.yml      # Docker Compose configuration
│   ├── nginx/                  # Nginx configuration
│   │   └── nginx.conf
│   ├── proxmox-setup.md        # VM deployment guide
│   └── backup-script.sh        # Backup automation
│
├── tests/                      # End-to-end tests
│   └── e2e/                    # Playwright tests
│
├── .github/                    # GitHub configuration
│   └── workflows/              # CI/CD workflows
│       ├── backend-tests.yml
│       ├── frontend-tests.yml
│       └── deploy.yml
│
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── README.md                   # Project README
├── CONTRIBUTING.md             # Contribution guidelines
├── CHANGELOG.md                # Version history
└── LICENSE                     # License file
```

### Backend Directory Structure

```
backend/src/
├── api/                        # API route handlers
│   ├── __init__.py
│   ├── auth.py                 # Authentication endpoints
│   ├── recipes.py              # Recipe CRUD + scraping
│   ├── inventory.py            # Inventory management
│   ├── ratings.py              # Recipe ratings
│   ├── menu_plans.py           # Menu planning
│   ├── shopping_lists.py       # Shopping list generation
│   ├── notifications.py        # Notification endpoints
│   └── admin.py                # Admin endpoints
│
├── core/                       # Core functionality
│   ├── __init__.py
│   ├── config.py               # Configuration management
│   ├── database.py             # Database connection and session
│   ├── security.py             # Authentication and authorization
│   └── dependencies.py         # FastAPI dependencies
│
├── models/                     # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── user.py                 # User model
│   ├── recipe.py               # Recipe, RecipeVersion, Ingredient, RecipeTag
│   ├── inventory.py            # InventoryItem, InventoryHistory
│   ├── rating.py               # Rating model
│   ├── menu_plan.py            # MenuPlan, PlannedMeal
│   ├── notification.py         # Notification model
│   └── app_settings.py         # AppSettings model
│
├── schemas/                    # Pydantic schemas (validation, serialization)
│   ├── __init__.py
│   ├── user.py                 # UserCreate, UserResponse, etc.
│   ├── recipe.py               # RecipeCreate, RecipeUpdate, RecipeResponse, etc.
│   ├── inventory.py            # InventoryCreate, InventoryUpdate, etc.
│   ├── rating.py               # RatingCreate, RatingResponse, etc.
│   ├── menu_plan.py            # MenuPlanCreate, MenuPlanResponse, etc.
│   ├── notification.py         # NotificationCreate, NotificationResponse, etc.
│   └── common.py               # Common schemas (pagination, etc.)
│
├── services/                   # Business logic layer
│   ├── __init__.py
│   ├── recipe_service.py       # Recipe CRUD, versioning
│   ├── inventory_service.py    # Inventory management, auto-deduction
│   ├── rating_service.py       # Rating calculations, favorites
│   ├── menu_plan_service.py    # Menu planning, copy, auto-generate
│   ├── shopping_list_service.py # Shopping list generation
│   ├── notification_service.py  # Notification generation
│   ├── recipe_suggestions.py    # Suggestion algorithms
│   └── scraper.py              # Recipe web scraping
│
├── scrapers/                   # Web scraping utilities
│   ├── __init__.py
│   └── recipe_scraper.py       # Recipe extraction logic
│
├── utils/                      # Helper functions
│   ├── __init__.py
│   ├── date_utils.py           # Date manipulation
│   └── text_utils.py           # Text processing
│
└── main.py                     # Application entry point
```

### Frontend Directory Structure

```
frontend/src/
├── app/                        # Next.js App Router pages
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home page (redirects to dashboard)
│   ├── (main)/                 # Protected routes (authenticated)
│   │   ├── layout.tsx          # Main layout with navigation
│   │   ├── page.tsx            # Dashboard
│   │   ├── recipes/
│   │   │   ├── page.tsx        # Recipe list
│   │   │   ├── new/
│   │   │   │   └── page.tsx    # New recipe form
│   │   │   └── [id]/
│   │   │       └── page.tsx    # Recipe detail
│   │   ├── inventory/
│   │   │   ├── page.tsx        # Inventory list
│   │   │   └── new/
│   │   │       └── page.tsx    # New inventory item
│   │   ├── menu-plans/
│   │   │   ├── page.tsx        # Menu plan list
│   │   │   └── new/
│   │   │       └── page.tsx    # New menu plan
│   │   └── admin/
│   │       ├── dashboard/
│   │       │   └── page.tsx    # Admin dashboard
│   │       ├── users/
│   │       │   └── page.tsx    # User management
│   │       └── settings/
│   │           └── page.tsx    # System settings
│   └── auth/                   # Public routes (unauthenticated)
│       ├── login/
│       │   └── page.tsx        # Login page
│       └── register/
│           └── page.tsx        # Registration page
│
├── components/                 # React components
│   ├── common/                 # Shared components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Select.tsx
│   │   ├── Modal.tsx
│   │   ├── Toast.tsx
│   │   ├── LoadingSpinner.tsx
│   │   ├── ErrorMessage.tsx
│   │   ├── EmptyState.tsx
│   │   ├── ConfirmDialog.tsx
│   │   ├── ProtectedRoute.tsx
│   │   └── NotificationBell.tsx
│   ├── layout/                 # Layout components
│   │   ├── Header.tsx
│   │   ├── Navigation.tsx
│   │   └── Footer.tsx
│   ├── recipes/                # Recipe-specific components
│   │   ├── RecipeCard.tsx
│   │   ├── RecipeForm.tsx
│   │   ├── RecipeList.tsx
│   │   ├── RecipeSuggestions.tsx
│   │   └── RecipeVersionHistory.tsx
│   ├── inventory/              # Inventory components
│   │   ├── InventoryTable.tsx
│   │   └── InventoryForm.tsx
│   ├── menu-plans/             # Menu planning components
│   │   ├── MenuPlanCalendar.tsx
│   │   └── MenuPlanForm.tsx
│   └── ratings/                # Rating components
│       └── RatingWidget.tsx
│
├── contexts/                   # React Context providers
│   ├── AuthContext.tsx         # Authentication state
│   └── ToastContext.tsx        # Toast notifications
│
├── lib/                        # Utilities and libraries
│   ├── api/                    # API client functions
│   │   ├── client.ts           # Axios instance
│   │   ├── auth.ts             # Auth API calls
│   │   ├── recipes.ts          # Recipe API calls
│   │   ├── inventory.ts        # Inventory API calls
│   │   ├── ratings.ts          # Rating API calls
│   │   ├── menuPlans.ts        # Menu plan API calls
│   │   ├── notifications.ts    # Notification API calls
│   │   └── admin.ts            # Admin API calls
│   └── utils/                  # Helper functions
│       ├── formatters.ts       # Data formatting
│       ├── validators.ts       # Form validation
│       └── constants.ts        # App constants
│
└── types/                      # TypeScript type definitions
    ├── index.ts                # Exported types
    ├── recipe.ts               # Recipe types
    ├── inventory.ts            # Inventory types
    ├── user.ts                 # User types
    ├── menuPlan.ts             # Menu plan types
    └── notification.ts         # Notification types
```

---

## Backend Development

### Architecture Patterns

The backend follows a **layered architecture**:

```
API Route → Service → Model → Database
```

**Layers:**

1. **API Route** (`/api/*.py`): HTTP request handling
   - Receive requests
   - Validate input (Pydantic schemas)
   - Call service methods
   - Return responses

2. **Service** (`/services/*.py`): Business logic
   - Implement business rules
   - Orchestrate operations
   - Manage transactions
   - Handle complex queries

3. **Model** (`/models/*.py`): Data models
   - Define database schema (SQLAlchemy ORM)
   - Represent database tables
   - Define relationships

4. **Database**: PostgreSQL storage

**Benefits:**
- Clear separation of concerns
- Testability (services can be tested independently)
- Maintainability (changes localized to appropriate layer)
- Reusability (services used by multiple routes)

### Database Models (SQLAlchemy)

Models are defined using SQLAlchemy ORM.

**Example: User Model**

```python
# backend/src/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import enum

from src.core.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    CHILD = "child"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "shared"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"
```

**Key Concepts:**

- **`__tablename__`**: Database table name
- **`__table_args__`**: Table-level options (schema, indexes, constraints)
- **Column types**: String, Integer, Boolean, DateTime, UUID, etc.
- **Constraints**: `nullable`, `unique`, `primary_key`, `default`
- **Indexes**: `index=True` for performance
- **Enums**: Type-safe choices (UserRole)
- **Relationships**: `relationship()` for foreign keys

**Multi-Schema Design:**

```python
# Shared schema
__table_args__ = {"schema": "shared"}

# Meal planning schema
__table_args__ = {"schema": "meal_planning"}
```

**Defining Relationships:**

```python
# One-to-Many: Recipe has many RecipeVersions
class Recipe(Base):
    __tablename__ = "recipes"
    __table_args__ = {"schema": "meal_planning"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # ... other columns

    # Relationship
    versions = relationship("RecipeVersion", back_populates="recipe")

class RecipeVersion(Base):
    __tablename__ = "recipe_versions"
    __table_args__ = {"schema": "meal_planning"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("meal_planning.recipes.id"))
    # ... other columns

    # Relationship
    recipe = relationship("Recipe", back_populates="versions")
```

**Creating New Models:**

1. Create file in `backend/src/models/`
2. Import Base from `src.core.database`
3. Define model class inheriting from `Base`
4. Define columns with appropriate types
5. Add relationships if needed
6. Import in `models/__init__.py`

### Pydantic Schemas

Pydantic schemas validate request data and serialize responses.

**Example: Recipe Schemas**

```python
# backend/src/schemas/recipe.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class IngredientBase(BaseModel):
    quantity: float = Field(..., gt=0)
    unit: str = Field(..., max_length=50)
    name: str = Field(..., max_length=200)
    notes: Optional[str] = None

class RecipeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    servings: int = Field(default=4, gt=0)
    prep_time_minutes: int = Field(..., ge=0)
    cook_time_minutes: int = Field(..., ge=0)
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")
    ingredients: List[IngredientBase]
    instructions: List[str]
    tags: Optional[List[str]] = []
    source_url: Optional[str] = None

    @validator('instructions')
    def validate_instructions(cls, v):
        if not v or len(v) == 0:
            raise ValueError('At least one instruction is required')
        return v

class RecipeResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    servings: int
    prep_time_minutes: int
    cook_time_minutes: int
    difficulty: str
    current_version: int
    times_cooked: int
    last_cooked_date: Optional[datetime]
    is_deleted: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Allows ORM model conversion
```

**Key Concepts:**

- **BaseModel**: All schemas inherit from `pydantic.BaseModel`
- **Field validation**: `Field(...)` with constraints (min_length, max_length, gt, ge, pattern)
- **Type hints**: Python type hints for validation
- **Optional fields**: `Optional[Type]` or `Type | None`
- **Custom validators**: `@validator` decorator
- **Config**: `from_attributes=True` for ORM compatibility

**Schema Types:**

- **Create schemas**: Data for creating new records (`RecipeCreate`)
- **Update schemas**: Data for updating records (`RecipeUpdate`)
- **Response schemas**: Data returned to client (`RecipeResponse`)
- **Base schemas**: Shared fields (`IngredientBase`)

**Creating New Schemas:**

1. Create file in `backend/src/schemas/`
2. Import `BaseModel` from pydantic
3. Define schema class with typed fields
4. Add validators if needed
5. Set `Config.from_attributes = True` for response schemas

### API Endpoints

API endpoints are defined using FastAPI decorators.

**Example: Recipe Endpoints**

```python
# backend/src/api/recipes.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.user import User
from src.schemas.recipe import RecipeCreate, RecipeUpdate, RecipeResponse
from src.services.recipe_service import RecipeService

router = APIRouter()

@router.get("", response_model=dict)
async def list_recipes(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    tags: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List recipes with pagination and filters.

    - **page**: Page number (starting from 1)
    - **limit**: Items per page (1-100)
    - **search**: Search in title/description
    - **tags**: Comma-separated tags
    - **difficulty**: Filter by difficulty (easy/medium/hard)
    """
    tags_list = tags.split(',') if tags else None
    recipes, total = RecipeService.list_recipes(
        db, current_user.id, page, limit, search, tags_list, difficulty
    )
    return {
        "recipes": [RecipeSummary.model_validate(r) for r in recipes],
        "pagination": {
            "page": page,
            "limit": limit,
            "total_pages": (total + limit - 1) // limit,
            "total_items": total
        }
    }

@router.post("", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe_data: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new recipe."""
    return RecipeService.create_recipe(db, recipe_data, current_user.id)

@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(
    recipe_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recipe by ID."""
    recipe = RecipeService.get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: UUID,
    recipe_data: RecipeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update recipe (creates new version)."""
    recipe = RecipeService.update_recipe(db, recipe_id, recipe_data, current_user.id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete recipe (soft delete)."""
    success = RecipeService.delete_recipe(db, recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe not found")
```

**Key Concepts:**

- **APIRouter**: Group related endpoints
- **Route decorators**: `@router.get`, `@router.post`, `@router.put`, `@router.delete`
- **Path parameters**: `{recipe_id}` in URL
- **Query parameters**: `Query(default, validation)`
- **Request body**: Pydantic schema as parameter
- **Response model**: `response_model=RecipeResponse`
- **Status codes**: `status_code=status.HTTP_201_CREATED`
- **Dependencies**: `Depends(get_db)`, `Depends(get_current_user)`
- **Error handling**: `raise HTTPException(status_code=404)`

**Dependency Injection:**

```python
# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication dependency
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Decode JWT token
    # Query user from database
    # Return user or raise HTTPException
    pass
```

**Creating New Endpoints:**

1. Create file in `backend/src/api/`
2. Create `APIRouter` instance
3. Define route handlers with decorators
4. Add dependencies (db, auth)
5. Call service methods
6. Handle errors with HTTPException
7. Register router in `main.py`

```python
# backend/src/main.py
from src.api import recipes, inventory, auth

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(recipes.router, prefix="/api/recipes", tags=["recipes"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["inventory"])
```

### Service Layer

Services contain business logic and orchestrate database operations.

**Example: Recipe Service**

```python
# backend/src/services/recipe_service.py
from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
from uuid import UUID

from src.models.recipe import Recipe, RecipeVersion, Ingredient, RecipeTag
from src.schemas.recipe import RecipeCreate, RecipeUpdate

class RecipeService:
    """Service for recipe management."""

    @staticmethod
    def create_recipe(
        db: Session,
        recipe_data: RecipeCreate,
        user_id: UUID
    ) -> Recipe:
        """
        Create a new recipe with initial version.

        Args:
            db: Database session
            recipe_data: Recipe data from request
            user_id: ID of user creating recipe

        Returns:
            Created Recipe instance
        """
        # Create recipe record
        recipe = Recipe(
            title=recipe_data.title,
            description=recipe_data.description,
            current_version=1,
            times_cooked=0,
            is_deleted=False,
            created_by_id=user_id
        )
        db.add(recipe)
        db.flush()  # Get recipe.id without committing

        # Create initial version
        version = RecipeVersion(
            recipe_id=recipe.id,
            version_number=1,
            servings=recipe_data.servings,
            prep_time_minutes=recipe_data.prep_time_minutes,
            cook_time_minutes=recipe_data.cook_time_minutes,
            difficulty=recipe_data.difficulty,
            instructions=recipe_data.instructions,
            source_url=recipe_data.source_url,
            created_by_id=user_id
        )
        db.add(version)
        db.flush()

        # Add ingredients to version
        for ing_data in recipe_data.ingredients:
            ingredient = Ingredient(
                recipe_version_id=version.id,
                quantity=ing_data.quantity,
                unit=ing_data.unit,
                name=ing_data.name,
                notes=ing_data.notes
            )
            db.add(ingredient)

        # Add tags
        for tag_name in recipe_data.tags or []:
            tag = RecipeTag(
                recipe_id=recipe.id,
                tag_name=tag_name.lower()
            )
            db.add(tag)

        db.commit()
        db.refresh(recipe)
        return recipe

    @staticmethod
    def get_recipe(db: Session, recipe_id: UUID) -> Optional[Recipe]:
        """Get recipe by ID."""
        return db.query(Recipe).filter(
            Recipe.id == recipe_id,
            Recipe.is_deleted == False
        ).first()

    @staticmethod
    def list_recipes(
        db: Session,
        user_id: UUID,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        tags: Optional[List[str]] = None,
        difficulty: Optional[str] = None
    ) -> Tuple[List[Recipe], int]:
        """
        List recipes with pagination and filters.

        Returns:
            Tuple of (recipes, total_count)
        """
        query = db.query(Recipe).filter(Recipe.is_deleted == False)

        # Search filter
        if search:
            query = query.filter(
                or_(
                    Recipe.title.ilike(f"%{search}%"),
                    Recipe.description.ilike(f"%{search}%")
                )
            )

        # Tag filter
        if tags:
            query = query.join(RecipeTag).filter(
                RecipeTag.tag_name.in_([t.lower() for t in tags])
            )

        # Difficulty filter
        if difficulty:
            query = query.join(RecipeVersion).filter(
                RecipeVersion.difficulty == difficulty
            )

        # Get total count
        total = query.count()

        # Pagination
        offset = (page - 1) * limit
        recipes = query.offset(offset).limit(limit).all()

        return recipes, total

    @staticmethod
    def update_recipe(
        db: Session,
        recipe_id: UUID,
        recipe_data: RecipeUpdate,
        user_id: UUID
    ) -> Optional[Recipe]:
        """
        Update recipe by creating a new version.

        This preserves version history.
        """
        recipe = RecipeService.get_recipe(db, recipe_id)
        if not recipe:
            return None

        # Increment version
        new_version_number = recipe.current_version + 1

        # Create new version
        version = RecipeVersion(
            recipe_id=recipe.id,
            version_number=new_version_number,
            servings=recipe_data.servings,
            prep_time_minutes=recipe_data.prep_time_minutes,
            cook_time_minutes=recipe_data.cook_time_minutes,
            difficulty=recipe_data.difficulty,
            instructions=recipe_data.instructions,
            source_url=recipe_data.source_url,
            created_by_id=user_id
        )
        db.add(version)
        db.flush()

        # Add ingredients
        for ing_data in recipe_data.ingredients:
            ingredient = Ingredient(
                recipe_version_id=version.id,
                quantity=ing_data.quantity,
                unit=ing_data.unit,
                name=ing_data.name,
                notes=ing_data.notes
            )
            db.add(ingredient)

        # Update recipe
        recipe.title = recipe_data.title
        recipe.description = recipe_data.description
        recipe.current_version = new_version_number

        db.commit()
        db.refresh(recipe)
        return recipe

    @staticmethod
    def delete_recipe(db: Session, recipe_id: UUID) -> bool:
        """Soft delete a recipe."""
        recipe = RecipeService.get_recipe(db, recipe_id)
        if not recipe:
            return False

        recipe.is_deleted = True
        db.commit()
        return True
```

**Key Concepts:**

- **Static methods**: Services are collections of static methods
- **Database session**: Always passed as first parameter
- **Transaction management**: `db.commit()` at the end
- **Error handling**: Return `None` or raise exceptions
- **Query building**: SQLAlchemy query API
- **Relationships**: Access via ORM (e.g., `recipe.versions`)

**Best Practices:**

- Keep business logic in services, not routes
- Use type hints for clarity
- Document complex methods
- Return consistent types
- Handle edge cases (not found, invalid data)
- Use transactions (commit/rollback)

**Creating New Services:**

1. Create file in `backend/src/services/`
2. Define service class
3. Add static methods for operations
4. Implement CRUD operations
5. Handle errors gracefully
6. Write tests for service methods

### Authentication & Authorization

The system uses JWT tokens for authentication.

**Authentication Flow:**

1. User logs in with username/password
2. Backend validates credentials
3. Backend generates JWT token
4. Token sent to client (httpOnly cookie or header)
5. Client includes token in subsequent requests
6. Backend validates token on protected routes

**Implementation:**

```python
# backend/src/core/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

from src.core.config import settings
from src.core.database import get_db
from src.models.user import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token.

    Raises HTTPException if token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to require admin role.

    Raises HTTPException if user is not an admin.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
```

**Login Endpoint:**

```python
# backend/src/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from src.core.database import get_db
from src.core.security import verify_password, create_access_token
from src.models.user import User
from src.core.config import settings

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with username and password.

    Returns JWT access token.
    """
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }
```

**Protected Routes:**

```python
# Require authentication
@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}

# Require admin role
@router.get("/admin-only")
async def admin_route(current_user: User = Depends(require_admin)):
    return {"message": "Admin access granted"}
```

### Database Migrations (Alembic)

*If using Alembic for migrations:*

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add notification table"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

**Migration file example:**

```python
# alembic/versions/xxx_add_notification_table.py
def upgrade():
    op.create_table(
        'notifications',
        sa.Column('id', postgresql.UUID(), nullable=False),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        # ...
        schema='shared'
    )

def downgrade():
    op.drop_table('notifications', schema='shared')
```

### Testing

Backend tests use pytest.

**Example Test:**

```python
# backend/tests/test_recipe_service.py
import pytest
from src.services.recipe_service import RecipeService
from src.schemas.recipe import RecipeCreate, IngredientBase

def test_create_recipe(db, test_user):
    """Test creating a recipe."""
    recipe_data = RecipeCreate(
        title="Test Recipe",
        description="A test recipe",
        servings=4,
        prep_time_minutes=15,
        cook_time_minutes=30,
        difficulty="easy",
        ingredients=[
            IngredientBase(quantity=2, unit="cups", name="flour"),
            IngredientBase(quantity=1, unit="cup", name="sugar")
        ],
        instructions=["Mix ingredients", "Bake at 350°F"],
        tags=["dessert", "easy"]
    )

    recipe = RecipeService.create_recipe(db, recipe_data, test_user.id)

    assert recipe.id is not None
    assert recipe.title == "Test Recipe"
    assert recipe.current_version == 1
    assert len(recipe.versions) == 1
    assert len(recipe.versions[0].ingredients) == 2

def test_get_recipe_not_found(db):
    """Test getting non-existent recipe."""
    from uuid import uuid4
    recipe = RecipeService.get_recipe(db, uuid4())
    assert recipe is None
```

**Running Tests:**

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_recipe_service.py

# Run specific test
pytest tests/test_recipe_service.py::test_create_recipe

# Run with verbose output
pytest -v
```

See [TESTING.md](TESTING.md) for comprehensive testing guide.

---

## Frontend Development

### Next.js 14 App Router

The frontend uses Next.js 14 with the App Router (not Pages Router).

**Key Concepts:**

- **File-based routing**: Files in `app/` directory define routes
- **Layouts**: `layout.tsx` wraps pages with common UI
- **Server Components**: Components render on server by default
- **Client Components**: Use `'use client'` directive for interactivity
- **Data fetching**: Use `fetch()` in Server Components or React Query in Client Components

**Route Structure:**

```
app/
├── layout.tsx              # Root layout (applies to all pages)
├── page.tsx                # Home page (/)
├── (main)/                 # Route group (doesn't affect URL)
│   ├── layout.tsx          # Layout for authenticated pages
│   ├── page.tsx            # Dashboard (/page redirects here)
│   ├── recipes/
│   │   ├── page.tsx        # /recipes
│   │   ├── new/
│   │   │   └── page.tsx    # /recipes/new
│   │   └── [id]/
│   │       └── page.tsx    # /recipes/:id (dynamic route)
│   └── admin/
│       └── ...
└── auth/
    ├── login/
    │   └── page.tsx        # /auth/login
    └── register/
        └── page.tsx        # /auth/register
```

**Example Page:**

```tsx
// frontend/src/app/(main)/recipes/page.tsx
'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import RecipeCard from '@/components/recipes/RecipeCard';
import { getRecipes } from '@/lib/api/recipes';

export default function RecipesPage() {
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);

  const { data, isLoading, error } = useQuery({
    queryKey: ['recipes', page, search],
    queryFn: () => getRecipes({ page, search })
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading recipes</div>;

  return (
    <div>
      <h1>Recipes</h1>
      <input
        type="text"
        placeholder="Search recipes..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <div className="grid grid-cols-3 gap-4">
        {data.recipes.map(recipe => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>
      {/* Pagination */}
    </div>
  );
}
```

**Server vs Client Components:**

```tsx
// Server Component (default)
// Can fetch data directly, no 'use client'
export default async function ServerPage() {
  const data = await fetch('https://api.example.com/data');
  return <div>{data.title}</div>;
}

// Client Component
// Needed for interactivity (onClick, useState, useEffect)
'use client';

import { useState } from 'react';

export default function ClientPage() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

**Layouts:**

```tsx
// frontend/src/app/(main)/layout.tsx
import Header from '@/components/layout/Header';
import Navigation from '@/components/layout/Navigation';

export default function MainLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <div>
      <Header />
      <Navigation />
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  );
}
```

### React Components

Components are reusable UI pieces.

**Example Component:**

```tsx
// frontend/src/components/common/Button.tsx
import React from 'react';
import clsx from 'clsx';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  className?: string;
}

export default function Button({
  children,
  onClick,
  type = 'button',
  variant = 'primary',
  size = 'md',
  disabled = false,
  className
}: ButtonProps) {
  const baseClasses = 'rounded font-medium transition-colors focus:outline-none focus:ring-2';

  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-400',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500'
  };

  const sizeClasses = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg'
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={clsx(
        baseClasses,
        variantClasses[variant],
        sizeClasses[size],
        disabled && 'opacity-50 cursor-not-allowed',
        className
      )}
    >
      {children}
    </button>
  );
}
```

**Component Patterns:**

- **Props interface**: Define prop types with TypeScript
- **Conditional rendering**: `{condition && <Component />}`
- **List rendering**: `{items.map(item => <Item key={item.id} />)}`
- **Event handling**: `onClick={handleClick}`
- **Styling**: Tailwind classes with `clsx` for conditional classes

### API Integration

API calls use Axios and TanStack Query.

**API Client Setup:**

```typescript
// frontend/src/lib/api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

**API Functions:**

```typescript
// frontend/src/lib/api/recipes.ts
import apiClient from './client';
import type { Recipe, RecipeCreate, RecipeUpdate } from '@/types/recipe';

export async function getRecipes(params: {
  page?: number;
  limit?: number;
  search?: string;
  tags?: string;
  difficulty?: string;
}) {
  const response = await apiClient.get('/recipes', { params });
  return response.data;
}

export async function getRecipe(id: string): Promise<Recipe> {
  const response = await apiClient.get(`/recipes/${id}`);
  return response.data;
}

export async function createRecipe(data: RecipeCreate): Promise<Recipe> {
  const response = await apiClient.post('/recipes', data);
  return response.data;
}

export async function updateRecipe(id: string, data: RecipeUpdate): Promise<Recipe> {
  const response = await apiClient.put(`/recipes/${id}`, data);
  return response.data;
}

export async function deleteRecipe(id: string): Promise<void> {
  await apiClient.delete(`/recipes/${id}`);
}
```

**Using React Query:**

```tsx
// In a component
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getRecipes, createRecipe } from '@/lib/api/recipes';

function RecipesPage() {
  const queryClient = useQueryClient();

  // Fetch data
  const { data, isLoading, error } = useQuery({
    queryKey: ['recipes'],
    queryFn: getRecipes
  });

  // Mutate data
  const createMutation = useMutation({
    mutationFn: createRecipe,
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['recipes'] });
    }
  });

  const handleCreate = (data: RecipeCreate) => {
    createMutation.mutate(data);
  };

  // ...
}
```

### State Management

**AuthContext:**

```tsx
// frontend/src/contexts/AuthContext.tsx
'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { login as apiLogin, logout as apiLogout, getCurrentUser } from '@/lib/api/auth';
import type { User } from '@/types/user';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('access_token');
    if (token) {
      getCurrentUser()
        .then(setUser)
        .catch(() => localStorage.removeItem('access_token'))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (username: string, password: string) => {
    const response = await apiLogin(username, password);
    localStorage.setItem('access_token', response.access_token);
    setUser(response.user);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    apiLogout();
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

**Using Context:**

```tsx
import { useAuth } from '@/contexts/AuthContext';

function ProfilePage() {
  const { user, logout } = useAuth();

  return (
    <div>
      <p>Welcome, {user?.username}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

### Styling with Tailwind

Tailwind CSS is a utility-first CSS framework.

**Common Patterns:**

```tsx
// Layout
<div className="container mx-auto px-4 py-8">
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {/* Grid items */}
  </div>
</div>

// Flexbox
<div className="flex items-center justify-between">
  <h1 className="text-2xl font-bold">Title</h1>
  <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
    Action
  </button>
</div>

// Responsive design
<div className="text-sm md:text-base lg:text-lg">
  Responsive text
</div>

// Conditional classes
<div className={clsx(
  'px-4 py-2 rounded',
  isActive ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800'
)}>
  {/* Content */}
</div>
```

**Tailwind Config:**

```javascript
// frontend/tailwind.config.js
module.exports = {
  content: [
    './src/app/**/*.{js,ts,jsx,tsx}',
    './src/components/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#6B7280'
      }
    }
  },
  plugins: []
};
```

### Forms and Validation

Forms use React Hook Form for validation.

**Example Form:**

```tsx
import { useForm } from 'react-hook-form';
import Button from '@/components/common/Button';
import Input from '@/components/common/Input';

interface LoginFormData {
  username: string;
  password: string;
}

export default function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>();

  const onSubmit = (data: LoginFormData) => {
    console.log(data);
    // Call login API
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="username">Username</label>
        <Input
          id="username"
          {...register('username', {
            required: 'Username is required',
            minLength: { value: 3, message: 'Minimum 3 characters' }
          })}
        />
        {errors.username && (
          <p className="text-red-600 text-sm">{errors.username.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <Input
          id="password"
          type="password"
          {...register('password', {
            required: 'Password is required',
            minLength: { value: 8, message: 'Minimum 8 characters' }
          })}
        />
        {errors.password && (
          <p className="text-red-600 text-sm">{errors.password.message}</p>
        )}
      </div>

      <Button type="submit">Login</Button>
    </form>
  );
}
```

### TypeScript

TypeScript provides type safety.

**Type Definitions:**

```typescript
// frontend/src/types/recipe.ts
export interface Recipe {
  id: string;
  title: string;
  description: string | null;
  servings: number;
  prep_time_minutes: number;
  cook_time_minutes: number;
  difficulty: 'easy' | 'medium' | 'hard';
  current_version: number;
  times_cooked: number;
  last_cooked_date: string | null;
  is_deleted: boolean;
  created_at: string;
}

export interface RecipeCreate {
  title: string;
  description?: string;
  servings: number;
  prep_time_minutes: number;
  cook_time_minutes: number;
  difficulty: 'easy' | 'medium' | 'hard';
  ingredients: Ingredient[];
  instructions: string[];
  tags?: string[];
  source_url?: string;
}

export interface Ingredient {
  quantity: number;
  unit: string;
  name: string;
  notes?: string;
}
```

**Using Types:**

```typescript
import type { Recipe } from '@/types/recipe';

function RecipeCard({ recipe }: { recipe: Recipe }) {
  return (
    <div>
      <h3>{recipe.title}</h3>
      <p>{recipe.description}</p>
    </div>
  );
}
```

---

## Key Features Implementation

### Recipe Versioning System

**How It Works:**

1. Recipe has `current_version` field
2. Each edit creates a new `RecipeVersion` record
3. Old versions are preserved
4. Version history can be viewed
5. Versions can be reverted (creates new version with old content)

**Database Structure:**

```sql
recipes:
  id, title, description, current_version, times_cooked, last_cooked_date

recipe_versions:
  id, recipe_id, version_number, servings, prep_time_minutes, cook_time_minutes,
  difficulty, instructions, source_url, created_by_id, created_at

ingredients:
  id, recipe_version_id, quantity, unit, name, notes
```

**Creating a Version:**

```python
# Increment version number
new_version_number = recipe.current_version + 1

# Create new RecipeVersion
version = RecipeVersion(
    recipe_id=recipe.id,
    version_number=new_version_number,
    # ... fields
)

# Add ingredients to version
for ing in ingredients:
    Ingredient(recipe_version_id=version.id, ...)

# Update recipe.current_version
recipe.current_version = new_version_number
```

**Reverting a Version:**

```python
old_version = get_version(recipe_id, version_number)
new_version_number = recipe.current_version + 1

# Copy old version data to new version
new_version = RecipeVersion(
    recipe_id=recipe.id,
    version_number=new_version_number,
    servings=old_version.servings,
    # ... copy all fields
)
# Copy ingredients
for old_ing in old_version.ingredients:
    Ingredient(recipe_version_id=new_version.id, ...)
```

### Inventory Auto-Deduction

**How It Works:**

1. User marks meal as cooked
2. System gets recipe ingredients
3. For each ingredient, search inventory by name (case-insensitive)
4. If found, reduce quantity
5. Create inventory history record

**Implementation:**

```python
# backend/src/services/inventory_service.py
def deduct_ingredients_for_recipe(
    db: Session,
    recipe_id: UUID,
    servings_multiplier: float = 1.0
):
    """Deduct inventory when recipe is cooked."""
    recipe = get_recipe(db, recipe_id)
    version = recipe.current_version_obj

    for ingredient in version.ingredients:
        # Find inventory item by name (case-insensitive)
        item = db.query(InventoryItem).filter(
            func.lower(InventoryItem.name) == ingredient.name.lower()
        ).first()

        if item:
            # Calculate deduction
            deduct_qty = ingredient.quantity * servings_multiplier
            new_qty = max(0, item.quantity - deduct_qty)

            # Update quantity
            old_qty = item.quantity
            item.quantity = new_qty

            # Create history record
            history = InventoryHistory(
                inventory_item_id=item.id,
                change_type='deduction',
                previous_quantity=old_qty,
                new_quantity=new_qty,
                change_amount=-deduct_qty,
                reason=f'Used in recipe: {recipe.title}',
                recipe_id=recipe_id
            )
            db.add(history)

    db.commit()
```

### Recipe Suggestions Algorithm

**6 Strategies:**

1. **Rotation**: Not cooked recently
2. **Favorites**: High ratings
3. **Never Tried**: times_cooked = 0
4. **Available Inventory**: Match ingredients to stock
5. **Seasonal**: Tagged with current season
6. **Quick Meals**: Total time <= 30 minutes

**Implementation Example (Rotation):**

```python
def suggest_by_rotation(db: Session, user_id: UUID, limit: int = 10):
    recipes = db.query(Recipe).filter(
        Recipe.is_deleted == False
    ).order_by(
        Recipe.last_cooked_date.asc().nulls_first(),  # NULL first (never cooked)
        Recipe.times_cooked.asc(),                     # Then least cooked
        Recipe.title.asc()                             # Then alphabetically
    ).limit(limit).all()

    suggestions = []
    for recipe in recipes:
        days_since_cooked = None
        if recipe.last_cooked_date:
            days_since_cooked = (date.today() - recipe.last_cooked_date).days

        reason = (
            "Never tried before" if recipe.times_cooked == 0
            else f"Not cooked in {days_since_cooked} days"
        )

        suggestions.append({
            "recipe_id": str(recipe.id),
            "title": recipe.title,
            "reason": reason,
            "days_since_cooked": days_since_cooked
        })

    return suggestions
```

**Available Inventory Strategy:**

```python
def suggest_by_available_inventory(db: Session, user_id: UUID, limit: int = 10):
    recipes = db.query(Recipe).filter(Recipe.is_deleted == False).all()
    inventory_items = db.query(InventoryItem).all()

    # Create set of available ingredients (case-insensitive)
    available = {item.name.lower() for item in inventory_items if item.quantity > 0}

    scored_recipes = []
    for recipe in recipes:
        version = recipe.current_version_obj
        ingredients = version.ingredients

        if not ingredients:
            continue

        # Calculate match percentage
        matched = sum(1 for ing in ingredients if ing.name.lower() in available)
        match_pct = (matched / len(ingredients)) * 100

        scored_recipes.append({
            "recipe": recipe,
            "match_percentage": match_pct,
            "matched_count": matched,
            "total_count": len(ingredients)
        })

    # Sort by match percentage
    scored_recipes.sort(key=lambda x: x['match_percentage'], reverse=True)

    suggestions = []
    for item in scored_recipes[:limit]:
        recipe = item['recipe']
        suggestions.append({
            "recipe_id": str(recipe.id),
            "title": recipe.title,
            "match_percentage": round(item['match_percentage'], 1),
            "reason": f"{item['matched_count']}/{item['total_count']} ingredients available"
        })

    return suggestions
```

### Notification System

**Notification Types:**

- `low_stock`: Inventory below threshold
- `expiring`: Items expiring soon
- `meal_reminder`: Upcoming meal
- `recipe_update`: Recipe edited
- `system`: Admin announcements

**Auto-Generation:**

```python
# Generate low stock notifications (run periodically)
def generate_low_stock_notifications(db: Session):
    items = db.query(InventoryItem).filter(
        InventoryItem.quantity < InventoryItem.min_quantity_threshold
    ).all()

    for item in items:
        # Check if notification already exists
        existing = db.query(Notification).filter(
            Notification.type == 'low_stock',
            Notification.entity_id == item.id,
            Notification.is_read == False
        ).first()

        if not existing:
            notification = Notification(
                user_id=item.owner_id,  # or all users
                type='low_stock',
                title=f'Low stock: {item.name}',
                message=f'{item.name} is running low ({item.quantity} {item.unit} remaining)',
                link=f'/inventory/{item.id}',
                entity_id=item.id
            )
            db.add(notification)

    db.commit()
```

### Shopping List Generation

**Algorithm:**

1. Get all meals in menu plan
2. Get all ingredients from recipes
3. Aggregate quantities by ingredient name
4. Check current inventory
5. Calculate net deficit (need - have)
6. Group by category

**Implementation:**

```python
def generate_shopping_list(db: Session, menu_plan_id: UUID):
    menu_plan = db.query(MenuPlan).filter(MenuPlan.id == menu_plan_id).first()

    # Aggregate ingredients
    ingredient_totals = {}
    for meal in menu_plan.meals:
        recipe = meal.recipe
        version = recipe.current_version_obj
        servings_multiplier = meal.servings / version.servings

        for ing in version.ingredients:
            key = ing.name.lower()
            if key not in ingredient_totals:
                ingredient_totals[key] = {
                    'name': ing.name,
                    'unit': ing.unit,
                    'quantity': 0,
                    'category': get_ingredient_category(ing.name)
                }
            ingredient_totals[key]['quantity'] += ing.quantity * servings_multiplier

    # Check inventory
    inventory_items = db.query(InventoryItem).all()
    inventory_dict = {item.name.lower(): item for item in inventory_items}

    shopping_list = []
    for key, ing_data in ingredient_totals.items():
        current_stock = 0
        if key in inventory_dict:
            current_stock = inventory_dict[key].quantity

        net_needed = max(0, ing_data['quantity'] - current_stock)

        if net_needed > 0:
            shopping_list.append({
                'name': ing_data['name'],
                'category': ing_data['category'],
                'total_needed': round(ing_data['quantity'], 2),
                'current_stock': round(current_stock, 2),
                'net_needed': round(net_needed, 2),
                'unit': ing_data['unit']
            })

    # Group by category
    grouped = {}
    for item in shopping_list:
        category = item['category']
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(item)

    return grouped
```

---

## Adding New Features

Step-by-step guide to adding a new feature.

### Backend Checklist

1. **Create or Update Model**
   - Define table structure in `models/`
   - Add relationships
   - Create database migration (if needed)

2. **Create Pydantic Schemas**
   - Define request schema (`*Create`, `*Update`)
   - Define response schema (`*Response`)
   - Add validation

3. **Create Service**
   - Implement business logic in `services/`
   - Add CRUD operations
   - Handle transactions

4. **Create API Endpoint**
   - Define routes in `api/`
   - Add authentication/authorization
   - Call service methods
   - Handle errors

5. **Add Tests**
   - Write unit tests for service
   - Write integration tests for API
   - Ensure >80% coverage

6. **Update API Spec**
   - Document new endpoints in `docs/API_SPEC.yaml`
   - Include request/response examples

### Frontend Checklist

1. **Create Types**
   - Define TypeScript interfaces in `types/`
   - Export from `types/index.ts`

2. **Create API Client Method**
   - Add function in `lib/api/`
   - Use Axios for HTTP requests
   - Handle errors

3. **Create Components**
   - Build UI components in `components/`
   - Follow existing patterns
   - Use Tailwind for styling

4. **Create Pages**
   - Add pages in `app/` directory
   - Use Next.js App Router conventions
   - Integrate components

5. **Add Navigation**
   - Update navigation menu if needed
   - Add links to new pages

### Example: Adding a "Meal Prep" Feature

**Backend:**

1. **Model** (`models/meal_prep.py`):
```python
class MealPrep(Base):
    __tablename__ = "meal_preps"
    __table_args__ = {"schema": "meal_planning"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("shared.users.id"))
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("meal_planning.recipes.id"))
    prep_date = Column(Date, nullable=False)
    servings_made = Column(Integer, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
```

2. **Schema** (`schemas/meal_prep.py`):
```python
class MealPrepCreate(BaseModel):
    recipe_id: UUID
    prep_date: date
    servings_made: int = Field(..., gt=0)
    notes: Optional[str] = None

class MealPrepResponse(BaseModel):
    id: UUID
    recipe_id: UUID
    prep_date: date
    servings_made: int
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
```

3. **Service** (`services/meal_prep_service.py`):
```python
class MealPrepService:
    @staticmethod
    def create_meal_prep(db: Session, data: MealPrepCreate, user_id: UUID):
        meal_prep = MealPrep(
            user_id=user_id,
            recipe_id=data.recipe_id,
            prep_date=data.prep_date,
            servings_made=data.servings_made,
            notes=data.notes
        )
        db.add(meal_prep)
        db.commit()
        db.refresh(meal_prep)
        return meal_prep
```

4. **API** (`api/meal_preps.py`):
```python
router = APIRouter()

@router.post("", response_model=MealPrepResponse, status_code=201)
async def create_meal_prep(
    data: MealPrepCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return MealPrepService.create_meal_prep(db, data, current_user.id)
```

5. **Register Router** (`main.py`):
```python
from src.api import meal_preps
app.include_router(meal_preps.router, prefix="/api/meal-preps", tags=["meal-preps"])
```

**Frontend:**

1. **Types** (`types/mealPrep.ts`):
```typescript
export interface MealPrep {
  id: string;
  recipe_id: string;
  prep_date: string;
  servings_made: number;
  notes: string | null;
  created_at: string;
}

export interface MealPrepCreate {
  recipe_id: string;
  prep_date: string;
  servings_made: number;
  notes?: string;
}
```

2. **API Client** (`lib/api/mealPreps.ts`):
```typescript
export async function createMealPrep(data: MealPrepCreate): Promise<MealPrep> {
  const response = await apiClient.post('/meal-preps', data);
  return response.data;
}
```

3. **Component** (`components/meal-preps/MealPrepForm.tsx`):
```tsx
export default function MealPrepForm({ recipeId }: { recipeId: string }) {
  const { register, handleSubmit } = useForm<MealPrepCreate>();
  const mutation = useMutation({ mutationFn: createMealPrep });

  const onSubmit = (data: MealPrepCreate) => {
    mutation.mutate({ ...data, recipe_id: recipeId });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

4. **Page** (`app/(main)/meal-preps/page.tsx`):
```tsx
export default function MealPrepsPage() {
  // Implement page
}
```

---

## Code Style and Standards

### Python Style Guide (PEP 8)

- **Indentation**: 4 spaces
- **Line length**: 79 characters (88 for Black)
- **Imports**: Grouped (standard library, third-party, local)
- **Naming**:
  - Variables: `snake_case`
  - Functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`
- **Docstrings**: Use triple quotes for all functions/classes
- **Type hints**: Use type hints for function parameters and returns

**Example:**

```python
from typing import List, Optional
from uuid import UUID

def get_recipes(
    db: Session,
    user_id: UUID,
    limit: int = 20
) -> List[Recipe]:
    """
    Get recipes for a user.

    Args:
        db: Database session
        user_id: User ID
        limit: Maximum number of recipes

    Returns:
        List of Recipe instances
    """
    return db.query(Recipe).filter(
        Recipe.created_by_id == user_id
    ).limit(limit).all()
```

**Formatting with Black:**

```bash
# Format all Python files
black backend/src

# Check without modifying
black --check backend/src
```

### TypeScript/React Conventions

- **Indentation**: 2 spaces
- **Naming**:
  - Variables: `camelCase`
  - Components: `PascalCase`
  - Files: `PascalCase.tsx` for components, `camelCase.ts` for utilities
  - Types/Interfaces: `PascalCase`
- **Imports**: Absolute imports using `@/` alias
- **Props**: Define interface for component props
- **Hooks**: Prefix with `use` (e.g., `useRecipes`)

**Example:**

```tsx
import { useState } from 'react';
import type { Recipe } from '@/types/recipe';

interface RecipeCardProps {
  recipe: Recipe;
  onSelect?: (recipe: Recipe) => void;
}

export default function RecipeCard({ recipe, onSelect }: RecipeCardProps) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={() => onSelect?.(recipe)}
    >
      <h3>{recipe.title}</h3>
    </div>
  );
}
```

**Formatting with Prettier:**

```bash
# Format all files
npm run format

# Check without modifying
npm run format:check
```

### Git Commit Message Format (Conventional Commits)

Use Conventional Commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Build process, dependencies

**Examples:**

```bash
feat(recipes): add recipe versioning system

Implement full version control for recipes with history tracking.
Each edit creates a new version while preserving old ones.

Closes #42

fix(inventory): prevent negative quantities

Add validation to prevent inventory quantities from going below zero.

test(api): add tests for recipe suggestions

Add comprehensive tests for all 6 suggestion strategies.
Coverage increased to 85%.
```

### Modern FastAPI Patterns

This project follows modern FastAPI best practices and patterns:

**Lifespan Context Manager (Recommended):**

Modern FastAPI uses the `lifespan` context manager instead of deprecated `@app.on_event()` decorators:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("Starting application...")
    # Initialize database, load resources, etc.

    yield  # Application runs here

    # Shutdown
    print("Shutting down application...")
    # Close connections, cleanup resources, etc.

app = FastAPI(lifespan=lifespan)
```

**SQLAlchemy 2.0 Compatibility:**

Use `text()` for raw SQL execution:

```python
from sqlalchemy import text

# Correct (SQLAlchemy 2.0+)
conn.execute(text("SELECT 1"))

# Deprecated (will be removed)
conn.execute("SELECT 1")
```

**Import Organization:**

Follow isort/black standards for import organization:

```python
# Standard library imports (sorted alphabetically)
import os
import uuid
from datetime import datetime
from typing import List, Optional

# Third-party imports (sorted alphabetically)
from fastapi import APIRouter, Depends
from sqlalchemy import Column, String, text
from sqlalchemy.orm import Session

# Local imports (sorted alphabetically)
from src.core.config import settings
from src.core.database import get_db
from src.models.user import User
```

---

## Debugging

### Backend Debugging

**Logging:**

```python
import logging

logger = logging.getLogger(__name__)

def create_recipe(db: Session, data: RecipeCreate):
    logger.info(f"Creating recipe: {data.title}")
    try:
        # ... implementation
        logger.debug(f"Recipe created with ID: {recipe.id}")
        return recipe
    except Exception as e:
        logger.error(f"Error creating recipe: {e}", exc_info=True)
        raise
```

**Using Debugger:**

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use Python 3.7+ breakpoint
breakpoint()
```

**VS Code Debugging:**

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "src.main:app",
        "--reload"
      ],
      "jinja": true,
      "justMyCode": true
    }
  ]
}
```

**Common Issues:**

- **Database connection errors**: Check DATABASE_URL, ensure PostgreSQL is running
- **Import errors**: Verify virtual environment is activated
- **SQLAlchemy errors**: Check model definitions, relationships

### Frontend Debugging

**Browser DevTools:**

- **Console**: `console.log()`, `console.error()`
- **Network**: Inspect API requests/responses
- **React DevTools**: View component hierarchy and props

**React DevTools:**

```tsx
// Add displayName for easier debugging
RecipeCard.displayName = 'RecipeCard';
```

**Network Inspection:**

```tsx
// Log API errors
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data);
    return Promise.reject(error);
  }
);
```

**Common Issues:**

- **CORS errors**: Check CORS configuration in backend
- **API errors**: Check Network tab, verify request format
- **State not updating**: Check if state is immutable, use proper setters
- **Routing issues**: Verify file structure matches Next.js conventions

---

## Contributing

### Git Workflow (Gitflow)

**Branches:**

- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Urgent production fixes
- `release/*`: Release preparation

**Workflow:**

1. **Start feature**:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/recipe-tags
```

2. **Make changes**:
```bash
# Make changes
git add .
git commit -m "feat(recipes): add tag filtering"
```

3. **Push and create PR**:
```bash
git push origin feature/recipe-tags
# Create pull request on GitHub
```

4. **Code review and merge**:
- Address review comments
- Once approved, merge to develop
- Delete feature branch

### Branch Naming

Format: `<type>/<short-description>`

**Examples:**
- `feature/meal-prep-tracking`
- `bugfix/inventory-negative-quantity`
- `hotfix/login-error`
- `docs/update-readme`

### Pull Request Process

**PR Template:**

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] Code follows project style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests passing
- [ ] No merge conflicts

## Related Issues
Closes #123
```

**Review Checklist:**

- Code quality and readability
- Test coverage
- Documentation
- Performance implications
- Security considerations
- Breaking changes

### Code Review Checklist

**Reviewer Checklist:**

- [ ] Code is understandable
- [ ] Logic is correct
- [ ] Edge cases handled
- [ ] Error handling present
- [ ] Tests cover new code
- [ ] No security vulnerabilities
- [ ] Performance acceptable
- [ ] Documentation updated
- [ ] No code duplication
- [ ] Follows project conventions

**Author Checklist:**

- [ ] Self-reviewed code
- [ ] Tests added/updated
- [ ] Tests passing locally
- [ ] Documentation updated
- [ ] Commit messages clear
- [ ] No debug code left
- [ ] No commented-out code
- [ ] Branch up-to-date with develop

### Definition of Done

See [DEFINITION_OF_DONE.md](DEFINITION_OF_DONE.md) for comprehensive checklist.

**Summary:**
- Code implemented and working
- Tests written and passing (>80% coverage)
- Code reviewed and approved
- Documentation updated
- No known bugs
- Merged to develop branch

---

## Additional Resources

**Documentation:**
- [User Guide](USER_GUIDE.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Admin Guide](ADMIN_GUIDE.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Testing Guide](TESTING.md)
- [Architecture](ARCHITECTURE.md)
- [Database Schema](DATABASE_SCHEMA.md)

**External Resources:**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

**Community:**
- GitHub Issues: Report bugs, request features
- Pull Requests: Contribute code
- Discussions: Ask questions, share ideas

---

**Document Version:** 1.0
**Last Updated:** October 1, 2025
**Application Version:** 1.0.2

"""
Multi-Agent Configuration for Household Meal Planning System
This file defines the 6 specialized agents that will work together to build the application.
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool, DirectoryReadTool, CodeDocsSearchTool
import os

# Initialize basic tools (CodeDocsSearchTool requires API keys, so we'll add it later if needed)
file_read_tool = FileReadTool()
directory_read_tool = DirectoryReadTool()

# Agent 1: Database & Architecture Agent
database_architect = Agent(
    role="Database Architect and API Contract Designer",
    goal="Design PostgreSQL multi-schema structure, create migrations, and define comprehensive API contracts",
    backstory="""You are an expert database architect with deep knowledge of PostgreSQL,
    multi-tenant database design, and RESTful API architecture. You specialize in designing
    scalable database schemas that support future extensibility and cross-application queries.
    You understand the importance of proper indexing, foreign key relationships, and migration strategies.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read_tool, directory_read_tool],
    memory=True
)

# Agent 2: Backend API Agent
backend_developer = Agent(
    role="Backend Developer specializing in FastAPI and Python",
    goal="Implement RESTful APIs, authentication, recipe scraping (ethically), and all business logic",
    backstory="""You are a seasoned backend engineer with expertise in FastAPI, SQLAlchemy,
    and Python best practices. You're passionate about writing secure, performant code and
    have a strong understanding of ethical web scraping practices (robots.txt, rate limiting).
    You excel at implementing complex business logic, authentication systems, and data processing pipelines.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read_tool],
    memory=True
)

# Agent 3: Frontend UI Agent
frontend_developer = Agent(
    role="Frontend Developer specializing in React/Next.js and UX Design",
    goal="Build responsive, accessible UI with excellent UX including drag-and-drop interfaces",
    backstory="""You are a frontend specialist with deep knowledge of React, Next.js, TypeScript,
    and modern CSS frameworks. You're passionate about accessibility (WCAG 2.1 AA compliance) and
    creating intuitive user experiences. You have experience building complex interactive features
    like drag-and-drop interfaces that work seamlessly on both desktop and mobile devices.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read_tool],
    memory=True
)

# Agent 4: DevOps & Infrastructure Agent
devops_engineer = Agent(
    role="DevOps Engineer specializing in Docker and deployment automation",
    goal="Create Docker containers, CI/CD pipelines, and comprehensive deployment documentation",
    backstory="""You are an infrastructure specialist with extensive experience in Docker,
    docker-compose, and Proxmox virtualization. You understand local network deployment,
    security best practices for home servers, and automation. You excel at writing clear
    documentation that makes complex deployments accessible to non-technical users.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read_tool, directory_read_tool],
    memory=True
)

# Agent 5: Testing & QA Agent
qa_engineer = Agent(
    role="QA Engineer specializing in security and accessibility testing",
    goal="Write comprehensive test suites, conduct security audits, and ensure 80%+ test coverage",
    backstory="""You are a quality assurance expert with a strong focus on security and accessibility.
    You're well-versed in pytest, Jest, Playwright, and security testing tools like OWASP ZAP.
    You understand WCAG guidelines deeply and are passionate about making applications secure and
    accessible to all users. You believe in test-driven development and comprehensive coverage.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read_tool],
    memory=True
)

# Agent 6: Documentation Agent
technical_writer = Agent(
    role="Technical Writer specializing in beginner-friendly documentation",
    goal="Create comprehensive, clear documentation for users, administrators, and developers",
    backstory="""You are a technical writer with a gift for making complex systems understandable
    to non-technical audiences. You excel at writing step-by-step guides with screenshots, creating
    clear API documentation, and producing developer guides that help onboard new contributors quickly.
    You understand that good documentation is as important as good code.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read_tool, directory_read_tool],
    memory=True
)

# Agent List for easy access
ALL_AGENTS = {
    "database": database_architect,
    "backend": backend_developer,
    "frontend": frontend_developer,
    "devops": devops_engineer,
    "qa": qa_engineer,
    "documentation": technical_writer
}

def create_task(description, expected_output, agent, context=None):
    """Helper function to create tasks with consistent structure"""
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        context=context if context else []
    )

# Example: Create a crew for Phase 1 (Database & Infrastructure)
def create_phase1_crew():
    """Creates crew for Phase 1: Database & Infrastructure Foundation"""

    # Task 1: Database Schema Design
    db_schema_task = create_task(
        description="""Design a comprehensive PostgreSQL multi-schema database structure:
        1. Create 'shared' schema for users, authentication, and admin tables
        2. Create 'meal_planning' schema with tables for:
           - recipes (with current_version tracking)
           - recipe_versions (full version history with snapshots)
           - ingredients (linked to recipe_versions)
           - inventory (with quantity, location, expiration tracking)
           - ratings (thumbs up/down per user)
           - menu_plans and planned_meals
           - admin_settings (for configurable thresholds)
        3. Create placeholder schemas for future apps: chores, learning, rewards
        4. Define all relationships, foreign keys, and indexes
        5. Create Alembic migration scripts
        6. Generate database schema diagrams
        7. Document in docs/DATABASE_SCHEMA.md

        Ensure the schema supports:
        - Recipe versioning with full history
        - User-specific ratings (not averaged)
        - Inventory history tracking
        - Cross-schema queries for future dashboard
        - Performance optimization with proper indexes""",
        expected_output="""Deliverables:
        1. Complete SQL schema files in database/schemas/
        2. Alembic migration scripts in database/migrations/
        3. docs/DATABASE_SCHEMA.md with ERD diagrams
        4. Seed data scripts for testing
        5. Database connection pooling configuration""",
        agent=database_architect
    )

    # Task 2: API Contract Design
    api_contract_task = create_task(
        description="""Create comprehensive OpenAPI 3.0 specification for all API endpoints:

        Define endpoints for:
        - Authentication: /api/auth/register, /login, /logout, /me
        - Recipes: CRUD operations, versioning, scraping
        - Inventory: CRUD, low-stock alerts, history
        - Ratings: Create, update, favorites calculation
        - Menu Planning: Weekly menus, multi-week support
        - Shopping Lists: Generation, purchase tracking
        - Admin: User management, settings configuration

        For each endpoint include:
        - HTTP method and path
        - Request/response schemas
        - Authentication requirements
        - Error responses
        - Example requests

        Save as docs/API_SPEC.yaml (OpenAPI format)""",
        expected_output="""Deliverables:
        1. docs/API_SPEC.yaml - Complete OpenAPI 3.0 specification
        2. docs/API_SPEC.md - Human-readable API documentation
        3. Request/response schema definitions
        4. Authentication flow documentation""",
        agent=database_architect,
        context=[db_schema_task]
    )

    # Task 3: Docker Infrastructure Setup
    docker_setup_task = create_task(
        description="""Create production-ready Docker environment:

        1. Create Dockerfiles:
           - backend/Dockerfile (Python 3.12, FastAPI, optimized layers)
           - frontend/Dockerfile (Node.js, Next.js production build)
           - Use official postgres:15 image for database

        2. Create infrastructure/docker-compose.yml:
           - Services: postgres, backend, frontend, nginx
           - Networks: app-network (bridge)
           - Volumes: postgres_data, uploads
           - Environment variable injection from .env
           - Health checks for all services

        3. Create infrastructure/nginx.conf:
           - Reverse proxy: /api/* → backend:8000
           - Static files: /* → frontend:3000
           - SSL/TLS configuration (self-signed cert)
           - Security headers

        4. Write infrastructure/proxmox-setup.md:
           - VM specifications (4 cores, 8GB RAM, 50GB storage)
           - Ubuntu Server 22.04 installation steps
           - Network configuration (bridge, static IP, firewall)
           - Docker installation

        5. Create docs/LOCAL_SETUP.md for developers""",
        expected_output="""Deliverables:
        1. backend/Dockerfile
        2. frontend/Dockerfile
        3. infrastructure/docker-compose.yml
        4. infrastructure/nginx.conf
        5. infrastructure/proxmox-setup.md
        6. docs/LOCAL_SETUP.md
        7. SSL certificate generation script""",
        agent=devops_engineer
    )

    # Create and return crew
    crew = Crew(
        agents=[database_architect, devops_engineer],
        tasks=[db_schema_task, api_contract_task, docker_setup_task],
        process=Process.sequential,
        verbose=True,
        memory=True
    )

    return crew

# Example: Create crew for Phase 2 (Backend Development)
def create_phase2_crew():
    """Creates crew for Phase 2: Backend API Development"""
    # This would contain backend tasks for Agent 2
    # Implementation similar to phase1, defining all backend development tasks
    pass

# Example: Create crew for Phase 3 (Frontend Development)
def create_phase3_crew():
    """Creates crew for Phase 3: Frontend UI Development"""
    # This would contain frontend tasks for Agent 3
    pass

if __name__ == "__main__":
    print("Multi-Agent Configuration Loaded")
    print(f"Total Agents: {len(ALL_AGENTS)}")
    for name, agent in ALL_AGENTS.items():
        print(f"  - {name.capitalize()}: {agent.role}")

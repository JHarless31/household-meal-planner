# Comprehensive Coding Agent Prompt: Household Meal Planning & Inventory System

## Project Overview
Build a locally-hosted meal planning application for a blended family household that manages recipes, tracks inventory, plans weekly menus, and integrates with other household management applications through a central PostgreSQL database.

---

## 1. SYSTEM ARCHITECTURE

### 1.1 Deployment Environment
- **Host Platform**: Proxmox server (already set up)
- **Deployment Method**: Docker container in a Linux VM (Ubuntu recommended)
  - **Rationale**: VM provides better isolation and security than LXC containers, supports easier updates and maintenance, and is the recommended approach for Docker on Proxmox
- **Operating System**: Linux (Ubuntu Server or Debian)
- **Database**: PostgreSQL (shared central database for all household applications)

### 1.2 Database Architecture
- **Single Database, Multiple Schemas Approach**:
  - Create one PostgreSQL database for all household applications
  - Use separate schemas for each application (meal_planning, chores, learning, rewards, etc.)
  - Benefits: Cross-schema queries from single connection, easier backup management, better resource utilization
  - Schema structure:
    ```
    household_db/
    ├── meal_planning/    (recipes, inventory, menus, ratings)
    ├── chores/           (task assignments, schedules)
    ├── learning/         (educational content, progress)
    ├── rewards/          (allowance, reward tracking)
    └── shared/           (user accounts, authentication, admin)
    ```

### 1.3 Technology Stack Selection
The coding agent should select appropriate technologies based on these requirements:
- **Backend**: Modern web framework suitable for Python (FastAPI/Flask) or Node.js (Express/Nest.js)
- **Frontend**: React-based framework (Next.js recommended for better SEO and performance)
- **Authentication**: JWT-based with secure password hashing (bcrypt/argon2)
- **Recipe Scraping**: Python-based solution (BeautifulSoup4, Scrapy, or similar)
- **Containerization**: Docker with docker-compose for orchestration
- **Version Control**: Git with GitHub

---

## 2. MEAL PLANNING APPLICATION REQUIREMENTS

### 2.1 Recipe Management

#### 2.1.1 Recipe Data Model
Each recipe must store:
- **Basic Information**:
  - Title
  - Description
  - Source (URL if scraped, "Manual Entry" if user-created)
  - Date added
  - Created by (user ID)
  
- **Cooking Details**:
  - Preparation time (minutes)
  - Cook time (minutes)
  - Total time (calculated)
  - Number of servings
  - Difficulty level (Easy/Medium/Hard)
  
- **Ingredients**:
  - Ingredient name
  - Quantity
  - Unit of measurement
  - Optional: category (produce, dairy, meat, etc.)
  
- **Instructions**:
  - Step-by-step cooking instructions
  - Step number for ordering
  
- **Additional Data**:
  - Recipe photos (multiple images supported)
  - Categories/Tags (searchable, e.g., "breakfast", "vegetarian", "quick meals")
  - Nutritional information (optional: calories, protein, carbs, fat per serving)

#### 2.1.2 Recipe Versioning System
- Each recipe can have multiple versions
- Version tracking includes:
  - Version number (incremental)
  - Modification date
  - Modified by (user ID)
  - Change description
  - Complete snapshot of recipe at that version
- **Display Logic**:
  - Default view always shows latest version
  - Dropdown selector to view/use previous versions
  - "Revert to this version" functionality

#### 2.1.3 Recipe Input Methods

**Method 1: Web Scraping**
- Users can enter a recipe URL
- System scrapes pertinent information:
  - Recipe title and description
  - Ingredients list with quantities
  - Cooking instructions
  - Prep/cook times
  - Optional: images
- **Ethical Scraping Requirements**:
  - Check and respect robots.txt file before scraping
  - Implement rate limiting (max 1 request per 5 seconds per domain)
  - Use descriptive User-Agent identifying the application
  - Handle errors gracefully if site blocks scraping
  - Display warning if robots.txt disallows scraping
  - Offer manual entry alternative
- Scraped data presented for user review/editing before saving
- Store original source URL with recipe

**Method 2: Manual Entry**
- User-friendly form for entering all recipe fields
- Dynamic ingredient/instruction row addition
- Image upload capability
- Auto-save draft functionality

### 2.2 Inventory Management

#### 2.2.1 Inventory Data Model
Each inventory item tracks:
- Item name
- Current quantity
- Unit of measurement
- Category (produce, dairy, meat, pantry, frozen, etc.)
- Storage location (pantry, fridge, freezer)
- Expiration date (optional)
- Minimum stock level (for low inventory alerts)
- Date added
- Last updated

#### 2.2.2 Inventory Features
- **Add/Remove Items**: Manual entry interface
- **Quantity Adjustment**: Increase/decrease with reasons (purchased, used, expired)
- **Automatic Deduction**: Option to auto-deduct ingredients when recipe is marked as "cooked"
- **Low Stock Alerts**: Notifications when items below minimum level
- **Expiration Tracking**: Warnings for items approaching expiration
- **Recipe Matching**: Display recipes that can be made with available inventory
- **Inventory History**: Track changes over time for insights

### 2.3 Rating & Feedback System

#### 2.3.1 Rating Structure
- **User-Specific Ratings**:
  - Each user can rate any recipe
  - Thumbs up/thumbs down binary rating
  - Ratings are individual, not averaged
  - Users can change their rating anytime

#### 2.3.2 Recipe Modifications & Feedback
- Users can submit:
  - Recipe modifications (ingredient substitutions, technique changes)
  - Meal feedback (taste, difficulty, time accuracy)
  - Text comments
- Feedback attached to specific recipe versions
- Optional: Cook/modifier can review and integrate feedback into new version

#### 2.3.3 Favorites & Variety System
- **Household Favorites Calculation**:
  - Configurable threshold (default: 75% thumbs up)
  - Configurable minimum raters (default: 3 people)
  - Admin can adjust these settings
  - "Favorites" tag auto-applied when criteria met

- **Recipe Rotation/Variety Features**:
  - Track "last cooked" date for each recipe
  - Configurable "recent" period (default: 2 weeks)
  - UI highlights:
    - Recipes not cooked recently
    - Recipes used in last X weeks (warning indicator)
  - Filters: "Not recently cooked", "Never tried", "Due for rotation"

### 2.4 Weekly Menu Planning

#### 2.4.1 Planning Interface
- **Calendar View**:
  - 7-day week display
  - Each day shows: breakfast, lunch, dinner slots
  - Drag-and-drop recipe cards onto meal slots
  - Visual representation of planned meals
  
#### 2.4.2 Planning Features
- **Recipe Suggestions**:
  - Based on available inventory
  - Prioritize recipes with ingredients on hand
  - Show "shopping needed" indicator for recipes requiring additional items
  - Suggest recipes not recently cooked
  - Highlight household favorites
  
- **Flexible Meal Assignment**:
  - Any recipe can be assigned to any meal (no breakfast/lunch/dinner restrictions)
  - Tags are for search/filtering only
  
- **Multi-Week Planning**:
  - View and plan multiple weeks in advance
  - Copy previous week's menu as template
  - Recurring meal patterns (e.g., "Taco Tuesday")

#### 2.4.3 Shopping List Generation
- **Automated List Creation**:
  - Compares planned recipe ingredients vs. current inventory
  - Generates list of needed items with quantities
  - Aggregates duplicate ingredients across recipes
  - Organizes by store sections (produce, dairy, etc.)
  
- **Shopping List Features**:
  - Shareable (email, text, print, link)
  - Check-off items while shopping
  - Store organization toggle (turn on/off category grouping)
  - Manual item addition
  - Quantity adjustment
  - Mark items as "purchased" to auto-update inventory

---

## 3. USER MANAGEMENT & ADMIN PORTAL

### 3.1 User Authentication
- **Individual Login Credentials**:
  - Username and password for each family member
  - Secure password requirements (min length, complexity)
  - Optional: password reset via email
  - Session management with appropriate timeout

### 3.2 User Roles & Permissions
- **Admin Role**:
  - Full access to all features
  - User management (create, edit, delete accounts)
  - Application settings configuration
  - Access to all household applications
  - View aggregate statistics and reports

- **Standard User Role**:
  - Access to meal planning features
  - Submit recipes, rate, provide feedback
  - View and edit inventory
  - Participate in menu planning
  - Access to their personal data

- **Child User Role** (optional future enhancement):
  - Limited permissions (view-only for certain features)
  - Cannot delete recipes or make major changes

### 3.3 Central Admin Portal
- **User Management Section**:
  - List all users with status (active/inactive)
  - Create new user accounts
  - Edit user details (username, password, role)
  - Deactivate/reactivate accounts
  - View user activity logs

- **Application Management**:
  - Enable/disable applications (meal planning, chores, learning, rewards)
  - Configure application-specific settings
  - View application health/status
  - Access logs and error reports

- **System Settings**:
  - Household favorites threshold configuration
  - Recipe rotation period settings
  - Inventory alert thresholds
  - Notification preferences
  - Backup and maintenance scheduling

### 3.4 Individual Dashboard
- **Personalized Home Page** for each user showing:
  - Upcoming meals for the week
  - Assigned chores (from chores app)
  - Learning progress (from learning app)
  - Reward balance (from rewards app)
  - Quick actions (add recipe, update inventory, rate recent meal)
  - Notifications and alerts
  - Recently viewed recipes

---

## 4. MULTI-AGENT DEVELOPMENT APPROACH

### 4.1 Agent Roles & Responsibilities

The project should be divided among specialized agents:

#### Agent 1: Database & Architecture Agent
**Responsibilities**:
- Design and implement PostgreSQL database schema
- Set up multi-schema structure for all applications
- Create database migrations and versioning
- Implement database connection pooling
- Design API contracts between frontend and backend
- Set up authentication/authorization framework

**Deliverables**:
- Database schema diagrams
- Migration scripts
- Database documentation
- API specification (OpenAPI/Swagger)

#### Agent 2: Backend API Agent
**Responsibilities**:
- Implement RESTful API endpoints
- Business logic for recipes, inventory, ratings, menu planning
- Integration with PostgreSQL database
- Authentication and session management
- Recipe scraping service with ethical compliance
- Shopping list generation logic

**Deliverables**:
- Backend API implementation
- API endpoint documentation
- Unit tests for business logic
- Integration tests

#### Agent 3: Frontend UI Agent
**Responsibilities**:
- User interface design and implementation
- Responsive layouts for phones and computers
- Drag-and-drop menu planning interface
- Recipe browsing and search functionality
- User authentication flows
- Admin portal interface

**Deliverables**:
- Frontend application code
- UI component library
- User experience documentation
- Accessibility compliance

#### Agent 4: DevOps & Infrastructure Agent
**Responsibilities**:
- Docker containerization
- Docker Compose orchestration
- Proxmox VM setup instructions
- Network configuration (local access only)
- Backup and restore procedures
- CI/CD pipeline setup with GitHub Actions
- Monitoring and logging setup

**Deliverables**:
- Dockerfile and docker-compose.yml
- Deployment documentation
- Backup/restore scripts
- Monitoring dashboard

#### Agent 5: Testing & Quality Assurance Agent
**Responsibilities**:
- Write comprehensive test suites
- End-to-end testing
- Security testing (authentication, input validation, SQL injection prevention)
- Performance testing
- Accessibility testing
- Cross-browser/device testing

**Deliverables**:
- Test plans and test cases
- Automated test scripts
- Test coverage reports
- Security audit documentation

#### Agent 6: Documentation Agent
**Responsibilities**:
- User documentation (how to use the application)
- Administrator documentation (system management)
- Developer documentation (code structure, setup, contribution guide)
- API documentation
- Database schema documentation
- Deployment and maintenance guides

**Deliverables**:
- User manual (beginner-friendly)
- Admin guide
- Developer guide (README, CONTRIBUTING.md)
- Inline code documentation
- Video tutorials (optional)

### 4.2 Agent Coordination & Workflow

#### 4.2.1 Git Workflow
Use **Gitflow** branching strategy:
- **main branch**: Production-ready code
- **develop branch**: Integration branch for ongoing development
- **feature/* branches**: Individual features (one per agent task)
- **release/* branches**: Release preparation
- **hotfix/* branches**: Emergency fixes

**Branch Naming Convention**:
```
feature/agent-[number]-[feature-name]
Example: feature/agent-2-recipe-api-endpoints
Example: feature/agent-3-menu-planning-ui
```

#### 4.2.2 Commit Standards
Follow **Conventional Commits**:
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat(recipe-api): add recipe versioning endpoint

- Implement POST /api/recipes/:id/versions
- Add version comparison logic
- Update recipe model with version tracking

Resolves: #42
```

#### 4.2.3 Pull Request Process
1. Agent creates feature branch from develop
2. Agent implements feature with comprehensive tests
3. Agent creates PR with detailed description:
   - What was implemented
   - Testing performed
   - Screenshots (if UI changes)
   - Related issues/dependencies
4. Automated CI pipeline runs tests
5. Code review (can be automated or manual)
6. Merge to develop when approved
7. Delete feature branch

#### 4.2.4 Agent Communication Protocol
- **Shared Documentation**: Central design document (in repository)
- **API Contracts**: OpenAPI specification for all endpoints
- **Database Schema**: Single source of truth in version control
- **Issue Tracking**: GitHub Issues for tasks and dependencies
- **Dependency Declaration**: Each agent declares dependencies on other agents' work
- **Status Updates**: Regular commits and PR descriptions

### 4.3 Project File Structure

```
meal-planning-system/
├── .github/
│   └── workflows/           # CI/CD pipelines
│       ├── backend-tests.yml
│       ├── frontend-tests.yml
│       └── deploy.yml
├── backend/
│   ├── src/
│   │   ├── api/            # API endpoints
│   │   │   ├── recipes/
│   │   │   ├── inventory/
│   │   │   ├── users/
│   │   │   └── menu/
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Helper functions
│   │   └── scrapers/       # Recipe scraping logic
│   ├── tests/              # Backend tests
│   ├── migrations/         # Database migrations
│   ├── Dockerfile
│   ├── requirements.txt    # or package.json
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API client
│   │   ├── styles/         # CSS/styling
│   │   └── utils/          # Helper functions
│   ├── public/             # Static assets
│   ├── tests/              # Frontend tests
│   ├── Dockerfile
│   ├── package.json
│   └── README.md
├── database/
│   ├── schemas/            # Schema definitions
│   │   ├── meal_planning.sql
│   │   ├── chores.sql
│   │   ├── learning.sql
│   │   └── shared.sql
│   ├── migrations/         # Migration scripts
│   ├── seeds/              # Sample data
│   └── README.md
├── docs/
│   ├── USER_GUIDE.md       # End-user documentation
│   ├── ADMIN_GUIDE.md      # Admin documentation
│   ├── DEVELOPER_GUIDE.md  # Developer setup
│   ├── API_SPEC.md         # API documentation
│   ├── DATABASE_SCHEMA.md  # Database documentation
│   └── DEPLOYMENT.md       # Deployment instructions
├── infrastructure/
│   ├── docker-compose.yml  # Container orchestration
│   ├── nginx.conf          # Reverse proxy config
│   ├── backup-script.sh    # Backup automation
│   └── proxmox-setup.md    # VM setup guide
├── tests/
│   └── e2e/                # End-to-end tests
├── .gitignore
├── LICENSE
├── README.md               # Project overview
└── CONTRIBUTING.md         # Contribution guidelines
```

### 4.4 Development Phases

#### Phase 1: Foundation (Agents 1, 4)
- Set up Git repository and branching strategy
- Design database schema (all applications)
- Create Docker environment
- Set up local development environment
- **Duration**: Week 1

#### Phase 2: Backend Core (Agent 2)
- Implement authentication system
- Create user management APIs
- Implement recipe APIs (CRUD operations)
- Implement inventory APIs
- Basic scraping service
- **Duration**: Weeks 2-3

#### Phase 3: Frontend Core (Agent 3)
- User authentication UI
- Recipe browsing and search
- Recipe detail views
- Inventory management UI
- Basic user dashboard
- **Duration**: Weeks 2-3 (parallel with Phase 2)

#### Phase 4: Advanced Features (Agents 2, 3)
- Recipe versioning system
- Rating and feedback system
- Menu planning interface (drag-and-drop)
- Shopping list generation
- Admin portal
- **Duration**: Weeks 4-5

#### Phase 5: Integration & Polish (Agents 2, 3)
- Recipe suggestions based on inventory
- Favorites and rotation logic
- Notifications and alerts
- UI/UX refinements
- Performance optimization
- **Duration**: Week 6

#### Phase 6: Testing & Documentation (Agents 5, 6)
- Comprehensive testing
- Security audit
- Complete documentation
- User acceptance testing
- **Duration**: Weeks 7-8

#### Phase 7: Deployment (Agent 4)
- Proxmox VM setup
- Production deployment
- Backup configuration
- Monitoring setup
- **Duration**: Week 9

---

## 5. TECHNICAL REQUIREMENTS & BEST PRACTICES

### 5.1 Security Requirements
- **Authentication**: JWT tokens with secure storage
- **Password Security**: Bcrypt or Argon2 hashing
- **Input Validation**: Sanitize all user inputs
- **SQL Injection Prevention**: Use parameterized queries/ORMs
- **XSS Protection**: Escape output, use Content Security Policy
- **HTTPS**: Use SSL/TLS for all connections (even local)
- **Rate Limiting**: Prevent brute force attacks
- **Session Management**: Secure session tokens, appropriate timeouts

### 5.2 Performance Requirements
- **API Response Time**: < 200ms for most endpoints
- **Page Load Time**: < 2 seconds initial load
- **Database Queries**: Optimize with indexes, avoid N+1 queries
- **Image Optimization**: Compress and resize recipe images
- **Caching**: Implement caching for frequently accessed data
- **Pagination**: Implement for large lists (recipes, inventory)

### 5.3 Code Quality Standards
- **Linting**: ESLint (frontend), Pylint/Flake8 (backend)
- **Formatting**: Prettier (frontend), Black (backend Python)
- **Type Safety**: TypeScript (frontend), type hints (Python backend)
- **Code Review**: All PRs require review before merge
- **Test Coverage**: Minimum 80% code coverage
- **Documentation**: JSDoc/docstrings for all functions

### 5.4 Accessibility Requirements
- **WCAG 2.1 Level AA Compliance**:
  - Keyboard navigation
  - Screen reader support
  - Sufficient color contrast
  - Alt text for images
  - ARIA labels where appropriate

### 5.5 Browser & Device Support
- **Desktop Browsers**: Chrome, Firefox, Safari, Edge (latest 2 versions)
- **Mobile Browsers**: Chrome (Android), Safari (iOS)
- **Responsive Design**: Support phones (320px+) and desktops (1920px+)
- **Touch Support**: Drag-and-drop works on touch devices

---

## 6. DEPLOYMENT & OPERATIONS

### 6.1 Proxmox VM Setup
**VM Specifications**:
- **OS**: Ubuntu Server 22.04 LTS (or latest LTS)
- **CPU**: 4 cores (recommended minimum)
- **RAM**: 8GB (recommended minimum)
- **Storage**: 50GB (base) + additional for images/data
- **Network**: Bridge to local network, static IP recommended

**Installation Steps** (to be documented by Agent 4):
1. Create VM in Proxmox
2. Install Ubuntu Server
3. Install Docker and Docker Compose
4. Configure firewall (UFW) for local network only
5. Set up automatic security updates
6. Clone repository
7. Run deployment script

### 6.2 Docker Deployment
**Services**:
- **PostgreSQL Container**: Database server
- **Backend Container**: API server
- **Frontend Container**: Web UI served via Nginx
- **Nginx Reverse Proxy**: Routes requests, serves static files

**docker-compose.yml** structure:
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=household_db
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    networks:
      - app-network
    
  backend:
    build: ./backend
    depends_on:
      - postgres
    environment:
      - DATABASE_URL=postgresql://user:${DB_PASSWORD}@postgres:5432/household_db
      - JWT_SECRET=${JWT_SECRET}
    networks:
      - app-network
    
  frontend:
    build: ./frontend
    depends_on:
      - backend
    networks:
      - app-network
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infrastructure/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

### 6.3 Network Configuration
- **Local Access Only**: No external internet access
- **Static IP Assignment**: Assign VM a static IP on local network
- **Custom Domain** (optional): Use local DNS (e.g., meal-planner.local)
- **mDNS** (alternative): Bonjour/Avahi for easy local discovery
- **Port Configuration**:
  - HTTP: 80
  - HTTPS: 443 (with self-signed cert for local use)

### 6.4 Backup & Maintenance
**Automated Backups**:
- **Database**: Daily PostgreSQL dumps
- **Application Data**: Recipe images, user uploads
- **Configuration**: Docker configs, environment variables
- **Backup Location**: Network-attached storage or separate directory
- **Retention Policy**: 7 daily, 4 weekly, 12 monthly backups

**Maintenance Tasks**:
- Weekly: Review logs for errors
- Monthly: Update Docker images
- Quarterly: Full system backup test restore
- As needed: Database optimization, image cleanup

### 6.5 Monitoring & Logging
- **Application Logs**: Structured logging to files
- **Error Tracking**: Log errors with stack traces
- **Access Logs**: Track API requests
- **Performance Metrics**: Response times, database query times
- **Health Checks**: Endpoint to verify all services running
- **Optional**: Grafana dashboard for visualization

---

## 7. FUTURE EXTENSIBILITY

### 7.1 Integration with Other Household Apps
The database schema should support future applications:

#### Chores Application
- Task assignments
- Completion tracking
- Recurring schedules
- Point/reward integration

#### Personal Learning Application
- Learning modules/courses
- Progress tracking
- Quiz/assessment results
- Certificates/achievements

#### Rewards/Allowance Application
- Point balance tracking
- Allowance scheduling
- Purchase history
- Chore completion bonuses

### 7.2 Dashboard Integration
- Central dashboard aggregates data from all apps
- Unified notification system
- Cross-app insights and reports
- Single sign-on across all applications

### 7.3 Planned Enhancements
Consider these for future iterations:
- Mobile native apps (React Native)
- Voice assistant integration (recipe reading)
- Meal prep timers and notifications
- Integration with smart home devices
- Social features (share recipes with friends)
- Meal planning AI suggestions (ML-based)
- Nutrition tracking and goals
- Integration with online grocery delivery APIs

---

## 8. DELIVERABLES & QUALITY CRITERIA

### 8.1 Code Deliverables
- ✅ Complete, working application deployable via Docker
- ✅ Well-organized, modular codebase
- ✅ Comprehensive test suites (unit, integration, E2E)
- ✅ All code follows style guides and best practices
- ✅ Git history with meaningful commits
- ✅ No hardcoded secrets (use environment variables)

### 8.2 Documentation Deliverables
- ✅ **README.md**: Project overview, quick start guide
- ✅ **USER_GUIDE.md**: Step-by-step user instructions with screenshots
- ✅ **ADMIN_GUIDE.md**: System administration and configuration
- ✅ **DEVELOPER_GUIDE.md**: Setup, architecture, contribution guidelines
- ✅ **API_SPEC.md**: Complete API documentation
- ✅ **DATABASE_SCHEMA.md**: Schema diagrams and descriptions
- ✅ **DEPLOYMENT.md**: Detailed Proxmox and Docker deployment
- ✅ All documentation is clear, beginner-friendly, human-readable

### 8.3 Quality Criteria
- ✅ Application runs without errors on fresh installation
- ✅ All core features implemented and functional
- ✅ Responsive UI works on phones and computers
- ✅ Authentication and authorization work correctly
- ✅ Recipe scraping respects robots.txt and rate limits
- ✅ Database schema supports all current and planned features
- ✅ Passes security audit (no major vulnerabilities)
- ✅ Test coverage > 80%
- ✅ Documentation complete and accurate

---

## 9. AGENT INSTRUCTIONS

### 9.1 General Guidelines for All Agents
1. **Read All Documentation First**: Understand the full system before starting
2. **Check Dependencies**: Ensure other agents' work is complete before depending on it
3. **Communicate via Git**: Use commits, PRs, and issues for coordination
4. **Test Thoroughly**: Every feature should have tests
5. **Document as You Go**: Don't save documentation for later
6. **Follow Standards**: Adhere to project coding standards and conventions
7. **Ask Questions**: Use GitHub issues for clarifications
8. **Be Security-Conscious**: Always validate inputs, use secure patterns
9. **Think About Maintenance**: Write code that's easy to understand and modify
10. **Consider the End User**: This is for a household, not tech experts

### 9.2 First Steps for Coordinator/Lead Agent
1. Set up Git repository on GitHub
2. Create initial project structure (folders, base files)
3. Set up GitHub Actions for CI/CD
4. Create issues for all major tasks
5. Assign issues to appropriate agent roles
6. Create initial `README.md` and `CONTRIBUTING.md`
7. Set up branch protection rules
8. Create project board for tracking progress

### 9.3 Definition of Done
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

---

## 10. SUCCESS CRITERIA

The project is complete when:
1. ✅ A family member with no technical background can:
   - Install the application following the documentation
   - Create an account and log in
   - Add a recipe by URL or manual entry
   - Browse and search recipes
   - Add items to inventory
   - Plan a week's meals using drag-and-drop
   - Generate a shopping list
   - Rate recipes and provide feedback
   - View household favorites and recipe suggestions

2. ✅ An administrator can:
   - Create and manage user accounts
   - Configure application settings
   - Access the admin portal
   - View system status and logs

3. ✅ A developer can:
   - Clone the repository
   - Set up the development environment
   - Understand the code structure
   - Add new features following the established patterns
   - Run all tests successfully

4. ✅ The system:
   - Runs reliably on the Proxmox VM
   - Is accessible to all devices on the local network
   - Performs well with expected load
   - Maintains data integrity
   - Has automated backups configured

---

## 11. CONTACT & SUPPORT

For questions during development:
- **GitHub Issues**: Technical questions, bugs, feature clarifications
- **Pull Request Comments**: Code-specific discussions
- **Project Wiki**: Shared knowledge, design decisions, meeting notes

---

## APPENDIX A: Database Schema Examples

### Meal Planning Schema (meal_planning)

```sql
-- Users table (in shared schema)
CREATE TABLE shared.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Recipes table
CREATE TABLE meal_planning.recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    source_url VARCHAR(500),
    created_by UUID REFERENCES shared.users(id),
    current_version INT NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Recipe versions table
CREATE TABLE meal_planning.recipe_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID REFERENCES meal_planning.recipes(id) ON DELETE CASCADE,
    version_number INT NOT NULL,
    prep_time INT, -- minutes
    cook_time INT, -- minutes
    servings INT,
    difficulty VARCHAR(20),
    instructions TEXT,
    change_description TEXT,
    modified_by UUID REFERENCES shared.users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(recipe_id, version_number)
);

-- Ingredients table
CREATE TABLE meal_planning.ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_version_id UUID REFERENCES meal_planning.recipe_versions(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    quantity DECIMAL(10, 2),
    unit VARCHAR(50),
    category VARCHAR(50)
);

-- Inventory table
CREATE TABLE meal_planning.inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_name VARCHAR(255) NOT NULL,
    quantity DECIMAL(10, 2),
    unit VARCHAR(50),
    category VARCHAR(50),
    location VARCHAR(50), -- pantry, fridge, freezer
    expiration_date DATE,
    minimum_stock DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ratings table
CREATE TABLE meal_planning.ratings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID REFERENCES meal_planning.recipes(id) ON DELETE CASCADE,
    user_id UUID REFERENCES shared.users(id) ON DELETE CASCADE,
    rating BOOLEAN NOT NULL, -- thumbs up (true) or down (false)
    feedback TEXT,
    modifications TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(recipe_id, user_id)
);

-- Menu plans table
CREATE TABLE meal_planning.menu_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    week_start_date DATE NOT NULL,
    created_by UUID REFERENCES shared.users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Planned meals table
CREATE TABLE meal_planning.planned_meals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    menu_plan_id UUID REFERENCES meal_planning.menu_plans(id) ON DELETE CASCADE,
    recipe_id UUID REFERENCES meal_planning.recipes(id),
    meal_date DATE NOT NULL,
    meal_type VARCHAR(20), -- breakfast, lunch, dinner
    cooked BOOLEAN DEFAULT false,
    cooked_date TIMESTAMP
);
```

---

## APPENDIX B: API Endpoint Examples

```
### Authentication
POST   /api/auth/register       # Register new user
POST   /api/auth/login          # Login
POST   /api/auth/logout         # Logout
GET    /api/auth/me             # Get current user info

### Recipes
GET    /api/recipes             # List all recipes (with pagination, filters)
GET    /api/recipes/:id         # Get recipe details (latest version)
GET    /api/recipes/:id/versions/:version  # Get specific version
POST   /api/recipes             # Create new recipe
PUT    /api/recipes/:id         # Update recipe (creates new version)
DELETE /api/recipes/:id         # Delete recipe
POST   /api/recipes/scrape      # Scrape recipe from URL

### Inventory
GET    /api/inventory           # List all inventory items
POST   /api/inventory           # Add inventory item
PUT    /api/inventory/:id       # Update inventory item
DELETE /api/inventory/:id       # Delete inventory item
GET    /api/inventory/low-stock # Get items below minimum stock

### Ratings
POST   /api/recipes/:id/ratings # Rate a recipe
PUT    /api/recipes/:id/ratings/:ratingId  # Update rating
DELETE /api/recipes/:id/ratings/:ratingId  # Remove rating

### Menu Planning
GET    /api/menu-plans          # Get menu plans
GET    /api/menu-plans/:id      # Get specific menu plan
POST   /api/menu-plans          # Create menu plan
PUT    /api/menu-plans/:id      # Update menu plan
DELETE /api/menu-plans/:id      # Delete menu plan

### Shopping List
GET    /api/shopping-list/:menuPlanId  # Generate shopping list for menu plan
POST   /api/shopping-list/:id/items/:itemId/check  # Mark item as purchased

### Admin
GET    /api/admin/users         # List all users
POST   /api/admin/users         # Create user
PUT    /api/admin/users/:id     # Update user
DELETE /api/admin/users/:id     # Delete user
GET    /api/admin/settings      # Get system settings
PUT    /api/admin/settings      # Update system settings
```

---

## APPENDIX C: Environment Variables Template

```env
# Database
DB_HOST=postgres
DB_PORT=5432
DB_NAME=household_db
DB_USER=household_app
DB_PASSWORD=<generate-secure-password>

# Application
NODE_ENV=production
PORT=3000
API_URL=http://localhost:3000

# Authentication
JWT_SECRET=<generate-secure-secret>
JWT_EXPIRATION=24h
SESSION_SECRET=<generate-secure-secret>

# Recipe Scraping
SCRAPER_USER_AGENT=HouseholdMealPlanner/1.0 (+http://your-domain.local/about)
SCRAPER_RATE_LIMIT=5  # seconds between requests
SCRAPER_TIMEOUT=10    # seconds

# File Upload
MAX_FILE_SIZE=5242880  # 5MB in bytes
UPLOAD_PATH=/app/uploads

# Email (optional, for password reset)
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=

# Backup
BACKUP_PATH=/backups
BACKUP_RETENTION_DAYS=30
```

---

**END OF PROMPT**

This comprehensive prompt should provide all necessary information for coding agents to successfully build, test, document, and deploy your household meal planning application. Good luck with your project!
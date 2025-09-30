# Database Schema Documentation

## Overview

The Household Meal Planning System uses PostgreSQL 15+ with a **multi-schema architecture**. This design separates concerns while maintaining a single database for easier backups and cross-application queries.

## Schema Architecture

```
household_db
├── shared/              # Common tables (users, auth, settings)
├── meal_planning/       # Recipe management, inventory, menus
├── chores/              # Future: Chore management (placeholder)
├── learning/            # Future: Learning modules (placeholder)
└── rewards/             # Future: Allowance/rewards (placeholder)
```

### Benefits of Multi-Schema Design

- **Cross-schema queries** for unified dashboard
- **Single database backup** for all applications
- **Shared connection pool** for better resource utilization
- **Clear separation** of application concerns
- **Future extensibility** for additional household apps

---

## SHARED SCHEMA

Contains tables used across all household applications.

### Tables

#### `shared.users`

Stores user accounts for all family members.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique user identifier |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Login username (min 3 chars) |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email address |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'user' | admin \| user \| child |
| is_active | BOOLEAN | DEFAULT true | Account active status |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Account creation |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Last update |
| last_login | TIMESTAMP WITH TIME ZONE | NULL | Last successful login |

**Indexes:**
- `idx_users_username` - Username lookup
- `idx_users_email` - Email lookup
- `idx_users_role` - Role filtering
- `idx_users_active` - Active users only

**Constraints:**
- `chk_role` - Role must be 'admin', 'user', or 'child'
- `chk_username_length` - Username minimum 3 characters
- `chk_email_format` - Valid email format (regex)

#### `shared.sessions`

Manages JWT authentication sessions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Session identifier |
| user_id | UUID | FK → users(id) ON DELETE CASCADE | User owning session |
| token_hash | VARCHAR(255) | NOT NULL | Hashed JWT token |
| expires_at | TIMESTAMP WITH TIME ZONE | NOT NULL | Expiration time |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Session start |
| last_accessed | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Last activity |
| ip_address | INET | NULL | Client IP |
| user_agent | TEXT | NULL | Browser/device info |

**Indexes:**
- `idx_sessions_user_id` - Find user sessions
- `idx_sessions_token_hash` - Token validation
- `idx_sessions_expires_at` - Cleanup expired sessions

#### `shared.user_activity_log`

Audit trail of user actions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Log entry ID |
| user_id | UUID | FK → users(id) ON DELETE SET NULL | Acting user |
| action | VARCHAR(100) | NOT NULL | Action performed |
| entity_type | VARCHAR(50) | NULL | Entity type (recipe, inventory, etc.) |
| entity_id | UUID | NULL | Entity ID |
| details | JSONB | NULL | Additional context |
| ip_address | INET | NULL | Client IP |
| timestamp | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | When action occurred |

**Indexes:**
- `idx_activity_log_user_id` - User activity
- `idx_activity_log_timestamp` - Recent activity (DESC)
- `idx_activity_log_action` - Action filtering
- `idx_activity_log_entity` - Entity lookups

#### `shared.system_settings`

Global system configuration.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Setting ID |
| key | VARCHAR(100) | UNIQUE, NOT NULL | Setting key |
| value | JSONB | NOT NULL | Setting value (flexible type) |
| description | TEXT | NULL | Human-readable description |
| updated_by | UUID | FK → users(id) | Last modifier |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Last update |

**Default Settings:**
- `app.name`: "Household Meal Planning System"
- `app.version`: "1.0.0"
- `session.timeout_hours`: 24
- `session.max_concurrent`: 5

---

## MEAL_PLANNING SCHEMA

Core application schema for recipe management, inventory, and menu planning.

### Entity Relationship Diagram

```
users (shared.users)
  ├──> recipes (created_by)
  ├──> recipe_versions (modified_by)
  ├──> ratings (user_id)
  ├──> menu_plans (created_by)
  └──> planned_meals (cooked_by)

recipes
  ├──> recipe_versions (recipe_id) [1:N]
  ├──> recipe_tags (recipe_id) [1:N]
  ├──> recipe_images (recipe_id) [1:N]
  ├──> ratings (recipe_id) [1:N]
  └──> planned_meals (recipe_id) [1:N]

recipe_versions
  └──> ingredients (recipe_version_id) [1:N]

inventory
  └──> inventory_history (inventory_id) [1:N]

menu_plans
  └──> planned_meals (menu_plan_id) [1:N]
```

### Tables

#### `meal_planning.recipes`

Main recipe metadata with version tracking.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Recipe ID |
| title | VARCHAR(255) | NOT NULL | Recipe name |
| description | TEXT | NULL | Brief description |
| source_url | VARCHAR(500) | NULL | Original URL (if scraped) |
| source_type | VARCHAR(20) | DEFAULT 'manual' | manual \| scraped |
| created_by | UUID | FK → shared.users(id) | Creator |
| current_version | INTEGER | NOT NULL, DEFAULT 1 | Latest version number |
| is_deleted | BOOLEAN | DEFAULT false | Soft delete flag |
| last_cooked_date | DATE | NULL | For rotation tracking |
| times_cooked | INTEGER | DEFAULT 0 | Cooking counter |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Creation time |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Last update |

**Indexes:**
- `idx_recipes_title` - Title search
- `idx_recipes_created_by` - Creator lookup
- `idx_recipes_last_cooked` - Rotation queries (DESC NULLS LAST)
- `idx_recipes_is_deleted` - Active recipes only
- `idx_recipes_search` - Full-text search (GIN index on title + description)

**Special Features:**
- **Full-text search** using PostgreSQL's `to_tsvector`
- **Soft delete** with `is_deleted` flag
- **Rotation tracking** via `last_cooked_date` and `times_cooked`

#### `meal_planning.recipe_versions`

Complete history of recipe changes (versioning system).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Version ID |
| recipe_id | UUID | FK → recipes(id) ON DELETE CASCADE | Parent recipe |
| version_number | INTEGER | NOT NULL | Version sequence (1, 2, 3, ...) |
| prep_time_minutes | INTEGER | CHECK >= 0 | Preparation time |
| cook_time_minutes | INTEGER | CHECK >= 0 | Cooking time |
| total_time_minutes | INTEGER | GENERATED ALWAYS AS (prep + cook) | Auto-calculated |
| servings | INTEGER | CHECK > 0 | Number of servings |
| difficulty | VARCHAR(20) | CHECK IN ('easy', 'medium', 'hard') | Difficulty level |
| instructions | TEXT | NOT NULL | Step-by-step instructions |
| change_description | TEXT | NULL | What changed in this version |
| nutritional_info | JSONB | NULL | Optional nutrition data |
| modified_by | UUID | FK → shared.users(id) | Who made this version |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Version created |

**Unique Constraint:**
- `(recipe_id, version_number)` - One version number per recipe

**Indexes:**
- `idx_recipe_versions_recipe_id` - Find all versions of recipe
- `idx_recipe_versions_version_number` - Latest version queries (DESC)

**Version Management:**
- Each update creates a **new version**
- Default view shows `current_version`
- Users can **revert to previous versions**
- Complete **snapshot** of recipe at each version

#### `meal_planning.ingredients`

Ingredients linked to specific recipe versions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Ingredient ID |
| recipe_version_id | UUID | FK → recipe_versions(id) ON DELETE CASCADE | Parent version |
| name | VARCHAR(255) | NOT NULL | Ingredient name |
| quantity | DECIMAL(10, 3) | CHECK > 0 | Amount needed |
| unit | VARCHAR(50) | NULL | Unit (cup, tbsp, oz, etc.) |
| category | VARCHAR(50) | NULL | produce, dairy, meat, etc. |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | Display sequence |
| is_optional | BOOLEAN | DEFAULT false | Optional ingredient flag |

**Indexes:**
- `idx_ingredients_recipe_version` - Find ingredients for version
- `idx_ingredients_name` - Ingredient name search
- `idx_ingredients_category` - Category filtering
- `idx_ingredients_display_order` - Ordered display

#### `meal_planning.recipe_tags`

Categories and tags for recipe filtering.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Tag ID |
| recipe_id | UUID | FK → recipes(id) ON DELETE CASCADE | Tagged recipe |
| tag | VARCHAR(50) | NOT NULL | Tag name |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Tag added |

**Unique Constraint:**
- `(recipe_id, tag)` - No duplicate tags per recipe

**Common Tags:**
- Meal type: breakfast, lunch, dinner, snack, dessert
- Dietary: vegetarian, vegan, gluten-free, dairy-free
- Cuisine: italian, mexican, chinese, indian
- Speed: quick-meals (< 30 min), slow-cooker
- Season: summer, winter, holiday

#### `meal_planning.recipe_images`

Multiple images per recipe.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Image ID |
| recipe_id | UUID | FK → recipes(id) ON DELETE CASCADE | Parent recipe |
| image_path | VARCHAR(500) | NOT NULL | File path/URL |
| is_primary | BOOLEAN | DEFAULT false | Main recipe image |
| display_order | INTEGER | DEFAULT 0 | Display sequence |
| uploaded_by | UUID | FK → shared.users(id) | Uploader |
| uploaded_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Upload time |

**Indexes:**
- `idx_recipe_images_recipe_id` - Find images for recipe
- `idx_recipe_images_primary` - Quick primary image lookup

#### `meal_planning.inventory`

Current kitchen inventory items.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Item ID |
| item_name | VARCHAR(255) | NOT NULL | Item name |
| quantity | DECIMAL(10, 3) | NOT NULL, DEFAULT 0, CHECK >= 0 | Current amount |
| unit | VARCHAR(50) | NULL | Unit of measurement |
| category | VARCHAR(50) | NULL | Item category |
| location | VARCHAR(50) | CHECK IN ('pantry', 'fridge', 'freezer', 'other') | Storage location |
| expiration_date | DATE | NULL | Expiration date |
| minimum_stock | DECIMAL(10, 3) | DEFAULT 0, CHECK >= 0 | Low stock threshold |
| notes | TEXT | NULL | Additional notes |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Item added |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Last updated |

**Indexes:**
- `idx_inventory_item_name` - Name search
- `idx_inventory_category` - Category filtering
- `idx_inventory_location` - Location filtering
- `idx_inventory_expiration` - Expiration queries
- `idx_inventory_low_stock` - Low stock alerts (`quantity <= minimum_stock`)

#### `meal_planning.inventory_history`

Track all quantity changes over time.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | History entry ID |
| inventory_id | UUID | FK → inventory(id) ON DELETE CASCADE | Item |
| change_type | VARCHAR(20) | NOT NULL, CHECK IN ('purchased', 'used', 'expired', 'adjusted', 'auto_deducted') | Change reason |
| quantity_before | DECIMAL(10, 3) | NOT NULL | Quantity before change |
| quantity_after | DECIMAL(10, 3) | NOT NULL | Quantity after change |
| quantity_change | DECIMAL(10, 3) | GENERATED ALWAYS AS (after - before) | Calculated delta |
| reason | VARCHAR(100) | NULL | Additional context |
| changed_by | UUID | FK → shared.users(id) | Who made change |
| changed_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | When changed |

**Indexes:**
- `idx_inventory_history_inventory_id` - Item history
- `idx_inventory_history_changed_at` - Recent changes (DESC)
- `idx_inventory_history_change_type` - Filter by type

**Automatic Tracking:**
- Trigger captures all quantity changes
- Manual adjustments logged as 'adjusted'
- Cooking deducts logged as 'auto_deducted'

#### `meal_planning.ratings`

User-specific recipe ratings (thumbs up/down, not averaged).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Rating ID |
| recipe_id | UUID | FK → recipes(id) ON DELETE CASCADE | Rated recipe |
| user_id | UUID | FK → shared.users(id) ON DELETE CASCADE | Rating user |
| rating | BOOLEAN | NOT NULL | true = 👍, false = 👎 |
| feedback | TEXT | NULL | Comments |
| modifications | TEXT | NULL | Suggested changes |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Rating created |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Rating updated |

**Unique Constraint:**
- `(recipe_id, user_id)` - One rating per user per recipe

**Indexes:**
- `idx_ratings_recipe_id` - Find ratings for recipe
- `idx_ratings_user_id` - Find user's ratings
- `idx_ratings_rating` - Filter by thumbs up/down

**Important:** Ratings are **not averaged**. Each user's rating is stored individually.

#### `meal_planning.menu_plans`

Weekly meal plans.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Menu plan ID |
| week_start_date | DATE | NOT NULL, CHECK (ISODOW = 1) | Monday of week |
| week_end_date | DATE | GENERATED ALWAYS AS (start + 6 days) | Sunday of week |
| name | VARCHAR(100) | NULL | Optional plan name |
| created_by | UUID | FK → shared.users(id) | Creator |
| is_active | BOOLEAN | DEFAULT true | Active plan flag |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Plan created |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Plan updated |

**Constraints:**
- `chk_week_start_monday` - Week must start on Monday

**Indexes:**
- `idx_menu_plans_week_start` - Find plans by week (DESC)
- `idx_menu_plans_created_by` - User's plans
- `idx_menu_plans_active` - Active plans only

#### `meal_planning.planned_meals`

Individual meals in menu plans.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Planned meal ID |
| menu_plan_id | UUID | FK → menu_plans(id) ON DELETE CASCADE | Parent plan |
| recipe_id | UUID | FK → recipes(id) ON DELETE CASCADE | Recipe to cook |
| meal_date | DATE | NOT NULL | Date of meal |
| meal_type | VARCHAR(20) | NOT NULL, CHECK IN ('breakfast', 'lunch', 'dinner', 'snack') | Meal slot |
| servings_planned | INTEGER | CHECK > 0 | Servings to make |
| notes | TEXT | NULL | Meal notes |
| cooked | BOOLEAN | DEFAULT false | Whether meal was cooked |
| cooked_date | TIMESTAMP WITH TIME ZONE | NULL | When marked cooked |
| cooked_by | UUID | FK → shared.users(id) | Who cooked it |

**Indexes:**
- `idx_planned_meals_menu_plan` - Find meals in plan
- `idx_planned_meals_recipe` - Usage tracking
- `idx_planned_meals_date` - Date queries
- `idx_planned_meals_cooked` - Cooked status

**Special Logic:**
- When `cooked = true`, inventory auto-deducts ingredients
- Updates `recipes.last_cooked_date` and `recipes.times_cooked`

#### `meal_planning.app_settings`

Meal planning specific configuration.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Settings ID |
| favorites_threshold | DECIMAL(3, 2) | DEFAULT 0.75, CHECK (0-1) | % thumbs up for favorite (75%) |
| favorites_min_raters | INTEGER | DEFAULT 3, CHECK > 0 | Min users to rate (3) |
| rotation_period_days | INTEGER | DEFAULT 14, CHECK > 0 | "Recently cooked" period (14 days) |
| low_stock_threshold_percent | DECIMAL(3, 2) | DEFAULT 0.20, CHECK (0-1) | Low stock % (20%) |
| expiration_warning_days | INTEGER | DEFAULT 7, CHECK >= 0 | Expiration warning (7 days) |
| updated_by | UUID | FK → shared.users(id) | Last modifier |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Last update |

**Default Values:**
- Favorites: 75% thumbs up, 3+ raters
- Rotation: 14 days
- Low stock: 20% of minimum
- Expiration warning: 7 days

---

## VIEWS

### `meal_planning.recipes_with_current_version`

Joins recipes with their current version for easy querying.

```sql
SELECT
    r.id, r.title, r.description, r.source_url,
    rv.prep_time_minutes, rv.cook_time_minutes, rv.servings, rv.difficulty, rv.instructions
FROM recipes r
JOIN recipe_versions rv ON r.id = rv.recipe_id AND r.current_version = rv.version_number
WHERE r.is_deleted = false;
```

### `meal_planning.low_stock_items`

Items below minimum stock level.

```sql
SELECT * FROM inventory
WHERE quantity <= minimum_stock
ORDER BY (minimum_stock - quantity) DESC;
```

### `meal_planning.expiring_items`

Items expiring within warning period.

```sql
SELECT i.*, (expiration_date - CURRENT_DATE) as days_until_expiration
FROM inventory i
WHERE expiration_date <= CURRENT_DATE + (SELECT expiration_warning_days FROM app_settings)
ORDER BY expiration_date ASC;
```

### `meal_planning.recipe_favorites`

Calculates favorite status based on ratings.

```sql
SELECT
    r.id, r.title,
    COUNT(CASE WHEN rt.rating = true THEN 1 END) as thumbs_up_count,
    COUNT(rt.id) as total_ratings,
    (thumbs_up_count / total_ratings) as thumbs_up_percentage,
    CASE WHEN total_ratings >= favorites_min_raters
         AND thumbs_up_percentage >= favorites_threshold
         THEN true ELSE false
    END as is_favorite
FROM recipes r
LEFT JOIN ratings rt ON r.id = rt.recipe_id
GROUP BY r.id;
```

---

## TRIGGERS

### `update_updated_at_column`

Automatically updates `updated_at` timestamp on UPDATE.

Applied to:
- `shared.users`
- `meal_planning.recipes`
- `meal_planning.inventory`
- `meal_planning.ratings`
- `meal_planning.menu_plans`

### `track_inventory_changes`

Automatically logs quantity changes to `inventory_history`.

Applied to: `meal_planning.inventory`

---

## FUTURE SCHEMAS

### `chores` (Placeholder)

Future chore management application.

**Planned tables:**
- `tasks` - Chore definitions
- `assignments` - User assignments
- `completed_tasks` - Completion tracking
- `recurring_schedules` - Recurring patterns

### `learning` (Placeholder)

Future learning/education application.

**Planned tables:**
- `modules` - Learning modules
- `lessons` - Individual lessons
- `user_progress` - Progress tracking
- `assessments` - Quizzes/tests
- `achievements` - Certificates, badges

### `rewards` (Placeholder)

Future allowance/rewards application.

**Planned tables:**
- `user_balances` - Point balances
- `transactions` - Point history
- `allowance_schedules` - Recurring allowance
- `rewards_catalog` - Available rewards
- `redemptions` - Purchase history

---

## Indexes Summary

### Critical Indexes (Performance)

1. **Users**: username, email (authentication)
2. **Recipes**: title search, full-text search, last_cooked (rotation)
3. **Inventory**: low_stock, expiring items
4. **Ratings**: recipe_id, user_id (favorites calculation)
5. **Planned Meals**: menu_plan_id, meal_date

### Index Types

- **B-tree** (default): Exact matches, range queries
- **GIN**: Full-text search (`recipes.title + description`)
- **Partial**: Conditional indexes (e.g., `WHERE is_deleted = false`)

---

## Maintenance

### Regular Tasks

**Daily:**
- Clean expired sessions: `DELETE FROM shared.sessions WHERE expires_at < NOW()`

**Weekly:**
- Vacuum and analyze: `VACUUM ANALYZE`

**Monthly:**
- Reindex: `REINDEX DATABASE household_db`
- Review slow queries: Check `pg_stat_statements`

### Backup Strategy

- **Full backup**: Daily at 2 AM
- **Retention**: 7 daily, 4 weekly, 12 monthly
- **Command**: `pg_dump -Fc household_db > backup_$(date +%Y%m%d).dump`

---

## Migration Strategy

When modifying schema:

1. Create migration script in `database/migrations/`
2. Test on development database
3. Document changes in this file
4. Update API contracts if needed
5. Deploy with backward compatibility
6. Update application code
7. Remove deprecated code after grace period

---

## References

- PostgreSQL Documentation: https://www.postgresql.org/docs/15/
- Schema files: `database/schemas/`
- Initialization: `database/init.sql`
- Seed data: `database/seeds/`

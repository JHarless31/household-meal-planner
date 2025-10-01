-- ============================================================================
-- DATABASE INITIALIZATION SCRIPT
-- Household Meal Planning System
-- ============================================================================
-- This script initializes the complete database structure with all schemas
-- Run this on a fresh PostgreSQL 15+ database

-- ============================================================================
-- DATABASE SETUP
-- ============================================================================

-- Enable UUID extension (required for gen_random_uuid())
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Enable full-text search extensions
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text search
CREATE EXTENSION IF NOT EXISTS "unaccent";  -- For accent-insensitive search

-- ============================================================================
-- EXECUTE SCHEMA SCRIPTS IN ORDER
-- ============================================================================

-- 1. Shared schema (users, authentication, system settings)
\i /docker-entrypoint-initdb.d/schemas/shared.sql

-- 2. Meal planning schema (main application)
\i /docker-entrypoint-initdb.d/schemas/meal_planning.sql

-- 3. Future application schemas (placeholders)
\i /docker-entrypoint-initdb.d/schemas/future_apps.sql

-- ============================================================================
-- GRANT PERMISSIONS
-- ============================================================================

-- Create application role (used by backend API)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'meal_planner_app') THEN
        CREATE ROLE meal_planner_app LOGIN PASSWORD 'CHANGE_ME_IN_PRODUCTION';
    END IF;
END
$$;

-- Grant schema usage
GRANT USAGE ON SCHEMA shared TO meal_planner_app;
GRANT USAGE ON SCHEMA meal_planning TO meal_planner_app;
GRANT USAGE ON SCHEMA chores TO meal_planner_app;
GRANT USAGE ON SCHEMA learning TO meal_planner_app;
GRANT USAGE ON SCHEMA rewards TO meal_planner_app;

-- Grant table permissions (shared schema)
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA shared TO meal_planner_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA shared TO meal_planner_app;

-- Grant table permissions (meal_planning schema)
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA meal_planning TO meal_planner_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA meal_planning TO meal_planner_app;

-- Grant permissions for future schemas
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA chores TO meal_planner_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA learning TO meal_planner_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA rewards TO meal_planner_app;

-- Make grants apply to future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA shared GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO meal_planner_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA meal_planning GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO meal_planner_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA chores GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO meal_planner_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA learning GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO meal_planner_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA rewards GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO meal_planner_app;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- List all schemas
SELECT schema_name
FROM information_schema.schemata
WHERE schema_name IN ('shared', 'meal_planning', 'chores', 'learning', 'rewards')
ORDER BY schema_name;

-- Count tables per schema
SELECT
    schemaname,
    COUNT(*) as table_count
FROM pg_tables
WHERE schemaname IN ('shared', 'meal_planning', 'chores', 'learning', 'rewards')
GROUP BY schemaname
ORDER BY schemaname;

-- ============================================================================
-- COMPLETION MESSAGE
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Database initialization complete!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Schemas created:';
    RAISE NOTICE '  - shared (users, auth, system settings)';
    RAISE NOTICE '  - meal_planning (recipes, inventory, menus)';
    RAISE NOTICE '  - chores (placeholder for future)';
    RAISE NOTICE '  - learning (placeholder for future)';
    RAISE NOTICE '  - rewards (placeholder for future)';
    RAISE NOTICE '';
    RAISE NOTICE 'Next steps:';
    RAISE NOTICE '  1. Change default password for meal_planner_app role';
    RAISE NOTICE '  2. Create initial admin user via backend API';
    RAISE NOTICE '  3. Run seed data script if needed';
    RAISE NOTICE '========================================';
END
$$;

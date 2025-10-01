-- ============================================================================
-- FUTURE APPLICATION SCHEMAS (Placeholders)
-- ============================================================================
-- These schemas support future household management applications
-- They are created now to establish the multi-schema architecture

-- ============================================================================
-- CHORES SCHEMA: Task assignments and tracking
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS chores;

COMMENT ON SCHEMA chores IS 'Future: Chore management application (task assignments, completion tracking, schedules)';

-- Placeholder table to establish schema
CREATE TABLE chores.app_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status VARCHAR(20) DEFAULT 'planned',
    description TEXT DEFAULT 'Chore management: task assignments, completion tracking, recurring schedules, point/reward integration',
    planned_features JSONB DEFAULT '[
        "Task assignment to family members",
        "Recurring schedule support",
        "Completion tracking with verification",
        "Point rewards for completed chores",
        "Age-appropriate task suggestions",
        "Notification reminders"
    ]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO chores.app_info (status) VALUES ('planned');

-- ============================================================================
-- LEARNING SCHEMA: Educational content and progress tracking
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS learning;

COMMENT ON SCHEMA learning IS 'Future: Personal learning application (modules, progress tracking, assessments)';

-- Placeholder table
CREATE TABLE learning.app_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status VARCHAR(20) DEFAULT 'planned',
    description TEXT DEFAULT 'Personal learning: educational modules, progress tracking, quizzes, achievements',
    planned_features JSONB DEFAULT '[
        "Learning modules/courses",
        "Progress tracking per user",
        "Quiz and assessment system",
        "Certificates and achievements",
        "Age-appropriate content",
        "Learning goals and milestones"
    ]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO learning.app_info (status) VALUES ('planned');

-- ============================================================================
-- REWARDS SCHEMA: Allowance and reward tracking
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS rewards;

COMMENT ON SCHEMA rewards IS 'Future: Rewards and allowance application (point balance, purchases, allowance scheduling)';

-- Placeholder table
CREATE TABLE rewards.app_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status VARCHAR(20) DEFAULT 'planned',
    description TEXT DEFAULT 'Rewards and allowance: point balance tracking, allowance scheduling, purchase history',
    planned_features JSONB DEFAULT '[
        "Point balance per user",
        "Allowance scheduling (weekly/monthly)",
        "Purchase/redemption history",
        "Chore completion bonuses",
        "Savings goals",
        "Virtual or physical rewards catalog"
    ]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO rewards.app_info (status) VALUES ('planned');

-- ============================================================================
-- CROSS-SCHEMA INTEGRATION NOTES
-- ============================================================================

/*
Future integration points between applications:

1. CHORES + REWARDS:
   - Completed chores award points
   - Query: SELECT chore_id, points FROM chores.completed_tasks JOIN rewards.point_transactions

2. MEAL_PLANNING + CHORES:
   - Cooking assigned as chore
   - Query: SELECT recipe_id FROM meal_planning.planned_meals WHERE assigned_to_chore IS NOT NULL

3. LEARNING + REWARDS:
   - Completed lessons award points
   - Query: SELECT lesson_id, points FROM learning.completed_lessons JOIN rewards.point_transactions

4. DASHBOARD (future):
   - Aggregate data from all schemas
   - Single query across shared.users + meal_planning + chores + learning + rewards

Example unified dashboard query:
SELECT
    u.username,
    (SELECT COUNT(*) FROM meal_planning.planned_meals pm WHERE pm.cooked = true AND pm.cooked_by = u.id) as meals_cooked,
    (SELECT COUNT(*) FROM chores.completed_tasks ct WHERE ct.user_id = u.id) as chores_completed,
    (SELECT COUNT(*) FROM learning.completed_lessons cl WHERE cl.user_id = u.id) as lessons_completed,
    (SELECT balance FROM rewards.user_balances rb WHERE rb.user_id = u.id) as point_balance
FROM shared.users u
WHERE u.is_active = true;

*/

-- ============================================================================
-- MIGRATION PATH
-- ============================================================================

/*
When implementing future applications:

1. Create detailed tables in respective schemas
2. Add foreign keys to shared.users(id)
3. Create indexes for performance
4. Add triggers for audit logging
5. Create views for common queries
6. Update docs/DATABASE_SCHEMA.md
7. Add API endpoints in docs/API_SPEC.yaml
8. Implement backend services
9. Build frontend UI components
10. Update shared dashboard

Example: Implementing chores schema

CREATE TABLE chores.tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    assigned_to UUID REFERENCES shared.users(id),
    due_date DATE,
    recurring_schedule VARCHAR(50),
    points_reward INTEGER DEFAULT 0,
    created_by UUID REFERENCES shared.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chores.completed_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES chores.tasks(id),
    user_id UUID REFERENCES shared.users(id),
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    verified_by UUID REFERENCES shared.users(id),
    notes TEXT
);

*/

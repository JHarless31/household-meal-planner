-- ============================================================================
-- MEAL_PLANNING SCHEMA: Recipe management, inventory, menus, and ratings
-- ============================================================================

-- Create meal_planning schema
CREATE SCHEMA IF NOT EXISTS meal_planning;

-- Set search path
SET search_path TO meal_planning, shared, public;

-- ============================================================================
-- RECIPES TABLE (main recipe metadata)
-- ============================================================================
CREATE TABLE meal_planning.recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    source_url VARCHAR(500),
    source_type VARCHAR(20) DEFAULT 'manual',
    created_by UUID NOT NULL REFERENCES shared.users(id) ON DELETE SET NULL,
    current_version INTEGER NOT NULL DEFAULT 1,
    is_deleted BOOLEAN DEFAULT false,
    last_cooked_date DATE,
    times_cooked INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_source_type CHECK (source_type IN ('manual', 'scraped')),
    CONSTRAINT chk_current_version_positive CHECK (current_version > 0),
    CONSTRAINT chk_times_cooked_non_negative CHECK (times_cooked >= 0)
);

-- Indexes for recipes
CREATE INDEX idx_recipes_title ON meal_planning.recipes(title);
CREATE INDEX idx_recipes_created_by ON meal_planning.recipes(created_by);
CREATE INDEX idx_recipes_last_cooked ON meal_planning.recipes(last_cooked_date DESC NULLS LAST);
CREATE INDEX idx_recipes_is_deleted ON meal_planning.recipes(is_deleted) WHERE is_deleted = false;
CREATE INDEX idx_recipes_created_at ON meal_planning.recipes(created_at DESC);

-- Full-text search index on title and description
CREATE INDEX idx_recipes_search ON meal_planning.recipes USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')));

-- ============================================================================
-- RECIPE VERSIONS TABLE (complete history of recipe changes)
-- ============================================================================
CREATE TABLE meal_planning.recipe_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID NOT NULL REFERENCES meal_planning.recipes(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    prep_time_minutes INTEGER,
    cook_time_minutes INTEGER,
    total_time_minutes INTEGER GENERATED ALWAYS AS (COALESCE(prep_time_minutes, 0) + COALESCE(cook_time_minutes, 0)) STORED,
    servings INTEGER,
    difficulty VARCHAR(20),
    instructions TEXT NOT NULL,
    change_description TEXT,
    nutritional_info JSONB,
    modified_by UUID NOT NULL REFERENCES shared.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_version_positive CHECK (version_number > 0),
    CONSTRAINT chk_difficulty CHECK (difficulty IN ('easy', 'medium', 'hard')),
    CONSTRAINT chk_prep_time CHECK (prep_time_minutes IS NULL OR prep_time_minutes >= 0),
    CONSTRAINT chk_cook_time CHECK (cook_time_minutes IS NULL OR cook_time_minutes >= 0),
    CONSTRAINT chk_servings CHECK (servings IS NULL OR servings > 0),
    UNIQUE (recipe_id, version_number)
);

-- Indexes for recipe versions
CREATE INDEX idx_recipe_versions_recipe_id ON meal_planning.recipe_versions(recipe_id);
CREATE INDEX idx_recipe_versions_version_number ON meal_planning.recipe_versions(recipe_id, version_number DESC);

-- ============================================================================
-- INGREDIENTS TABLE (linked to specific recipe versions)
-- ============================================================================
CREATE TABLE meal_planning.ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_version_id UUID NOT NULL REFERENCES meal_planning.recipe_versions(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    quantity DECIMAL(10, 3),
    unit VARCHAR(50),
    category VARCHAR(50),
    display_order INTEGER NOT NULL DEFAULT 0,
    is_optional BOOLEAN DEFAULT false,

    CONSTRAINT chk_quantity CHECK (quantity IS NULL OR quantity > 0)
);

-- Indexes for ingredients
CREATE INDEX idx_ingredients_recipe_version ON meal_planning.ingredients(recipe_version_id);
CREATE INDEX idx_ingredients_name ON meal_planning.ingredients(name);
CREATE INDEX idx_ingredients_category ON meal_planning.ingredients(category);
CREATE INDEX idx_ingredients_display_order ON meal_planning.ingredients(recipe_version_id, display_order);

-- ============================================================================
-- RECIPE TAGS TABLE (for categorization and filtering)
-- ============================================================================
CREATE TABLE meal_planning.recipe_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID NOT NULL REFERENCES meal_planning.recipes(id) ON DELETE CASCADE,
    tag VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (recipe_id, tag)
);

-- Indexes for recipe tags
CREATE INDEX idx_recipe_tags_recipe_id ON meal_planning.recipe_tags(recipe_id);
CREATE INDEX idx_recipe_tags_tag ON meal_planning.recipe_tags(tag);

-- ============================================================================
-- RECIPE IMAGES TABLE (multiple images per recipe)
-- ============================================================================
CREATE TABLE meal_planning.recipe_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID NOT NULL REFERENCES meal_planning.recipes(id) ON DELETE CASCADE,
    image_path VARCHAR(500) NOT NULL,
    is_primary BOOLEAN DEFAULT false,
    display_order INTEGER DEFAULT 0,
    uploaded_by UUID REFERENCES shared.users(id),
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for recipe images
CREATE INDEX idx_recipe_images_recipe_id ON meal_planning.recipe_images(recipe_id);
CREATE INDEX idx_recipe_images_primary ON meal_planning.recipe_images(recipe_id, is_primary) WHERE is_primary = true;

-- ============================================================================
-- INVENTORY TABLE (current kitchen inventory)
-- ============================================================================
CREATE TABLE meal_planning.inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_name VARCHAR(255) NOT NULL,
    quantity DECIMAL(10, 3) NOT NULL DEFAULT 0,
    unit VARCHAR(50),
    category VARCHAR(50),
    location VARCHAR(50),
    expiration_date DATE,
    minimum_stock DECIMAL(10, 3) DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_quantity_non_negative CHECK (quantity >= 0),
    CONSTRAINT chk_minimum_stock_non_negative CHECK (minimum_stock >= 0),
    CONSTRAINT chk_location CHECK (location IN ('pantry', 'fridge', 'freezer', 'other'))
);

-- Indexes for inventory
CREATE INDEX idx_inventory_item_name ON meal_planning.inventory(item_name);
CREATE INDEX idx_inventory_category ON meal_planning.inventory(category);
CREATE INDEX idx_inventory_location ON meal_planning.inventory(location);
CREATE INDEX idx_inventory_expiration ON meal_planning.inventory(expiration_date) WHERE expiration_date IS NOT NULL;
CREATE INDEX idx_inventory_low_stock ON meal_planning.inventory(quantity, minimum_stock) WHERE quantity <= minimum_stock;

-- ============================================================================
-- INVENTORY HISTORY TABLE (track quantity changes)
-- ============================================================================
CREATE TABLE meal_planning.inventory_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    inventory_id UUID NOT NULL REFERENCES meal_planning.inventory(id) ON DELETE CASCADE,
    change_type VARCHAR(20) NOT NULL,
    quantity_before DECIMAL(10, 3) NOT NULL,
    quantity_after DECIMAL(10, 3) NOT NULL,
    quantity_change DECIMAL(10, 3) GENERATED ALWAYS AS (quantity_after - quantity_before) STORED,
    reason VARCHAR(100),
    changed_by UUID REFERENCES shared.users(id),
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_change_type CHECK (change_type IN ('purchased', 'used', 'expired', 'adjusted', 'auto_deducted'))
);

-- Indexes for inventory history
CREATE INDEX idx_inventory_history_inventory_id ON meal_planning.inventory_history(inventory_id);
CREATE INDEX idx_inventory_history_changed_at ON meal_planning.inventory_history(changed_at DESC);
CREATE INDEX idx_inventory_history_change_type ON meal_planning.inventory_history(change_type);

-- ============================================================================
-- RATINGS TABLE (user-specific ratings, not averaged)
-- ============================================================================
CREATE TABLE meal_planning.ratings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID NOT NULL REFERENCES meal_planning.recipes(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES shared.users(id) ON DELETE CASCADE,
    rating BOOLEAN NOT NULL,
    feedback TEXT,
    modifications TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (recipe_id, user_id)
);

-- Indexes for ratings
CREATE INDEX idx_ratings_recipe_id ON meal_planning.ratings(recipe_id);
CREATE INDEX idx_ratings_user_id ON meal_planning.ratings(user_id);
CREATE INDEX idx_ratings_rating ON meal_planning.ratings(recipe_id, rating);

-- ============================================================================
-- MENU PLANS TABLE (weekly meal planning)
-- ============================================================================
CREATE TABLE meal_planning.menu_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    week_start_date DATE NOT NULL,
    week_end_date DATE GENERATED ALWAYS AS (week_start_date + INTERVAL '6 days') STORED,
    name VARCHAR(100),
    created_by UUID NOT NULL REFERENCES shared.users(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_week_start_monday CHECK (EXTRACT(ISODOW FROM week_start_date) = 1)
);

-- Indexes for menu plans
CREATE INDEX idx_menu_plans_week_start ON meal_planning.menu_plans(week_start_date DESC);
CREATE INDEX idx_menu_plans_created_by ON meal_planning.menu_plans(created_by);
CREATE INDEX idx_menu_plans_active ON meal_planning.menu_plans(is_active) WHERE is_active = true;

-- ============================================================================
-- PLANNED MEALS TABLE (individual meals in menu plans)
-- ============================================================================
CREATE TABLE meal_planning.planned_meals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    menu_plan_id UUID NOT NULL REFERENCES meal_planning.menu_plans(id) ON DELETE CASCADE,
    recipe_id UUID NOT NULL REFERENCES meal_planning.recipes(id) ON DELETE CASCADE,
    meal_date DATE NOT NULL,
    meal_type VARCHAR(20) NOT NULL,
    servings_planned INTEGER,
    notes TEXT,
    cooked BOOLEAN DEFAULT false,
    cooked_date TIMESTAMP WITH TIME ZONE,
    cooked_by UUID REFERENCES shared.users(id),

    CONSTRAINT chk_meal_type CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
    CONSTRAINT chk_servings_positive CHECK (servings_planned IS NULL OR servings_planned > 0),
    CONSTRAINT chk_cooked_date CHECK (cooked = false OR cooked_date IS NOT NULL)
);

-- Indexes for planned meals
CREATE INDEX idx_planned_meals_menu_plan ON meal_planning.planned_meals(menu_plan_id);
CREATE INDEX idx_planned_meals_recipe ON meal_planning.planned_meals(recipe_id);
CREATE INDEX idx_planned_meals_date ON meal_planning.planned_meals(meal_date);
CREATE INDEX idx_planned_meals_cooked ON meal_planning.planned_meals(cooked);

-- ============================================================================
-- APP SETTINGS TABLE (meal planning specific configuration)
-- ============================================================================
CREATE TABLE meal_planning.app_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    favorites_threshold DECIMAL(3, 2) DEFAULT 0.75,
    favorites_min_raters INTEGER DEFAULT 3,
    rotation_period_days INTEGER DEFAULT 14,
    low_stock_threshold_percent DECIMAL(3, 2) DEFAULT 0.20,
    expiration_warning_days INTEGER DEFAULT 7,
    updated_by UUID REFERENCES shared.users(id),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_favorites_threshold CHECK (favorites_threshold >= 0 AND favorites_threshold <= 1),
    CONSTRAINT chk_favorites_min_raters CHECK (favorites_min_raters > 0),
    CONSTRAINT chk_rotation_period CHECK (rotation_period_days > 0),
    CONSTRAINT chk_low_stock_threshold CHECK (low_stock_threshold_percent >= 0 AND low_stock_threshold_percent <= 1),
    CONSTRAINT chk_expiration_warning CHECK (expiration_warning_days >= 0)
);

-- Insert default settings
INSERT INTO meal_planning.app_settings (id) VALUES (gen_random_uuid())
ON CONFLICT DO NOTHING;

-- ============================================================================
-- TRIGGER FUNCTIONS
-- ============================================================================

-- Update updated_at timestamp
CREATE OR REPLACE FUNCTION meal_planning.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply triggers
CREATE TRIGGER update_recipes_updated_at
    BEFORE UPDATE ON meal_planning.recipes
    FOR EACH ROW
    EXECUTE FUNCTION meal_planning.update_updated_at_column();

CREATE TRIGGER update_inventory_updated_at
    BEFORE UPDATE ON meal_planning.inventory
    FOR EACH ROW
    EXECUTE FUNCTION meal_planning.update_updated_at_column();

CREATE TRIGGER update_ratings_updated_at
    BEFORE UPDATE ON meal_planning.ratings
    FOR EACH ROW
    EXECUTE FUNCTION meal_planning.update_updated_at_column();

CREATE TRIGGER update_menu_plans_updated_at
    BEFORE UPDATE ON meal_planning.menu_plans
    FOR EACH ROW
    EXECUTE FUNCTION meal_planning.update_updated_at_column();

-- Track inventory changes automatically
CREATE OR REPLACE FUNCTION meal_planning.track_inventory_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.quantity != NEW.quantity THEN
        INSERT INTO meal_planning.inventory_history (
            inventory_id,
            change_type,
            quantity_before,
            quantity_after,
            reason
        ) VALUES (
            NEW.id,
            'adjusted',
            OLD.quantity,
            NEW.quantity,
            'Manual adjustment'
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER track_inventory_quantity_changes
    AFTER UPDATE ON meal_planning.inventory
    FOR EACH ROW
    WHEN (OLD.quantity IS DISTINCT FROM NEW.quantity)
    EXECUTE FUNCTION meal_planning.track_inventory_changes();

-- ============================================================================
-- VIEWS
-- ============================================================================

-- View: Current recipes with latest version info
CREATE OR REPLACE VIEW meal_planning.recipes_with_current_version AS
SELECT
    r.id,
    r.title,
    r.description,
    r.source_url,
    r.source_type,
    r.created_by,
    r.current_version,
    r.last_cooked_date,
    r.times_cooked,
    rv.prep_time_minutes,
    rv.cook_time_minutes,
    rv.total_time_minutes,
    rv.servings,
    rv.difficulty,
    rv.instructions,
    r.created_at,
    r.updated_at
FROM meal_planning.recipes r
JOIN meal_planning.recipe_versions rv ON r.id = rv.recipe_id AND r.current_version = rv.version_number
WHERE r.is_deleted = false;

-- View: Low stock inventory items
CREATE OR REPLACE VIEW meal_planning.low_stock_items AS
SELECT *
FROM meal_planning.inventory
WHERE quantity <= minimum_stock
ORDER BY (minimum_stock - quantity) DESC;

-- View: Expiring items
CREATE OR REPLACE VIEW meal_planning.expiring_items AS
SELECT
    i.*,
    (expiration_date - CURRENT_DATE) as days_until_expiration
FROM meal_planning.inventory i
WHERE expiration_date IS NOT NULL
  AND expiration_date <= CURRENT_DATE + INTERVAL '7 days'
ORDER BY expiration_date ASC;

-- View: Recipe favorites calculation
CREATE OR REPLACE VIEW meal_planning.recipe_favorites AS
SELECT
    r.id as recipe_id,
    r.title,
    COUNT(CASE WHEN rt.rating = true THEN 1 END) as thumbs_up_count,
    COUNT(CASE WHEN rt.rating = false THEN 1 END) as thumbs_down_count,
    COUNT(rt.id) as total_ratings,
    CASE
        WHEN COUNT(rt.id) >= (SELECT favorites_min_raters FROM meal_planning.app_settings LIMIT 1)
        THEN CAST(COUNT(CASE WHEN rt.rating = true THEN 1 END) AS DECIMAL) / COUNT(rt.id)
        ELSE NULL
    END as thumbs_up_percentage,
    CASE
        WHEN COUNT(rt.id) >= (SELECT favorites_min_raters FROM meal_planning.app_settings LIMIT 1)
             AND CAST(COUNT(CASE WHEN rt.rating = true THEN 1 END) AS DECIMAL) / COUNT(rt.id)
                 >= (SELECT favorites_threshold FROM meal_planning.app_settings LIMIT 1)
        THEN true
        ELSE false
    END as is_favorite
FROM meal_planning.recipes r
LEFT JOIN meal_planning.ratings rt ON r.id = rt.recipe_id
WHERE r.is_deleted = false
GROUP BY r.id, r.title;

-- ============================================================================
-- ADDITIONAL PERFORMANCE INDEXES (Phase 4 Optimizations)
-- ============================================================================

-- Composite index for recipe suggestions by rotation
CREATE INDEX IF NOT EXISTS idx_recipes_rotation ON meal_planning.recipes(is_deleted, last_cooked_date ASC NULLS FIRST, times_cooked ASC);

-- Index for rating aggregations (favorites view)
CREATE INDEX IF NOT EXISTS idx_ratings_recipe_rating ON meal_planning.ratings(recipe_id, rating);

-- Index for menu plan queries by date range
CREATE INDEX IF NOT EXISTS idx_menu_plans_week ON meal_planning.menu_plans(week_start_date DESC, is_active);

-- Index for planned meals by date range
CREATE INDEX IF NOT EXISTS idx_planned_meals_date ON meal_planning.planned_meals(meal_date, cooked);

-- Index for inventory low stock queries
CREATE INDEX IF NOT EXISTS idx_inventory_threshold ON meal_planning.inventory(quantity, threshold) WHERE quantity <= threshold;

-- Composite index for recipe search and filtering
CREATE INDEX IF NOT EXISTS idx_recipes_filter ON meal_planning.recipes(is_deleted, current_version) WHERE is_deleted = false;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON SCHEMA meal_planning IS 'Meal planning application schema: recipes, inventory, menus, ratings';
COMMENT ON TABLE meal_planning.recipes IS 'Main recipe table with metadata and current version tracking';
COMMENT ON TABLE meal_planning.recipe_versions IS 'Complete history of recipe versions with snapshots';
COMMENT ON TABLE meal_planning.ingredients IS 'Ingredients linked to specific recipe versions';
COMMENT ON TABLE meal_planning.inventory IS 'Current kitchen inventory items';
COMMENT ON TABLE meal_planning.ratings IS 'User-specific recipe ratings (thumbs up/down, not averaged)';
COMMENT ON TABLE meal_planning.menu_plans IS 'Weekly meal plans';
COMMENT ON TABLE meal_planning.planned_meals IS 'Individual meals in menu plans';

COMMENT ON COLUMN meal_planning.recipes.current_version IS 'Tracks the current/latest version number';
COMMENT ON COLUMN meal_planning.recipes.last_cooked_date IS 'For recipe rotation tracking';
COMMENT ON COLUMN meal_planning.recipes.times_cooked IS 'Incremented each time recipe is marked as cooked';
COMMENT ON COLUMN meal_planning.ratings.rating IS 'Boolean: true = thumbs up, false = thumbs down';
COMMENT ON COLUMN meal_planning.inventory_history.change_type IS 'purchased, used, expired, adjusted, auto_deducted';

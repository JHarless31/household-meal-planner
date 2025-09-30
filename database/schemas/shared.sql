-- ============================================================================
-- SHARED SCHEMA: Common tables used across all household applications
-- ============================================================================

-- Create shared schema
CREATE SCHEMA IF NOT EXISTS shared;

-- Set search path
SET search_path TO shared, public;

-- ============================================================================
-- USERS TABLE
-- ============================================================================
CREATE TABLE shared.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,

    CONSTRAINT chk_role CHECK (role IN ('admin', 'user', 'child')),
    CONSTRAINT chk_username_length CHECK (char_length(username) >= 3),
    CONSTRAINT chk_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Indexes for users table
CREATE INDEX idx_users_username ON shared.users(username);
CREATE INDEX idx_users_email ON shared.users(email);
CREATE INDEX idx_users_role ON shared.users(role);
CREATE INDEX idx_users_active ON shared.users(is_active);

-- ============================================================================
-- SESSIONS TABLE (for JWT token management)
-- ============================================================================
CREATE TABLE shared.sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES shared.users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT,

    CONSTRAINT chk_expires_future CHECK (expires_at > created_at)
);

-- Indexes for sessions table
CREATE INDEX idx_sessions_user_id ON shared.sessions(user_id);
CREATE INDEX idx_sessions_token_hash ON shared.sessions(token_hash);
CREATE INDEX idx_sessions_expires_at ON shared.sessions(expires_at);

-- ============================================================================
-- USER ACTIVITY LOG (for audit trail)
-- ============================================================================
CREATE TABLE shared.user_activity_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES shared.users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    details JSONB,
    ip_address INET,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for activity log
CREATE INDEX idx_activity_log_user_id ON shared.user_activity_log(user_id);
CREATE INDEX idx_activity_log_timestamp ON shared.user_activity_log(timestamp DESC);
CREATE INDEX idx_activity_log_action ON shared.user_activity_log(action);
CREATE INDEX idx_activity_log_entity ON shared.user_activity_log(entity_type, entity_id);

-- ============================================================================
-- SYSTEM SETTINGS (global configuration)
-- ============================================================================
CREATE TABLE shared.system_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key VARCHAR(100) UNIQUE NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    updated_by UUID REFERENCES shared.users(id),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for system settings
CREATE INDEX idx_system_settings_key ON shared.system_settings(key);

-- ============================================================================
-- TRIGGER FUNCTIONS
-- ============================================================================

-- Update updated_at timestamp automatically
CREATE OR REPLACE FUNCTION shared.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to users table
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON shared.users
    FOR EACH ROW
    EXECUTE FUNCTION shared.update_updated_at_column();

-- ============================================================================
-- INITIAL DATA
-- ============================================================================

-- Insert default system settings
INSERT INTO shared.system_settings (key, value, description) VALUES
    ('app.name', '"Household Meal Planning System"', 'Application name'),
    ('app.version', '"1.0.0"', 'Application version'),
    ('session.timeout_hours', '24', 'Session timeout in hours'),
    ('session.max_concurrent', '5', 'Maximum concurrent sessions per user')
ON CONFLICT (key) DO NOTHING;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON SCHEMA shared IS 'Shared schema containing common tables for all household applications';
COMMENT ON TABLE shared.users IS 'User accounts for all family members';
COMMENT ON TABLE shared.sessions IS 'Active user sessions for JWT token management';
COMMENT ON TABLE shared.user_activity_log IS 'Audit trail of user actions';
COMMENT ON TABLE shared.system_settings IS 'Global system configuration';

COMMENT ON COLUMN shared.users.role IS 'User role: admin, user, or child';
COMMENT ON COLUMN shared.users.is_active IS 'Whether the user account is active';
COMMENT ON COLUMN shared.sessions.token_hash IS 'Hashed JWT token for validation';
COMMENT ON COLUMN shared.system_settings.value IS 'JSON value allows flexible configuration types';

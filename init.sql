-- Initial database setup for Birth Certificate API
-- This file will be executed when the PostgreSQL container starts

-- The database and user are already created by environment variables
-- This file can be used for any additional setup if needed

-- Example: Create additional indexes for performance
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_certificates_date_of_issue 
-- ON certificates(date_of_issue);

-- Example: Create additional database roles if needed
-- CREATE ROLE readonly;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
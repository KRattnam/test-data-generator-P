-- this script runes once when the PostgreSSQL container first starts.
-- it sets up extensions and baseline config.
-- the actual tables are created by alembic migrations(not here)

-- Enable UUID generation
-- gen_random_uuid() is used as the default for UUID primary keys
CREATE EXTENSION IF NOT EXITS "pgcrypto";

-- Enable pg_stat_statements for query performance monitoring
CREATE EXTENSIONS IF NOT EXISTS "pg_stat_statements";

-- set timezone to UTC for all connections
-- always store timestamps in UTC - covert to local time in the application layer

ALTER DATABASE tdg SET timezone TO 'UTC';

CREATE ROLE postgres WITH LOGIN SUPERUSER PASSWORD 'postgres';
CREATE TABLE IF NOT EXISTS numbers (
    number BIGINT,
    timestamp BIGINT
);
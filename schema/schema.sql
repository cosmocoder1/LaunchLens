/*
schema.sql

Defines the normalized SQLite database schema for the SpaceX data pipeline.

This schema includes:
- Dimensional tables: rockets, launchpads, payloads
- Fact table: launches
- Join table: launch_payload (to model the many-to-many relationship between launches and payloads)

All tables include appropriate primary and foreign keys to maintain referential integrity.
Indexes are added to support efficient analytical queries on launch dates, rocket usage, and payload mass.

This schema supports downstream analysis such as:
- Launch frequency and success trends
- Payload characteristics across missions
- Rocket and launchpad performance metrics
*/


-- Table: rockets
CREATE TABLE IF NOT EXISTS rockets (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT
);

-- Table: launchpads
CREATE TABLE IF NOT EXISTS launchpads (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    locality TEXT,
    region TEXT
);

-- Table: payloads
CREATE TABLE IF NOT EXISTS payloads (
    id TEXT PRIMARY KEY,
    name TEXT,
    type TEXT,
    mass_kg REAL,
    orbit TEXT
);

-- Table: launches
CREATE TABLE IF NOT EXISTS launches (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    date_utc TEXT NOT NULL,
    success BOOLEAN,
    rocket_id TEXT,
    launchpad_id TEXT,
    FOREIGN KEY (rocket_id) REFERENCES rockets(id),
    FOREIGN KEY (launchpad_id) REFERENCES launchpads(id)
);

-- Table: launch_payload (many-to-many)
CREATE TABLE IF NOT EXISTS launch_payload (
    launch_id TEXT,
    payload_id TEXT,
    PRIMARY KEY (launch_id, payload_id),
    FOREIGN KEY (launch_id) REFERENCES launches(id),
    FOREIGN KEY (payload_id) REFERENCES payloads(id)
);

-- Indexes for query speed
CREATE INDEX IF NOT EXISTS idx_launches_date ON launches(date_utc);
CREATE INDEX IF NOT EXISTS idx_launches_rocket ON launches(rocket_id);
CREATE INDEX IF NOT EXISTS idx_payloads_mass ON payloads(mass_kg);

CREATE TABLE IF NOT EXISTS jobs (
    id CHAR(36) PRIMARY KEY,

    company VARCHAR(128) NOT NULL,
    title TEXT NOT NULL,
    location TEXT,
    job_type TEXT,
    description_html TEXT,
    link VARCHAR(512) UNIQUE NOT NULL,

    salary_min INT,
    salary_max INT,
    work_model ENUM('remote', 'on-site', 'hybrid'),
    industry TEXT,
    seniority ENUM('entry', 'mid', 'senior', 'lead'),
    technologies JSON,
    is_winnipeg BOOLEAN DEFAULT FALSE,
    department ENUM(
        'software_engineering',
        'management',
        'design',
        'marketing',
        'sales',
        'hr',
        'finance',
        'support',
        'operations',
        'other'
    ),
    min_experience INT,

    archived BOOLEAN DEFAULT FALSE,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE INDEX idx_archived_company ON jobs (archived, company);
CREATE INDEX idx_is_winnipeg ON jobs (is_winnipeg);
CREATE INDEX idx_last_seen ON jobs (last_seen);


CREATE TABLE IF NOT EXISTS job_notifications_queue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id CHAR(36) NOT NULL,  -- UUID as CHAR(36)
    event_type ENUM('new', 'archived') NOT NULL DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notified BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);
CREATE INDEX idx_notified_event ON job_notifications_queue (notified, event_type);


CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,  -- Telegram user ID
    username VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS job_alert_filters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,

    is_active BOOLEAN DEFAULT TRUE,         -- Whether alerts are currently enabled
    is_winnipeg BOOLEAN,                    -- Optional filter

    salary_min INT,
    salary_max INT,

    work_models JSON,                       -- e.g. ["remote", "on-site"]
    seniorities JSON,                       -- e.g. ["entry", "mid"]
    companies JSON,                         -- e.g. ["Neo", "Bold"]
    departments JSON,                       -- e.g. ["software_engineering", "design"]

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Speed up lookups when checking alerts for a user
CREATE INDEX idx_alerts_user_id ON job_alert_filters (user_id);

-- Filter only active ones during processing
CREATE INDEX idx_alerts_is_active ON job_alert_filters (is_active);

-- Optional: for time-based analysis
CREATE INDEX idx_alerts_created_at ON job_alert_filters (created_at);
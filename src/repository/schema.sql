CREATE TABLE IF NOT EXISTS system_metadata (
    system_id VARCHAR(50) PRIMARY KEY,
    target_repo_owner VARCHAR(100) NOT NULL,
    target_repo_name VARCHAR(100) NOT NULL,
    inactivity_threshold_hours INT DEFAULT 72,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS velocity_metrics (
    metric_id BIGSERIAL PRIMARY KEY,
    developer_name VARCHAR(100) NOT NULL,
    commit_sha VARCHAR(50) UNIQUE NOT NULL,
    commit_message TEXT,
    committed_at TIMESTAMP WITH TIME ZONE NOT NULL,
    lines_added INT DEFAULT 0,
    lines_deleted INT DEFAULT 0,
    extracted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pipeline_audit_logs (
    log_id BIGSERIAL PRIMARY KEY,
    system_id VARCHAR(50) REFERENCES system_metadata(system_id),
    total_commits_found INT NOT NULL,
    hours_since_last_push INT NOT NULL,
    threshold_triggered BOOLEAN DEFAULT FALSE,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS figma_metrics (
    id SERIAL PRIMARY KEY,
    designer_name VARCHAR(100) NOT NULL,
    file_key VARCHAR(100) NOT NULL,
    component_name VARCHAR(150),
    action_type VARCHAR(50) DEFAULT 'edit',
    modified_at TIMESTAMP WITH TIME ZONE NOT NULL,
    UNIQUE(designer_name, modified_at)
);

CREATE TABLE IF NOT EXISTS member_info (
    id SERIAL PRIMARY KEY,
    real_name VARCHAR(255) NOT NULL,
    github_username VARCHAR(100) UNIQUE,
    figma_username VARCHAR(100) UNIQUE,
    discord_user_id VARCHAR(50) UNIQUE,
    roles VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    has_contributed_today BOOLEAN DEFAULT FALSE,
    last_active_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    project_id INTEGER REFERENCES project_info(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS project_info (
        id SERIAL PRIMARY KEY,
        project_name VARCHAR(255) NOT NULL,
        start_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        project_deadline TIMESTAMP NULL
    );


INSERT INTO system_metadata (system_id, target_repo_owner, target_repo_name, inactivity_threshold_hours)
VALUES ('TRACKER-E5', 'Nyctukazu', 'e5-velocity-tracker', 72)
ON CONFLICT (system_id) DO UPDATE
SET target_repo_owner = EXCLUDED.target_repo_owner,
    target_repo_name = EXCLUDED.target_repo_name;
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

INSERT INTO system_metadata (system_id, target_repo_owner, target_repo_name, inactivity_threshold_hours)
VALUES ('TRACKER-E5', 'Nyctukazu', 'e5-velocity-tracker', 72)
ON CONFLICT (system_id) DO UPDATE
SET target_repo_owner = EXCLUDED.target_repo_owner,
    target_repo_name = EXCLUDED.target_repo_name;
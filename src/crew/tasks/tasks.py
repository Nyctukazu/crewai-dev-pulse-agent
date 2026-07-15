from crewai import Task
from src.models.project_model import ProjectHealthReport
import yaml

with open('config/tasks.yaml', 'r') as f:
    task_config = yaml.safe_load(f)

def get_velocity_task(agents: dict) -> list:
    """
    Dynamically maps configuration-driven tasks to specialized agent instances.
    Accepts a dictionary containing 'miner', 'archiver', 'inspector', and 'communicator' keys.
    """

    fetch_logs_task = Task(
        description=task_config['fetch_external_api_logs_task']['description'],
        expected_output=task_config['fetch_external_api_logs_task']['expected_output'],
        agent=agents['miner']
    )

    archive_data_task = Task(
        description=task_config['archive_data_task']['description'],
        expected_output=task_config['archive_data_task']['expected_output'],
        agent=agents['archiver'],
        context=[fetch_logs_task]
    )

    audit_velocity_task = Task(
        description=task_config['audit_velocity_metrics_task']['description'],
        expected_output=task_config['audit_velocity_metrics_task']['expected_output'],
        output_json=ProjectHealthReport,
        agent=agents['inspector'],
        context=[archive_data_task]
        
    )

    broadcast_alert_task = Task(
        description=task_config['broadcast_alert_task']['description'],
        expected_output=task_config['broadcast_alert_task']['expected_output'],
        agent=agents['communicator'],
        context=[audit_velocity_task]

    )

    return [fetch_logs_task, archive_data_task, audit_velocity_task, broadcast_alert_task]
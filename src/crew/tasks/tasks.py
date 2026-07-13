from crewai import Task
import yaml


with open('config/tasks.yaml', 'r') as f:
    github_task_config = yaml.safe_load(f)['velocity_inspection_task']
    figma_task_config = yaml.safe_load(f)['evaluate_figma_task']

def velocity_inspection_task(agent):
    """Generates the sequential pipeline tasks bound to our YAML configuration."""

    git_task = Task(
        description=github_task_config['description'],
        expected_output=github_task_config['expected_output'],
        agent=agent
    )

    figma_task = Task(
        description=figma_task_config['description'],
        expected_output=figma_task_config['expected_output'],
    )

    return [git_task, figma_task]
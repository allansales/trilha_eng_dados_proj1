import json
import pandas as pd
from config.config_loader import load_config
from src.utils.write_utils import write_to_destination
from src.utils.ingest_utils import read_from_source

config = load_config()

def create_dataframes_from_json(data: dict):
    """
    Receives a project + issues JSON e returns:
    1) df_project
    2) df_issue (with project_id as FK)
    """

    # -------------------------
    # Project dataframe
    # -------------------------
    df_project = pd.DataFrame([data["project"]])

    project_id = data["project"]["project_id"]

    # -------------------------
    # Issues dataframe
    # -------------------------
    issues_rows = []

    for issue in data["issues"]:
        base_issue = {
            "issue_id": issue["id"],
            "issue_type": issue["issue_type"],
            "status": issue["status"],
            "priority": issue["priority"],
            "project_id": project_id  # FK
        }

        # Assignee
        assignee = issue.get("assignee", [])
        if assignee:
            base_issue.update({
                "assignee_id": assignee[0].get("id"),
                "assignee_name": assignee[0].get("name"),
                "assignee_email": assignee[0].get("email"),
            })

        # Timestamps
        timestamps = issue.get("timestamps", [])
        if timestamps:
            base_issue.update({
                "created_at": timestamps[0].get("created_at"),
                "resolved_at": timestamps[0].get("resolved_at"),
            })

        issues_rows.append(base_issue)

    df_issue = pd.DataFrame(issues_rows)

    return df_project, df_issue

def validate_resolved_at(df: pd.DataFrame) -> pd.Series:
    date_valid = pd.to_datetime(df["resolved_at"], errors="coerce").notna()
    date_null_and_finished = df["resolved_at"].isna() & (df["status"] == "Open")
    
    return date_valid | date_null_and_finished

def evaluate_dates_quality(row):
    if not row["is_created_at_valid"] and not row["is_resolved_at_valid"]:
        return "INVALID_CREATED_AND_RESOLVED"
    if not row["is_created_at_valid"]:
        return "INVALID_CREATED_AT"
    if not row["is_resolved_at_valid"]:
        return "INVALID_RESOLVED_AT"
    return "VALID"

path_data_bronze = config['paths']['data']['bronze']
bronze_issue_filename = config['artifacts']['data']['bronze']['issue']
issues_data = read_from_source(path_data_bronze, bronze_issue_filename)

project, issue = create_dataframes_from_json(issues_data)

issue["raw_created_at"] = issue["created_at"]
issue["raw_resolved_at"] = issue["resolved_at"]

issue["created_at"] = pd.to_datetime(issue.raw_created_at, errors="coerce", utc=True)
issue["resolved_at"] = pd.to_datetime(issue.raw_resolved_at, errors="coerce", utc=True)

issue["is_created_at_valid"] = issue["created_at"].notna()
issue["is_resolved_at_valid"] = validate_resolved_at(issue)

issue["dates_quality"] = issue.apply(evaluate_dates_quality, axis=1)

path_data_silver = config['paths']['data']['silver']
issue_filename = config['artifacts']['data']['silver']['issue']
project_filename = config['artifacts']['data']['silver']['project']

write_to_destination(issue, path_data_silver, issue_filename)
write_to_destination(issue, path_data_silver, project_filename)
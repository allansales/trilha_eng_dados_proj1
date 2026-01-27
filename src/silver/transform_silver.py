import json
import pandas as pd
from config.config_loader import load_config

config = load_config()

filename = config['paths']['data']['bronze'] + "/" + config['artifacts']['data']['bronze'] 

def json_to_dataframes(data: dict):
    """
    Recebe um JSON de project + issues e retorna:
    1) df_project
    2) df_issue (com FK project_id)
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

        # Assignee (assumindo 1 assignee por issue)
        assignee = issue.get("assignee", [])
        if assignee:
            base_issue.update({
                "assignee_id": assignee[0].get("id"),
                "assignee_name": assignee[0].get("name"),
                "assignee_email": assignee[0].get("email"),
            })

        # Timestamps (assumindo 1 registro)
        timestamps = issue.get("timestamps", [])
        if timestamps:
            base_issue.update({
                "created_at": timestamps[0].get("created_at"),
                "resolved_at": timestamps[0].get("resolved_at"),
            })

        issues_rows.append(base_issue)

    df_issue = pd.DataFrame(issues_rows)

    return df_project, df_issue

# with open(filename, "r", encoding="utf-8") as f:
with open("data/bronze/bronze_sample.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

project, issue = json_to_dataframes(dados)
print(project.head(2))
print(issue.head(2))

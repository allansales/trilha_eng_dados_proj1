import pandas as pd

def get_report_from_group(data:pd.DataFrame, group:list[str]) -> pd.DataFrame:
    report = data.groupby(group).agg(
        avg_business_hours_to_sla_resolution=("business_hours_to_sla_resolution", "mean"),
        issue_count=("issue_id", "count")
    ).reset_index()
    return(report)

data = pd.read_parquet("data/gold/gold_jira_issues.parquet")

analyst_report = get_report_from_group(data, ['assignee_name','assignee_id','project_id'])
analyst_report.to_csv("analytics/report/analyst_report.csv", index=False)

issue_type_report = get_report_from_group(data, ['issue_type','project_id'])
issue_type_report.to_csv("analytics/report/issue_type_report.csv", index=False)
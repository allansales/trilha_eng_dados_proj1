import pandas as pd

def float_hours_to_hms(df: pd.DataFrame, column: str, new_column: str | None = None):
    """
    Converte uma coluna em horas decimais (float) para o formato HH:MM:SS.

    Ex:
    1.5  -> 01:30:00
    2.75 -> 02:45:00
    """

    target_col = new_column or column

    def convert(value):
        if pd.isna(value):
            return None

        total_seconds = int(round(value * 3600))
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return f"{hours}:{minutes:02d}:{seconds:02d}"

    df[target_col] = df[column].apply(convert)
    return df

def get_report_from_group(data:pd.DataFrame, group:list[str]) -> pd.DataFrame:
    report = data.groupby(group).agg(
        avg_business_hours_to_sla_resolution=("business_hours_to_sla_resolution", "mean"),
        issue_count=("issue_id", "count")
    ).reset_index()

    report = float_hours_to_hms(report, 'avg_business_hours_to_sla_resolution', 'avg_business_hours_to_sla_resolution_hms')

    return(report)

data = pd.read_parquet("data/gold/gold_jira_issues.parquet")

analyst_report = get_report_from_group(data, ['assignee_name','assignee_id','project_id'])
analyst_report.to_csv("analytics/report/analyst_report.csv", index=False)

issue_type_report = get_report_from_group(data, ['issue_type','project_id'])
issue_type_report.to_csv("analytics/report/issue_type_report.csv", index=False)
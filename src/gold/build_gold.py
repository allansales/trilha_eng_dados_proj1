import pandas as pd
from config.config_loader import load_config
from src.utils.write_utils import write_to_destination
from src.utils.ingest_utils import read_from_source
from src.utils.sla_calculation import get_business_hours_diff, get_expected_sla_hours_to_resolution, get_is_sla_violated

config = load_config()

# Paths from silver
path_data_silver = config['paths']['data']['silver']
silver_issue_filename = config['artifacts']['data']['silver']['issue']
silver_project_filename = config['artifacts']['data']['silver']['project']

# Paths from Gold
path_data_gold = config['paths']['data']['gold']
issue_filename = config['artifacts']['data']['gold']['issue']
project_filename = config['artifacts']['data']['gold']['project']

def run_gold():
    try:
        # Read files from silver
        issues_data_silver = read_from_source(path_data_silver, silver_issue_filename)
        project_data_silver = read_from_source(path_data_silver, silver_project_filename)

        # Filter finished and valid issues
        finished_issues = issues_data_silver[issues_data_silver.status != "Open"]
        valid_issues = finished_issues[finished_issues.dates_quality == 'VALID']

        # Compute business hours to resolve sla
        valid_issues["business_hours_to_sla_resolution"] = valid_issues.apply(lambda row: get_business_hours_diff(row["created_at"], row["resolved_at"]), axis=1)

        # Compute expected hours to resolve sla
        valid_issues = get_expected_sla_hours_to_resolution(valid_issues, 'priority')

        # Check whether the sla is violated or not
        valid_issues["is_sla_violated"] = get_is_sla_violated(valid_issues, "business_hours_to_sla_resolution", "expected_sla_hours_to_resolution")

        # Save issues and projects in the gold data folder as parquet
        write_to_destination(valid_issues, path_data_gold, issue_filename)
        write_to_destination(project_data_silver, path_data_gold, project_filename)

        print("Successfully executed Gold layer.")
    except Exception as e:
        print(f"Gold layer executed with error {e}")
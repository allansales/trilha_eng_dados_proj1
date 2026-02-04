import pandas as pd
from config.config_loader import load_config
from src.utils.write_utils import write_to_destination
from src.utils.ingest_utils import read_from_source
from src.utils.sla_calculation import get_business_hours_diff, get_expected_sla_hours_to_resolution, get_is_sla_violated

config = load_config()

path_data_silver = config['paths']['data']['silver']
silver_issue_filename = config['artifacts']['data']['silver']['issue']

issues_data_silver = read_from_source(path_data_silver, silver_issue_filename)
print(issues_data_silver.head(2))

finished_issues = issues_data_silver[issues_data_silver.status != "Open"]
valid_issues = finished_issues[finished_issues.dates_quality == 'VALID']
valid_issues.info()

valid_issues["business_hours_to_sla_resolution"] = valid_issues.apply(lambda row: get_business_hours_diff(row["created_at"], row["resolved_at"]), axis=1)

valid_issues = get_expected_sla_hours_to_resolution(valid_issues, 'priority')

valid_issues["is_sla_violated"] = get_is_sla_violated(valid_issues, "business_hours_to_sla_resolution", "expected_sla_hours_to_resolution")

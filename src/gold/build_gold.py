import pandas as pd
from config.config_loader import load_config
from src.utils.write_utils import write_to_destination
from src.utils.ingest_utils import read_from_source

config = load_config()

path_data_silver = config['paths']['data']['silver']
silver_issue_filename = config['artifacts']['data']['silver']['issue']

issues_data_silver = read_from_source(path_data_silver, silver_issue_filename)
print(issues_data_silver.head(2))
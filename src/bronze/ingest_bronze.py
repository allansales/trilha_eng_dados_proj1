import json

from config.settings import settings
from config.config_loader import load_config

from src.bronze.utils.ingest_utils import *

tenant_id = settings.AZURE_TENANT_ID
client_id = settings.AZURE_CLIENT_ID
client_secret = settings.AZURE_CLIENT_SECRET

config = load_config()
source_cfg = config['source']
account_url = source_cfg["account_url"]
container_name = source_cfg["container_name"]
blob_name = source_cfg["blob_name"]

path_data_bronze = config['paths']['data']['bronze']
artifact_bronze_name = config['artifacts']['data']['bronze']['issue']

data = get_json_blob_from_azure(blob_name, container_name, account_url, tenant_id, client_id, client_secret)
write_json_to_destination(data, path_data_bronze, artifact_bronze_name)
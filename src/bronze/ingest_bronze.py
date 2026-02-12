from config.settings import settings
from config.config_loader import load_config

from src.utils.write_utils import write_to_destination
from src.utils.ingest_utils import get_json_blob_from_azure

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

def run_bronze():
    try:
        data = get_json_blob_from_azure(blob_name, container_name, account_url, tenant_id, client_id, client_secret)
        write_to_destination(data, path_data_bronze, artifact_bronze_name)
        print("Successfully executed Bronze layer.")
    except Exception as e:
        print(f"Bronze layer executed with error {e}")
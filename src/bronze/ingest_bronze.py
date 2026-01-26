import json

from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient

from config.settings import settings
from config.config_loader import load_config

tenant_id = settings.AZURE_TENANT_ID
client_id = settings.AZURE_CLIENT_ID
client_secret = settings.AZURE_CLIENT_SECRET

config = load_config()
source_cfg = config['source']
account_url = source_cfg["account_url"]
container_name = source_cfg["container_name"]
blob_name = source_cfg["blob_name"]

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

blob_service_client = BlobServiceClient(
    account_url=account_url,
    credential=credential
)

blob_client = blob_service_client.get_blob_client(
    container=container_name,
    blob=blob_name
)

blob_bytes = blob_client.download_blob().readall()

data = json.loads(blob_bytes.decode("utf-8"))

print(data.keys())
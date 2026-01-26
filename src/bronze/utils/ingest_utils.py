import json

from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient

def get_json_blob_from_azure(blob_name:str, container_name:str, account_url:str, tenant_id:str, client_id:str, client_secret:str) -> json:

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

    return json.loads(blob_bytes.decode("utf-8"))

def write_json_to_destination(data:json, path_data_bronze:str, artifact_bronze_name:str) -> bool:
    try: 
        with open(f"{path_data_bronze}/{artifact_bronze_name}", "w", encoding="utf-8") as f:
            json.dump(data, f)
        print("Arquivo salvo com sucesso")
        return True
    except Exception as e:
        print(f"Falha ao salvar o arquivo: {e}")
        return False
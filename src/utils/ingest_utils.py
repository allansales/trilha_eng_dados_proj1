import json
import pandas as pd
from pathlib import Path

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

def read_from_source(
    path_source: str,
    artifact_name: str
):
    """
    Read data from filename and path.

    Suports:
    - .json  -> dict | list
    - .csv   -> pandas.DataFrame
    - .parquet -> pandas.DataFrame
    - .txt   -> str

    Parameters
    ----------
    path_source : str
    artifact_name : str (ex: 'data.json', 'data.csv')

    Returns
    -------
    dict | list | pd.DataFrame | str
    """
    try:
        file_path = Path(path_source) / artifact_name
        ext = file_path.suffix.lower()

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if ext == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)

        elif ext == ".csv":
            return pd.read_csv(file_path)

        elif ext == ".parquet":
            return pd.read_parquet(file_path)

        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        else:
            raise ValueError(f"Format not supported: {ext}")

    except Exception as e:
        raise RuntimeError(f"Failed to read file '{artifact_name}': {e}")

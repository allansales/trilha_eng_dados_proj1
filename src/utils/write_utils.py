from pathlib import Path
import json
import pandas as pd

def write_to_destination(data, path_destination: str, artifact_name: str) -> bool:
    """
    Write data in the destination acording to the file extention.

    Suports:
    - .json
    - .csv
    - .parquet
    - .txt

    Parameters
    ----------
    data : dict | list | pd.DataFrame | str
    path_destination : str
    artifact_name : str (ex: 'dados.json', 'dados.csv')

    Returns
    -------
    bool
    """
    try:
        destination = Path(path_destination)
        destination.mkdir(parents=True, exist_ok=True)

        file_path = destination / artifact_name
        ext = file_path.suffix.lower()

        if ext == ".json":
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

        elif ext == ".csv":
            if not isinstance(data, pd.DataFrame):
                raise TypeError("For csv, 'data' must be a pandas DataFrame")
            data.to_csv(file_path, index=False)

        elif ext == ".parquet":
            if not isinstance(data, pd.DataFrame):
                raise TypeError("Para Parquet, 'data' must be a pandas DataFrame")
            data.to_parquet(file_path, index=False, engine="fastparquet")

        elif ext == ".txt":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(str(data))

        else:
            raise ValueError(f"Format not supported: {ext}")

        print(f"File created at {file_path}")
        return True

    except Exception as e:
        print(f"Failed to save file: {e}")
        return False
import yaml

def load_config():
    with open("config/pipeline.yaml") as f:
        return yaml.safe_load(f)
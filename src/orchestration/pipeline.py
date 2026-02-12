from src.bronze.ingest_bronze import run_bronze
from src.silver.transform_silver import run_silver
from src.gold.build_gold import run_gold


def run_pipeline():
    print("Executing pipeline")

    run_bronze()
    run_silver()
    run_gold()

    print("Pipeline successfully executed.")

if __name__ == "__main__":
    run_pipeline()

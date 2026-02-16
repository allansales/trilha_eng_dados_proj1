from src.bronze.ingest_bronze import run_bronze
from src.silver.transform_silver import run_silver
from src.gold.build_gold import run_gold


def run_pipeline():
    print("Executing pipeline")
    try:
        run_bronze()
        run_silver()
        run_gold()

        print("Pipeline successfully executed.")

    except Exception as e:
        print(f"Pipeline executed with error {e}")

if __name__ == "__main__":
    run_pipeline()

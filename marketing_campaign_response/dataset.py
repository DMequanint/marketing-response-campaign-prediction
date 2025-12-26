# marketing_campaing_response/dataset.py

from pathlib import Path
import shutil

import pandas as pd
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from loguru import logger
import argparse

from marketing_campaing_response.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


def main(split_ratio: float = 0.1):
    """
    Download the Banking Marketing dataset, split into train/test, 
    and save CSVs. Automatically handles Parquet cache issues.

    Args:
        split_ratio (float): Fraction of dataset to use as test set (0 < split_ratio < 1)
    """
    logger.info("Starting dataset preparation...")

    # Clear Hugging Face cache for this dataset to avoid Parquet issues
    hf_cache_dir = Path.home() / ".cache/huggingface/datasets/Andyrasika___parquet"
    if hf_cache_dir.exists():
        logger.info(f"Clearing Hugging Face cache at {hf_cache_dir}")
        shutil.rmtree(hf_cache_dir)

    logger.info("Downloading banking marketing dataset...")
    ds = load_dataset("Andyrasika/banking-marketing", download_mode="force_redownload")
    df = pd.DataFrame(ds['train'])

    # Split into train/test
    train_df, test_df = train_test_split(df, test_size=split_ratio, random_state=42)

    # Save CSVs
    train_path = RAW_DATA_DIR / "marketing_training.csv"
    test_path = RAW_DATA_DIR / "marketing_test.csv"

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    # Optional: save a processed copy in PROCESSED_DATA_DIR
    processed_train_path = PROCESSED_DATA_DIR / "marketing_training.csv"
    processed_test_path = PROCESSED_DATA_DIR / "marketing_test.csv"

    train_df.to_csv(processed_train_path, index=False)
    test_df.to_csv(processed_test_path, index=False)

    logger.success(f"Training and test CSVs saved successfully:\n"
                   f"RAW: {train_path}, {test_path}\n"
                   f"PROCESSED: {processed_train_path}, {processed_test_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare banking marketing dataset")
    parser.add_argument(
        "--test_ratio",
        type=float,
        default=0.1,
        help="Fraction of the dataset to use as the test set (default: 0.1)",
    )
    args = parser.parse_args()
    main(split_ratio=args.test_ratio)

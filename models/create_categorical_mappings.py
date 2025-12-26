# models/create_categorical_mappings.py
"""
Script to generate and save categorical mappings from training data.

This script reads the processed marketing campaign training CSV,
applies column renaming, extracts unique values for each categorical
column, and saves them in a deterministic order to a pickle file.
These mappings are later used by the API and frontend to populate
dropdowns and ensure consistency during model inference.
"""

import sys
from pathlib import Path
import joblib
import pandas as pd

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from marketing_campaign_response.features import (
    CATEGORICAL_COLS,
    COLUMN_MAPPING,
)

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "marketing_training.csv"
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)


def create_categorical_mappings():
    """
    Generate deterministic mappings of categorical values from training data.

    Steps:
    1. Load processed training CSV.
    2. Rename columns according to COLUMN_MAPPING.
    3. For each categorical column:
       - Convert to string, strip whitespace, lowercase, fill missing with "unknown".
       - Extract unique values and sort them.
    4. Save the mappings as 'categorical_mappings.pkl' in the models directory.

    Raises
    ------
    FileNotFoundError
        If the training CSV does not exist.
    ValueError
        If any expected categorical column is missing after renaming.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Training data not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # Apply SAME renaming logic as training/inference
    df = df.rename(columns=COLUMN_MAPPING)

    mappings = {}

    for col in CATEGORICAL_COLS:
        if col not in df.columns:
            raise ValueError(
                f"Categorical column '{col}' missing AFTER renaming. "
                f"Available columns: {list(df.columns)}"
            )

        values = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
            .fillna("unknown")
            .unique()
            .tolist()
        )

        if "unknown" not in values:
            values.append("unknown")

        # Stable, deterministic order
        mappings[col] = sorted(values)

    mappings_file = MODELS_DIR / "categorical_mappings.pkl"
    joblib.dump(mappings, mappings_file)

    print(f"✅ Categorical mappings saved to {mappings_file}")


if __name__ == "__main__":
    """
    Run the script as a standalone program to generate categorical mappings.
    """
    create_categorical_mappings()


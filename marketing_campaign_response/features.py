# marketing_campaign_response/features.py
import pandas as pd
from typing import Tuple, Optional, List
from pathlib import Path
import joblib

TARGET_COL = "responded"

CATEGORICAL_COLS: List[str] = [
    "profession",
    "marital",
    "schooling",
    "default",
    "housing",
    "contact",
    "month",
    "day_of_week",
    "poutcome",
]

NUMERICAL_COLS: List[str] = [
    "custAge",
    "campaign",
    "pdays",
    "previous",
    "emp.var.rate",
    "cons.price.idx",
    "cons.conf.idx",
    "euribor3m",
    "nr.employed",
    "pmonths",
    "pastEmail",
]

FEATURE_COLS: List[str] = CATEGORICAL_COLS + NUMERICAL_COLS

COLUMN_MAPPING = {
    "age": "custAge",
    "job": "profession",
    "education": "schooling",
    "day": "day_of_week",
    "y": "responded",

    # 🔴 REQUIRED FIX
    "emp_var_rate": "emp.var.rate",
    "cons_price_idx": "cons.price.idx",
    "cons_conf_idx": "cons.conf.idx",
    "nr_employed": "nr.employed",
}

PROJ_ROOT = Path(__file__).resolve().parent.parent
CATEGORICAL_MAPPINGS_FILE = PROJ_ROOT / "models" / "categorical_mappings.pkl"


def load_categorical_mappings() -> dict:
    if not CATEGORICAL_MAPPINGS_FILE.exists():
        raise FileNotFoundError(
            f"Categorical mappings not found at {CATEGORICAL_MAPPINGS_FILE}. "
            "Please run models/create_categorical_mappings.py first."
        )
    return joblib.load(CATEGORICAL_MAPPINGS_FILE)


def prepare_features(
    df: pd.DataFrame,
    *,
    training: bool = True,
    target_col: str = TARGET_COL,
) -> Tuple[pd.DataFrame, Optional[pd.Series]]:

    if df.empty:
        raise ValueError("Input dataframe is empty")

    df = df.copy()

    # 🔹 Normalize column names FIRST
    df.rename(columns=COLUMN_MAPPING, inplace=True)
    df = df.loc[:, ~df.columns.duplicated()]

    y: Optional[pd.Series] = None
    if training and target_col in df.columns:
        y = df[target_col].apply(
            lambda x: 1 if str(x).lower() in ["yes", "1", "true"] else 0
        )
        df = df.drop(columns=[target_col])

    # 🔹 Ensure all features exist
    for col in FEATURE_COLS:
        if col not in df.columns:
            df[col] = "unknown" if col in CATEGORICAL_COLS else 0

    # 🔹 Enforce correct order
    df = df[FEATURE_COLS]

    # 🔹 Categorical handling (LightGBM-native)
    mappings = load_categorical_mappings()

    for col in CATEGORICAL_COLS:
        allowed = mappings.get(col, [])

        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        df[col] = df[col].apply(
            lambda x: x if x in allowed else "unknown"
        )

        df[col] = pd.Categorical(df[col], categories=allowed)

    # 🔹 Special numeric handling
    df["pdays"] = df["pdays"].replace(999, -1)
    df["pmonths"] = df["pmonths"].replace(999, -1)

    return df, y


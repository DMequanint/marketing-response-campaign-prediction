# marketing_campaing_response/modeling/train.py

"""
Model training pipeline for marketing campaign response prediction.

This module trains a LightGBM binary classifier to predict whether a
customer will respond to a marketing campaign. It includes feature
preparation, class imbalance handling, model evaluation, and persistence.

The resulting model artifact is saved to disk and later used for inference.
"""

import logging
from pathlib import Path

import joblib
import lightgbm as lgb
import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

from marketing_campaign_response.config import PROCESSED_DATA_DIR, MODELS_DIR
from marketing_campaign_response.features import prepare_features, TARGET_COL

# -------------------------------------------------------------------
# Logging configuration
# -------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Output model path
MODEL_PATH = MODELS_DIR / "lgbm_marketing.pkl"


def main():
    """
    Train and persist a LightGBM marketing response model.

    Workflow:
    1. Load preprocessed training data
    2. Apply feature engineering and target extraction
    3. Split data into training and validation sets
    4. Address class imbalance using scale_pos_weight
    5. Train LightGBM with early stopping
    6. Evaluate model performance
    7. Save trained model to disk

    This function is intended to be executed as a script and does not
    return a value.
    """

    # ---------------------------------------------------------------
    # Load training data
    # ---------------------------------------------------------------
    train_csv = PROCESSED_DATA_DIR / "marketing_training.csv"
    logger.info(f"Loading training data from {train_csv}")

    df = pd.read_csv(train_csv)

    # ---------------------------------------------------------------
    # Feature engineering
    # ---------------------------------------------------------------
    X, y = prepare_features(
        df,
        training=True,
        target_col=TARGET_COL
    )

    # ---------------------------------------------------------------
    # Train / validation split
    # ---------------------------------------------------------------
    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # ---------------------------------------------------------------
    # Handle class imbalance
    # ---------------------------------------------------------------
    pos_ratio = y_train.sum() / y_train.shape[0]
    scale_pos_weight = (1 - pos_ratio) / pos_ratio

    logger.info(
        f"Positive class ratio: {pos_ratio:.4f}, "
        f"scale_pos_weight: {scale_pos_weight:.4f}"
    )

    # ---------------------------------------------------------------
    # LightGBM datasets
    # ---------------------------------------------------------------
    lgb_train = lgb.Dataset(
        X_train,
        label=y_train,
        categorical_feature="auto"
    )

    lgb_val = lgb.Dataset(
        X_val,
        label=y_val,
        categorical_feature="auto",
        reference=lgb_train
    )

    # ---------------------------------------------------------------
    # Model parameters
    # ---------------------------------------------------------------
    params = {
        "objective": "binary",
        "metric": ["binary_logloss", "auc"],
        "boosting_type": "gbdt",
        "learning_rate": 0.05,
        "num_leaves": 31,
        "max_depth": -1,
        "scale_pos_weight": scale_pos_weight,
        "verbose": -1,
        "seed": 42,
    }

    # ---------------------------------------------------------------
    # Model training
    # ---------------------------------------------------------------
    logger.info("Training LightGBM model...")

    model = lgb.train(
        params=params,
        train_set=lgb_train,
        num_boost_round=1000,
        valid_sets=[lgb_train, lgb_val],
        callbacks=[
            lgb.early_stopping(stopping_rounds=50),
            lgb.log_evaluation(50),
        ],
    )

    # ---------------------------------------------------------------
    # Model evaluation
    # ---------------------------------------------------------------
    val_preds = model.predict(X_val)
    val_preds_binary = (val_preds >= 0.5).astype(int)

    acc = accuracy_score(y_val, val_preds_binary)
    auc = roc_auc_score(y_val, val_preds)

    logger.info(f"Validation Accuracy: {acc:.4f}")
    logger.info(f"Validation AUC: {auc:.4f}")

    # ---------------------------------------------------------------
    # Persist trained model
    # ---------------------------------------------------------------
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    logger.info(f"Saved LightGBM model to {MODEL_PATH}")


# -------------------------------------------------------------------
# Script entry point
# -------------------------------------------------------------------
if __name__ == "__main__":
    main()


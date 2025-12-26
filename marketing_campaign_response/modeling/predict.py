# marketing_campaing_response/modeling/predict.py

"""
Inference module for marketing campaign response prediction.

This module loads a trained LightGBM model and exposes a Predictor class
for generating response predictions on new customer data. It supports
both batch and single-record inference and is designed to be reused
by APIs, CLIs, and notebooks.
"""

from typing import List, Dict, Union, Optional
from pathlib import Path

import pandas as pd
import joblib

from marketing_campaign_response.config import MODELS_DIR
from marketing_campaign_response.features import prepare_features


class Predictor:
    """
    Wrapper class for model inference.

    Responsibilities:
    - Load the trained LightGBM model from disk
    - Validate and transform input data
    - Produce binary predictions and associated probabilities

    This class is intentionally lightweight and stateless beyond
    model loading to keep inference fast and deterministic.
    """

    def __init__(self):
        """
        Initialize the Predictor by loading the trained model.

        Raises
        ------
        FileNotFoundError
            If the trained model file does not exist at the expected path.
        """
        self.model_path: Path = MODELS_DIR / "lgbm_marketing.pkl"

        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        # Load trained LightGBM model
        self.model = joblib.load(self.model_path)

    def predict(
        self,
        rows: Union[List[Dict[str, Optional[str]]], pd.DataFrame],
    ) -> Dict[str, List[float]]:
        """
        Predict customer response to a marketing campaign.

        This method:
        1. Converts raw input into a pandas DataFrame
        2. Applies the same feature engineering used during training
        3. Generates probability scores and binary predictions

        Parameters
        ----------
        rows : List[Dict[str, Optional[str]]] or pd.DataFrame
            Input customer records. Each record must contain the same
            feature schema used during model training.

        Returns
        -------
        dict
            A dictionary with:
            - "predictions": List[int]
                Binary class labels (0 = no response, 1 = response)
            - "probabilities": List[float]
                Model confidence scores for the positive class

        Notes
        -----
        - A probability threshold of 0.5 is used to generate class labels.
        - Feature preparation runs in inference mode (training=False).
        """
        # Normalize input format
        if isinstance(rows, list):
            df = pd.DataFrame(rows)
        else:
            df = rows.copy()

        # Apply feature engineering (no fitting during inference)
        X, _ = prepare_features(df, training=False)

        # Generate probability scores
        probs = self.model.predict(X)

        # Convert probabilities to binary predictions
        preds = (probs >= 0.5).astype(int)

        return {
            "predictions": preds.tolist(),
            "probabilities": probs.tolist(),
        }


# -------------------------------------------------------------------
# Quick CLI test
# -------------------------------------------------------------------
if __name__ == "__main__":
    """
    Minimal command-line test for validating inference behavior.

    This block allows developers to quickly sanity-check:
    - Model loading
    - Feature preprocessing
    - Output formatting
    """

    predictor = Predictor()

    sample_data = [
        {
            "custAge": 35,
            "profession": "admin",
            "marital": "single",
            "schooling": "high.school",
            "default": "no",
            "housing": "yes",
            "contact": "cellular",
            "month": "may",
            "day_of_week": "mon",
            "campaign": 1,
            "pdays": -1,
            "previous": 0,
            "poutcome": "unknown",
            "emp_var_rate": 1.1,
            "cons_price_idx": 93.994,
            "cons_conf_idx": -36.4,
            "euribor3m": 4.857,
            "nr_employed": 5191,
            "pmonths": -1,
            "pastEmail": 0,
        }
    ]

    result = predictor.predict(sample_data)
    print(result)


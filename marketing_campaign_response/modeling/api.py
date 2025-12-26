# api.py
"""
FastAPI backend for Marketing Campaign Response Prediction.

Provides endpoints for:
- Predicting response for a single customer
- Predicting response for a batch of customers
- Retrieving categorical mappings for frontend form population
- Health check for service status
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import joblib
from marketing_campaign_response.modeling.predict import Predictor
from marketing_campaign_response.config import MODELS_DIR

app = FastAPI(title="Marketing Campaign Response Predictor")
predictor = Predictor()


# -------------------------------
# Pydantic model for a single customer
# -------------------------------
class Customer(BaseModel):
    """
    Pydantic schema representing a single customer's features.

    All fields are optional to allow partial submissions.
    This schema is used for both single and batch predictions.
    """
    custAge: Optional[int]
    profession: Optional[str]
    marital: Optional[str]
    schooling: Optional[str]
    default: Optional[str]
    housing: Optional[str]
    contact: Optional[str]
    month: Optional[str]
    day_of_week: Optional[str]
    campaign: Optional[int]
    pdays: Optional[int]
    previous: Optional[int]
    poutcome: Optional[str]
    emp_var_rate: Optional[float]
    cons_price_idx: Optional[float]
    cons_conf_idx: Optional[float]
    euribor3m: Optional[float]
    nr_employed: Optional[float]
    pmonths: Optional[int]
    pastEmail: Optional[int]


# -------------------------------
# Single customer prediction
# -------------------------------
@app.post("/predict")
def predict_customer(customer: Customer):
    """
    Predict marketing campaign response for a single customer.

    Parameters
    ----------
    customer : Customer
        Pydantic model with customer features.

    Returns
    -------
    dict
        Dictionary containing:
        - predictions: list of predicted classes (0/1)
        - probabilities: list of predicted probabilities for class 1

    Raises
    ------
    HTTPException
        If prediction fails on the backend.
    """
    customer_dict = customer.dict()
    try:
        result = predictor.predict([customer_dict])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# Batch predictions
# -------------------------------
@app.post("/predict/batch")
def predict_batch(customers: List[Customer]):
    """
    Predict marketing campaign response for a batch of customers.

    Parameters
    ----------
    customers : List[Customer]
        List of Pydantic models, each representing a customer.

    Returns
    -------
    dict
        Dictionary containing:
        - predictions: list of predicted classes (0/1)
        - probabilities: list of predicted probabilities for class 1

    Raises
    ------
    HTTPException
        If prediction fails on the backend.
    """
    try:
        rows = [c.dict() for c in customers]
        result = predictor.predict(rows)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# Categorical mappings
# -------------------------------
@app.get("/categorical_mappings")
def get_categorical_mappings():
    """
    Returns allowed categorical values for all categorical columns.

    Frontend should fetch this endpoint to populate dropdowns dynamically
    for user-friendly input forms.

    Returns
    -------
    dict
        Dictionary with keys as categorical column names and values as lists
        of valid category strings.

    Raises
    ------
    HTTPException
        If the mappings file does not exist or cannot be loaded.
    """
    mappings_file = MODELS_DIR / "categorical_mappings.pkl"
    if not mappings_file.exists():
        raise HTTPException(status_code=404, detail="Categorical mappings not found")
    
    try:
        mappings = joblib.load(mappings_file)
        return mappings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading categorical mappings: {str(e)}")


# -------------------------------
# Health check
# -------------------------------
@app.get("/health")
def health_check():
    """
    Simple health check endpoint.

    Returns
    -------
    dict
        Dictionary indicating service status.
        Example: {"status": "ok"}
    """
    return {"status": "ok"}


# marketing_campaign_response/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from marketing_campaign_response.modeling.predict import Predictor
from pydantic import BaseModel
from typing import List, Dict, Any

# ------------------------------
# App Initialization
# ------------------------------

app = FastAPI(
    title="Marketing Campaign Predictor",
    version="0.1.0",
    description="Predicts customer response for marketing campaigns using ML model"
)

# ✅ CORS Middleware for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Predictor Instance
# ------------------------------

predictor = Predictor()

# ------------------------------
# Pydantic Model
# ------------------------------

class CustomerModel(BaseModel):
    custAge: int
    profession: str
    marital: str
    schooling: str
    default: str
    housing: str
    contact: str
    month: str
    day_of_week: str
    campaign: int
    pdays: int
    previous: int
    poutcome: str
    emp_var_rate: float
    cons_price_idx: float
    cons_conf_idx: float
    euribor3m: float
    nr_employed: float
    pmonths: int
    pastEmail: int

# ------------------------------
# API Endpoints
# ------------------------------

@app.get("/health", tags=["Health"])
def health_check() -> Dict[str, str]:
    """
    Health check endpoint to verify backend is running
    """
    return {"status": "ok"}


@app.post("/predict", tags=["Prediction"])
def predict(customers: List[CustomerModel]) -> Dict[str, Any]:
    """
    Accepts a list of customer data and returns predictions
    """
    rows = [customer.dict() for customer in customers]
    predictions = predictor.predict(rows)
    return predictions

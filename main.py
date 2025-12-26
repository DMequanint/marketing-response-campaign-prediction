# marketing_campaing_response/main.py
from fastapi import FastAPI
from marketing_campaign_response.modeling.predict import Predictor
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="Marketing Campaign Predictor")

predictor = Predictor()

# Pydantic model for input
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

@app.post("/predict")
def predict(customers: List[CustomerModel]):
    rows = [customer.dict() for customer in customers]
    result = predictor.predict(rows)
    return result


# api.py (PROJECT ROOT)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

from marketing_campaign_response.modeling.predict import Predictor

app = FastAPI(title="Marketing Campaign Response API")

# Allow React (adjust later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once at startup
predictor = Predictor()


class PredictionRequest(BaseModel):
    records: List[Dict]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictionRequest):
    return predictor.predict(request.records)


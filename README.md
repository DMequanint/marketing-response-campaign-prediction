# marketing-campaing-response

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Marketing Campaign Response Prediction

## Project Organization

```
marketing-response-project/
├── frontend/ <- React frontend
│ ├── public/
│ ├── src/
│ ├── package.json
│ └── ...
│ ├── marketing_campaing_response/
│ │ ├── config.py
│ │ ├── features.py
│ │ ├── modeling/
│ │ │ ├── train.py
│ │ │ └── predict.py
│ │ └── ...
│ ├── api.py
│ ├── requirements.txt
│ └── ...
├── README.md
└── .gitignore


- `frontend/` contains the React UI that allows users to input customer data and view predictions.
- `backend/` contains the Python ML code, FastAPI endpoints, and trained LightGBM model.
- `README.md` documents how to run both components.

---

## Features

### Frontend (React)
- Single customer input form
- Batch CSV upload support
- Dynamic input placeholders with hints
- Displays prediction class and probability
- Modern UI with responsive layout

### Backend (FastAPI + ML)
- LightGBM model trained on marketing campaign data
- Categorical encoding and preprocessing
- Single and batch predictions endpoints
- Endpoint for fetching allowed categorical values
- Health check endpoint

---

## Installation

### 1. Clone repository

```bash
git clone https://github.com/yourusername/marketing-response-project.git
cd marketing-response-project

#Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows
pip install -r requirements.txt

#Frontend Setup
cd ../frontend
npm install

#API runs at: http://127.0.0.1:8000
cd backend
uvicorn marketing_campaign_response.main:app --reload

#API Endpoints
- POST /predict → Predict single customer
- POST /predict/batch → Predict batch customers
- GET /categorical_mappings → Fetch allowed categorical values
- GET /health → Health check
#Start Frontend
cd frontend
npm run dev
# Example Prediction
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
  "pastEmail": 0
}
#Example Response
{
  "predictions": [1],
  "probabilities": [0.73]
}


```

--------


import pandas as pd
from marketing_campaing_response.features import prepare_features, CATEGORICAL_COLS, NUMERICAL_COLS

# Sample mock data (like your dataset)
data = {
    "custAge": [25, 40],
    "profession": ["admin", "technician"],
    "marital": ["single", "married"],
    "schooling": ["high.school", "university.degree"],
    "default": ["no", "no"],
    "housing": ["yes", "no"],
    "contact": ["cellular", "telephone"],
    "month": ["may", "jun"],
    "day_of_week": ["mon", "thu"],
    "campaign": [1, 3],
    "pdays": [999, 5],
    "previous": [0, 2],
    "poutcome": ["unknown", "failure"],
    "emp.var.rate": [-1.8, 1.1],
    "cons.price.idx": [92.893, 93.994],
    "cons.conf.idx": [-46.2, -42.0],
    "euribor3m": [1.313, 4.857],
    "nr.employed": [5099.1, 5191.0],
    "pmonths": [999, 2],
    "pastEmail": [0, 1],
    "responded": [0, 1],  # target column
}

df = pd.DataFrame(data)

# -------------------------------
# Test training mode
# -------------------------------
X_train, y_train = prepare_features(df, training=True)
print("TRAINING FEATURES:\n", X_train)
print("TRAINING TARGET:\n", y_train)

# -------------------------------
# Test inference mode
# -------------------------------
X_infer, y_infer = prepare_features(df.drop(columns=["responded"]), training=False)
print("INFERENCE FEATURES:\n", X_infer)
print("INFERENCE TARGET (should be None):", y_infer)


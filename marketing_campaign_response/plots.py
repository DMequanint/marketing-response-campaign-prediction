# marketing_campaing_response/plots.py

import matplotlib.pyplot as plt
import lightgbm as lgb
import joblib
from marketing_campaing_response.config import MODELS_DIR, REPORTS_DIR

REPORTS_DIR.mkdir(exist_ok=True)
model = joblib.load(MODELS_DIR / "lightgbm_model.pkl")
lgb.plot_importance(model, max_num_features=15, importance_type='gain')
plt.tight_layout()
plt.savefig(REPORTS_DIR / "figures/feature_importance.png")
plt.show()


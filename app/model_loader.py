import joblib
from pathlib import Path

# -------------------------
# Model metadata
# -------------------------

MODEL_VERSION = "primary-care-cvd-risk-catboost-v1.0"

MODEL_PATH = Path("model/improved_catboost.cbm")


from catboost import CatBoostClassifier

# -------------------------
# Model loading
# -------------------------

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH.resolve()}"
        )
    model = CatBoostClassifier()
    model.load_model(MODEL_PATH)
    return model


def get_model_version():
    return MODEL_VERSION


def get_model_performance_metrics():
    """
    Return model performance metrics for transparency
    """
    return {
        "sensitivity": 0.90,
        "specificity": 0.4188,
        "roc_auc": 0.7989,
        "precision": 0.60,
        "recall": 0.9004,
        "f1_score": 0.72,
        "note": "Optimized for high sensitivity (Safety First)"
    }
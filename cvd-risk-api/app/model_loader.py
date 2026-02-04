import joblib
from pathlib import Path

# -------------------------
# Model metadata
# -------------------------

MODEL_VERSION = "primary-care-cvd-risk-catboost-v1.0"

MODEL_PATH = Path("model/calibrated_catboost.pkl")


# -------------------------
# Model loading
# -------------------------

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH.resolve()}"
        )
    return joblib.load(MODEL_PATH)


def get_model_version():
    return MODEL_VERSION


def get_model_performance_metrics():
    """
    Return model performance metrics for transparency
    """
    return {
        "sensitivity": 0.7005,
        "specificity": 0.7733,
        "ppv": 0.7534,
        "npv": 0.7231,
        "pr_auc": 0.7796,
        "roc_auc": 0.7999,
        "brier_score": 0.1809,
        "precision": 0.5595,
        "recall": 0.9546,
        "f1_score": 0.7055,
        "gender_specific_roc_auc": {
            1: 0.8056,  # Female
            2: 0.7929   # Male
        }
    }
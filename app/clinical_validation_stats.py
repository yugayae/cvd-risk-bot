
import pandas as pd
import numpy as np
import json
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.calibration import calibration_curve
from pathlib import Path

# Configuration
DATA_PATH = "CVD_risk_dataset.csv"
MODEL_PATH = "model/improved_catboost.cbm"
OUTPUT_METRICS = "model/validation_stats.json"
RANDOM_SEED = 42

def calculate_ece(y_true, y_prob, n_bins=10):
    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=n_bins, strategy='uniform')
    
    # We need the counts in each bin to weigh the ECE
    counts, _ = np.histogram(y_prob, bins=np.linspace(0, 1, n_bins + 1))
    nonzero = counts > 0
    
    ece = np.sum(np.abs(prob_true - prob_pred[nonzero]) * counts[nonzero]) / np.sum(counts)
    return float(ece)

def calculate_net_benefit(y_true, y_prob, thresholds):
    net_benefits = []
    n = len(y_true)
    
    # Treat All
    tp_all = np.sum(y_true == 1)
    fp_all = np.sum(y_true == 0)
    
    # Treat None
    # Net benefit is 0 by definition
    
    for t in thresholds:
        if t == 1.0:
            net_benefits.append({"threshold": float(t), "model": 0.0, "all": 0.0, "none": 0.0})
            continue
            
        y_pred = (y_prob >= t).astype(int)
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        
        weight = t / (1 - t)
        nb_model = (tp / n) - (fp / n) * weight
        nb_all = (tp_all / n) - (fp_all / n) * weight
        
        net_benefits.append({
            "threshold": float(t),
            "model": float(nb_model),
            "all": float(nb_all),
            "none": 0.0
        })
    
    return net_benefits

def main():
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    # Simple cleaning as in training script to ensure consistency
    df = df[(df['ap_hi'] >= 40) & (df['ap_hi'] <= 250) & 
            (df['ap_lo'] >= 30) & (df['ap_lo'] <= 200) & 
            (df['ap_hi'] > df['ap_lo'])]
    df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
    df = df[(df['bmi'] >= 10) & (df['bmi'] <= 60)]
    
    feature_cols = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'bmi']
    X = df[feature_cols]
    y = df['cardio']
    
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y)
    
    print("Loading model...")
    model = CatBoostClassifier()
    model.load_model(MODEL_PATH)
    
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print("Calculating overall metrics...")
    brier = brier_score_loss(y_test, y_prob)
    ece = calculate_ece(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)
    
    # Calibration Plot Data
    prob_true, prob_pred = calibration_curve(y_test, y_prob, n_bins=10)
    
    print("Calculating subgroup analysis...")
    # Gender (1=female, 2=male usually)
    subgroups = {}
    
    for gender in [1, 2]:
        mask = X_test['gender'] == gender
        if mask.any():
            y_t = y_test[mask]
            y_p = y_prob[mask]
            subgroups[f"gender_{gender}"] = {
                "auc": float(roc_auc_score(y_t, y_p)),
                "brier": float(brier_score_loss(y_t, y_p)),
                "ece": calculate_ece(y_t, y_p),
                "count": int(mask.sum())
            }
            
    # Age Groups
    # age in dataset is in days
    df_test = X_test.copy()
    df_test['y_true'] = y_test
    df_test['y_prob'] = y_prob
    df_test['age_years'] = df_test['age'] / 365.25
    
    age_bins = [0, 45, 65, 100]
    age_labels = ["young", "middle", "old"]
    df_test['age_group'] = pd.cut(df_test['age_years'], bins=age_bins, labels=age_labels)
    
    for label in age_labels:
        mask = df_test['age_group'] == label
        if mask.any():
            y_t = df_test.loc[mask, 'y_true']
            y_p = df_test.loc[mask, 'y_prob']
            subgroups[f"age_{label}"] = {
                "auc": float(roc_auc_score(y_t, y_p)),
                "brier": float(brier_score_loss(y_t, y_p)),
                "ece": calculate_ece(y_t, y_p),
                "count": int(mask.sum())
            }
            
    print("Calculating DCA...")
    thresholds = np.linspace(0, 0.5, 51) # Focus on low-moderate thresholds for screening
    dca_data = calculate_net_benefit(y_test, y_prob, thresholds)
    
    stats = {
        "overall": {
            "auc": float(auc),
            "brier": float(brier),
            "ece": float(ece),
            "calibration_curve": {
                "prob_true": prob_true.tolist(),
                "prob_pred": prob_pred.tolist()
            }
        },
        "subgroups": subgroups,
        "dca": dca_data
    }
    
    with open(OUTPUT_METRICS, 'w') as f:
        json.dump(stats, f, indent=4)
        
    print(f"Stats saved to {OUTPUT_METRICS}")

if __name__ == "__main__":
    main()

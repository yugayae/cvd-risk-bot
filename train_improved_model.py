
import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, recall_score, precision_score, confusion_matrix

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
DATA_PATH = "CVD_risk_dataset.csv"
MODEL_OUTPUT_PATH = "model/improved_catboost.cbm"
RANDOM_SEED = 42

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------
print("Loading dataset...")
df = pd.read_csv(DATA_PATH)
initial_shape = df.shape
print(f"Initial shape: {initial_shape}")

# ---------------------------------------------------------
# 2. DATA CLEANING (OUTLIER REMOVAL)
# ---------------------------------------------------------
# Valid ranges based on physiological limits and common sense for this dataset
# Systolic BP: 40-250
# Diastolic BP: 30-200
# Height: 100-250 cm
# Weight: 30-250 kg

print("\nCleaning data (removing outliers)...")
df_clean = df.copy()

# Remove unrealistic Blood Pressure
mask_bp = (df_clean['ap_hi'] >= 40) & (df_clean['ap_hi'] <= 250) & \
          (df_clean['ap_lo'] >= 30) & (df_clean['ap_lo'] <= 200) & \
          (df_clean['ap_hi'] > df_clean['ap_lo']) # Systolic must be > Diastolic

# Remove unrealistic Height/Weight
mask_anthropometry = (df_clean['height'] >= 100) & (df_clean['height'] <= 250) & \
                     (df_clean['weight'] >= 30) & (df_clean['weight'] <= 250)

df_clean = df_clean[mask_bp & mask_anthropometry]

print(f"Rows removed: {initial_shape[0] - df_clean.shape[0]}")
print(f"Cleaned shape: {df_clean.shape}")

# ---------------------------------------------------------
# 3. FEATURE ENGINEERING
# ---------------------------------------------------------
print("\nFeature Engineering...")

# Calculate BMI accurately
# BMI = weight (kg) / (height (m))^2
df_clean['bmi'] = df_clean['weight'] / ((df_clean['height'] / 100) ** 2)

# Filter by BMI (realistic range 10-60)
df_clean = df_clean[(df_clean['bmi'] >= 10) & (df_clean['bmi'] <= 60)]
print(f"Shape after BMI filter: {df_clean.shape}")

# Select Features for Training
# EXCLUDING 'index' (leakage)
# EXCLUDING 'age_years' (redundancy, keeping 'age' in days for precision)
feature_cols = [
    'age',          # in days
    'gender',       # 1=female, 2=male (usually)
    'height',       # cm
    'weight',       # kg
    'ap_hi',        # systolic
    'ap_lo',        # diastolic
    'cholesterol',  # 1, 2, 3
    'gluc',         # 1, 2, 3
    'smoke',        # 0, 1
    'alco',         # 0, 1
    'active',       # 0, 1
    'bmi'           # calculated
]

target_col = 'cardio'

X = df_clean[feature_cols]
y = df_clean[target_col]

print(f"\nFinal Training Features: {feature_cols}")

# ---------------------------------------------------------
# 4. TRAIN/TEST SPLIT
# ---------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
)

# ---------------------------------------------------------
# 5. MODEL TRAINING
# ---------------------------------------------------------
print("\nTraining CatBoost Classifier...")
# We use a relatively simple configuration to avoid overfitting,
# but with sufficient depth and iterations to learn patterns.
# CatBoost handles categorical features automatically, but here inputs are mostly numerical/ordinal integers.
# We treat cholesterol, gluc, smoke, alco, active, gender as categorical implies we should let CatBoost know,
# but for this dataset they are often treated as int. We'll let CatBoost auto-detect or treat as numeric (ordinal is fine for boostings).

model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.03,
    depth=6,
    loss_function='Logloss',
    eval_metric='AUC',
    random_seed=RANDOM_SEED,
    verbose=100,
    allow_writing_files=False
)

model.fit(X_train, y_train, eval_set=(X_test, y_test), early_stopping_rounds=50)

# ---------------------------------------------------------
# 6. EVALUATION & THRESHOLD TUNING
# ---------------------------------------------------------
print("\nEvaluating Model...")
y_pred_proba = model.predict_proba(X_test)[:, 1]

auc = roc_auc_score(y_test, y_pred_proba)
print(f"Test AUC: {auc:.4f}")

# Find Threshold for 90% Sensitivity
# effective_sensitivity = TP / (TP + FN)
from sklearn.metrics import roc_curve

fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
# We want TPR >= 0.90
target_sensitivity = 0.90
idx = np.argmax(tpr >= target_sensitivity)
required_threshold = thresholds[idx]
achieved_sensitivity = tpr[idx]
specificity_at_threshold = 1 - fpr[idx]

print(f"\n--- SAFETY THRESHOLD CALIBRATION ---")
print(f"Target Sensitivity: {target_sensitivity*100}%")
print(f"Required Threshold: {required_threshold:.4f}")
print(f"Achieved Sensitivity: {achieved_sensitivity:.4f}")
print(f"Specificity at this threshold: {specificity_at_threshold:.4f}")

# Save the model
model.save_model(MODEL_OUTPUT_PATH)
print(f"\nModel saved to: {MODEL_OUTPUT_PATH}")

# Save metrics for the API to load
import json

metrics = {
    "roc_auc": round(auc, 4),
    "sensitivity_target": 0.90,
    "threshold_90_sens": round(required_threshold, 4),
    "specificity_at_threshold": round(specificity_at_threshold, 4),
    "features": feature_cols
}

with open("model/model_metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("Metrics saved to model/model_metrics.json")

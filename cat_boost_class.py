# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 20:10:21 2026

@author: admin
"""

import pandas as pd
import numpy as np
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import matplotlib.pyplot as plt


# 1. Загрузка и быстрая чистка
df = pd.read_csv('CVD_risk_dataset.csv')
df.drop('id', axis=1, inplace=True)

#Очистка аномалий в давлении! 
df = df[(df['ap_hi'] >=60) &
        (df['ap_hi'] <=250)]
df = df[(df['ap_lo'] >=40) &
        (df['ap_lo'] <=150)]

df = df[(df['height'] >=140) &
        (df['height'] <=220)]
df = df[(df['weight'] >=40) &
        (df['weight'] <=200)]
df['age_years'] = (df['age'] / 365.25).astype(int)

df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
df['bmi'].round(1)


# 2. Подготовка данных
X = df.drop('cardio', axis=1)
y = df['cardio']

# Указвыаем индексы категриальных признаков для CatBoost

cat_features = ['gender', 'smoke', 'alco', 'active']

feature_names = X.columns.tolist()
print(feature_names)

monotone_constraints = {
    'age_years': 1,
    'ap_hi': 1,
    'ap_lo': 1,
    'bmi': 1,
    'cholesterol': 1,
    'gluc': 1
}

monotone_constraints_list = [
    monotone_constraints.get(col, 0)
    for col in feature_names
]

for f, m in zip(feature_names, monotone_constraints_list):
    print(f"{f:15s} → {m}")


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=0,
    stratify=y
)

# 3. Обучение модели
model = CatBoostClassifier(
    iterations=2000,
    learning_rate=0.03,
    depth=6,
    loss_function='Logloss',
    eval_metric='AUC',
    early_stopping_rounds=100,
    monotone_constraints=monotone_constraints_list,
    verbose=100
)

model.fit(
    X_train,
    y_train,
    cat_features=cat_features,
    eval_set=(X_test, y_test),
    early_stopping_rounds=50
)

#BACKGROUND_SIZE = 300  # 200–500 оптимально
#shap_background = X_train.sample(
    #n=BACKGROUND_SIZE,
    #random_state=0
#)
#shap_background.to_csv(
    #"shap_background_catboost_clean.csv",
    #index=False
#)
#np.save(
   # "shap_background_catboost.npy",
   # shap_background.values
#)


from sklearn.calibration import CalibratedClassifierCV
calibrated_model = CalibratedClassifierCV(
    model,
    method='sigmoid',
    cv=5
)
calibrated_model.fit(X_train, y_train)
calibrated_probs = calibrated_model.predict_proba(X_test)[:,1]



# 4. Проверка качества
preds_prob = model.predict_proba(X_test)[:, 1]
print(f"Лучший ROC-AUC:{roc_auc_score(y_test, preds_prob):.4f}")
print(classification_report(y_test, model.predict(X_test)))

from sklearn.calibration import calibration_curve
prob_true, prob_pred = calibration_curve(
    y_test,
    preds_prob,
    n_bins=10
)

from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
fpr, tpr, _ = roc_curve(y_test, preds_prob)


from sklearn.metrics import brier_score_loss
print("Before:", brier_score_loss(y_test, preds_prob))
print("After :", brier_score_loss(y_test, calibrated_probs))


#линия ниже диагонали → модель завышает риск
#выше → занижает риск
#зигзаги → мало данных / шум

prob_true_c, prob_pred_c = calibration_curve(
    y_test,
    calibrated_probs,
    n_bins=10
)
plt.figure()
plt.plot(prob_pred, prob_true, marker='o', label='Before calibration')
plt.plot(prob_pred_c, prob_true_c, marker='s', label='After calibration')
plt.plot([0,1], [0,1], linestyle='--')
plt.legend()
plt.xlabel("Predicted probability")
plt.ylabel("Observed probability")
plt.title("Calibration comparison")
plt.show()


#Distribution вероятностей
plt.figure()
plt.hist(preds_prob[y_test==0], bins=50, alpha=0.5, label="No CVD")
plt.hist(preds_prob[y_test==1], bins=50, alpha=0.5, label="CVD")
plt.xlabel("Predicted probability")
plt.ylabel("Count")
plt.legend()
plt.title("Probability distribution")
plt.show()


import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Общая важность признаков
shap.summary_plot(
    shap_values,
    X_test,
    plot_type="bar",
    max_display=10
)

# Распределение вкладов
shap.summary_plot(
    shap_values,
    X_test,
    max_display=10
)

# Монотонные признаки
shap.dependence_plot("bmi", shap_values, X_test)
shap.dependence_plot("ap_hi", shap_values, X_test)
shap.dependence_plot("cholesterol", shap_values, X_test)
shap.dependence_plot("gluc", shap_values, X_test)
shap.dependence_plot("alco", shap_values, X_test)

#import joblib
#joblib.dump(calibrated_model, "calibrated_catboost.pkl")
#model.save_model("catboost_cvd_model.cbm")



from sklearn.metrics import (
    roc_auc_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    brier_score_loss,
    roc_curve
)


# --- вероятности (ТОЛЬКО откалиброванные) ---
y_prob = calibrated_model.predict_proba(X_test)[:,1]

# --- бинарный прогноз при пороге 0.20  ---
THRESHOLD = 0.20
y_pred = (y_prob >= THRESHOLD).astype(int)

print("\n=== CLASSIFICATION REPORT ===")
print(classification_report(y_test, y_pred))

print("\n=== MAIN METRICS ===")
print(f"ROC-AUC        : {roc_auc_score(y_test, y_prob):.4f}")
print(f"Brier score    : {brier_score_loss(y_test, y_prob):.4f}")
print(f"Precision      : {precision_score(y_test, y_pred):.4f}")
print(f"Recall         : {recall_score(y_test, y_pred):.4f}")
print(f"F1-score       : {f1_score(y_test, y_pred):.4f}")

print("\n=== CONFUSION MATRIX ===")
print(confusion_matrix(y_test, y_pred))



fpr, tpr, _ = roc_curve(y_test, y_prob)
plt.figure()
plt.plot(fpr, tpr)
plt.plot([0,1], [0,1], linestyle='--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve (Calibrated Model)")
plt.show()

from sklearn.calibration import calibration_curve
prob_true, prob_pred = calibration_curve(
    y_test,
    y_prob,
    n_bins=10
)
plt.figure()
plt.plot(prob_pred, prob_true, marker='o')
plt.plot([0,1], [0,1], linestyle='--')
plt.xlabel("Predicted probability")
plt.ylabel("Observed probability")
plt.title("Calibration Curve (Final Model)")
plt.show()



thresholds = np.arange(0.05, 0.51, 0.05)
precisions = []
recalls = []

for t in thresholds:
    y_pred_t = (y_prob >= t).astype(int)
    precisions.append(precision_score(y_test, y_pred_t))
    recalls.append(recall_score(y_test, y_pred_t))

plt.figure()
plt.plot(thresholds, precisions, label="Precision")
plt.plot(thresholds, recalls, label="Recall")
plt.xlabel("Threshold")
plt.ylabel("Score")
plt.title("Precision / Recall vs Threshold")
plt.legend()
plt.show()



from sklearn.metrics import roc_auc_score, brier_score_loss

# вероятности
y_train_proba = model.predict_proba(X_train)[:, 1]
y_test_proba  = model.predict_proba(X_test)[:, 1]

# бинарные предсказания (порог 0.5 — временно)
y_train_pred = (y_train_proba >= 0.5).astype(int)
y_test_pred  = (y_test_proba  >= 0.5).astype(int)


metrics = {
    "ROC_AUC": {
        "train": roc_auc_score(y_train, y_train_proba),
        "test":  roc_auc_score(y_test, y_test_proba)
    },
    "Brier": {
        "train": brier_score_loss(y_train, y_train_proba),
        "test":  brier_score_loss(y_test, y_test_proba)
    }
}

metrics


from sklearn.model_selection import learning_curve

train_sizes, train_scores, val_scores = learning_curve(
    model,
    X,
    y,
    cv=5,
    scoring='roc_auc',
    train_sizes=np.linspace(0.1, 1.0, 5)
)

train_mean = train_scores.mean(axis=1)
val_mean   = val_scores.mean(axis=1)
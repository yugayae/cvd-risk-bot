CLINICAL_FACTOR_RISK = {
    "age_years": "increases",
    "ap_hi": "increases",
    "ap_lo": "increases",
    "bmi": "increases",
    "cholesterol": "increases",
    "gluc": "increases",  # High glucose ALWAYS increases risk
    "smoke": "increases",  # Smoking ALWAYS increases risk when present
    "alco": "increases",   # Alcohol ALWAYS increases risk when present
    "active": "reduces",   # Physical activity can be protective but cannot completely override risk factors
    "gender": "neutral"
}
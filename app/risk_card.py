from .localization import t, LOCALIZATION

def build_risk_card(
    lang: str,
    risk_probability: float,
    risk_category: str,
    confidence_level: str,
    confidence_note: str,
    clinical_explanation: list
):
    """
    Формирует клиническую Risk Card для врача
    """
    factors_text = ", ".join([f["factor"] for f in clinical_explanation])   
    headline = LOCALIZATION[lang]["risk_card"]["headline"][risk_category]
    summary_template = LOCALIZATION[lang]["risk_card"]["summary"][risk_category]
    summary = summary_template.format(factors=factors_text)

    summary = {
        "headline": headline,
        "risk_probability_percent": round(risk_probability * 100, 1),
        "confidence_level": confidence_level,
        "confidence_note": confidence_note,
        "key_factors": [
            {
                "factor": item["factor"],
                "direction": item["direction"]
            }
            for item in clinical_explanation[:3]
        ],
        "clinical_summary": generate_clinical_summary(
            lang,
            risk_category,
            clinical_explanation
        )
    }

    return summary


def generate_clinical_summary(
    lang: str,
    risk_category: str,
    factors: list
) -> str:

    factor_names = ", ".join([f["factor"] for f in factors[:3]])

    summary_template = LOCALIZATION[lang]["risk_card"]["summary"][risk_category]

    return summary_template.format(factors=factor_names)

from .localization import t


def input_sanity_check(patient, lang: str) -> list:
    warnings = []

    if patient.age_years < 40:
        warnings.append(
            t(lang, "warnings", "young_age")
        )

    if patient.ap_hi < patient.ap_lo:
        warnings.append(
            t(lang, "warnings", "bp_inversion")
        )

    # Calculate BMI if missing
    bmi = patient.bmi
    if bmi is None and patient.height > 0:
        bmi = patient.weight / ((patient.height / 100) ** 2)

    if bmi is not None and bmi < 18.5:
        warnings.append(
            t(lang, "warnings", "underweight")
        )

    if patient.age_years > 85:
        warnings.append(
            t(lang, "warnings", "very_old_age")
        )

    return warnings


def ood_check(patient, lang: str) -> list:
    warnings = []

    if patient.ap_hi > 200 or patient.ap_lo > 120:
        warnings.append(
            t(lang, "warnings", "extreme_bp")
        )

    # Calculate BMI if missing
    bmi = patient.bmi
    if bmi is None and patient.height > 0:
        bmi = patient.weight / ((patient.height / 100) ** 2)

    if bmi is not None and bmi > 50:
        warnings.append(
            t(lang, "warnings", "extreme_bmi")
        )

    return warnings


def uncertainty_warning(confidence_level: str, lang: str) -> list:
    if confidence_level == "low":
        return [
            t(lang, "warnings", "low_confidence")
        ]
    return []


def collect_safety_warnings(
    patient,
    confidence_level: str,
    lang: str
) -> list:
    """
    Collects all clinical safety warnings
    """

    warnings = []
    warnings.extend(input_sanity_check(patient, lang))
    warnings.extend(ood_check(patient, lang))
    warnings.extend(uncertainty_warning(confidence_level, lang))

    return warnings

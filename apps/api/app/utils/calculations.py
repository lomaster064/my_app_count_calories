from dataclasses import dataclass


ACTIVITY_MULTIPLIERS = {
    "low": 1.2,
    "medium": 1.55,
    "high": 1.725,
}


@dataclass
class MacroTargets:
    calories: float
    protein: float
    fat: float
    carbs: float


def calculate_bmr(weight_kg: float, height_cm: float, age_years: int, gender: str | None) -> float:
    if gender == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age_years + 5
    if gender == "female":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 161
    return 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 78


def calculate_tdee(bmr: float, activity_level: str) -> float:
    return bmr * ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return weight_kg / (height_m * height_m)


def recommended_weight_range(height_cm: float) -> tuple[float, float]:
    height_m = height_cm / 100
    min_weight = 18.5 * height_m * height_m
    max_weight = 24.9 * height_m * height_m
    return round(min_weight, 1), round(max_weight, 1)


def macro_targets(goal: str, tdee: float, weight_kg: float, training_level: str) -> MacroTargets:
    if goal == "cut":
        calories = tdee - 300
    else:
        calories = tdee + 250
    protein_per_kg = 1.6 if training_level == "beginner" else 2.0
    protein = protein_per_kg * weight_kg
    fat = 0.8 * weight_kg
    carbs = max((calories - protein * 4 - fat * 9) / 4, 0)
    return MacroTargets(
        calories=round(calories, 1),
        protein=round(protein, 1),
        fat=round(fat, 1),
        carbs=round(carbs, 1),
    )

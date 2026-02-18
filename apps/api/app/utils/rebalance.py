from dataclasses import dataclass


@dataclass
class RebalanceResult:
    new_targets: dict[str, float]
    workout_suggestion: str | None


def rebalance_day(
    target_calories: float,
    consumed_calories: float,
    remaining_meals: int,
    has_workout_today: bool,
    injury_constraints: list[str],
) -> RebalanceResult:
    if remaining_meals <= 0:
        return RebalanceResult(
            new_targets={"remaining_calories": 0.0},
            workout_suggestion=None,
        )

    remaining_calories = max(target_calories - consumed_calories, 0)
    per_meal_target = remaining_calories / remaining_meals

    workout_suggestion = None
    if consumed_calories > target_calories and has_workout_today:
        workout_suggestion = (
            "Предложить +10-15 минут LISS кардио или +1 подход в безопасных упражнениях."
        )
        if injury_constraints:
            workout_suggestion += " Исключить упражнения, связанные с травмами."

    return RebalanceResult(
        new_targets={
            "remaining_calories": round(remaining_calories, 1),
            "per_meal_target": round(per_meal_target, 1),
        },
        workout_suggestion=workout_suggestion,
    )

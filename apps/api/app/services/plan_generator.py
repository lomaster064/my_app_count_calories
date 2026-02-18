from datetime import date, timedelta
from random import shuffle

from sqlalchemy.orm import Session

from app.models.plan import Meal, MealDay, MealItem, MealPlan
from app.models.recipe import Recipe
from app.models.user import User
from app.utils.calculations import calculate_bmi, calculate_bmr, calculate_tdee, macro_targets, recommended_weight_range


def generate_meal_plan(db: Session, user: User, days: int = 30) -> dict:
    today = date.today()
    safe_days = max(1, min(days, 30))
    end = today + timedelta(days=safe_days - 1)

    age = 30
    if user.birth_date:
        age = today.year - user.birth_date.year
    bmr = calculate_bmr(user.current_weight_kg, user.height_cm, age, user.gender)
    tdee = calculate_tdee(bmr, user.activity_level)
    macros = macro_targets(user.goal, tdee, user.current_weight_kg, user.training_level)

    recipes = db.query(Recipe).all()
    if user.diet_type:
        recipes = [r for r in recipes if user.diet_type in r.tags]
    blocked = set(user.allergies + user.intolerances + user.dislikes)
    if blocked:
        recipes = [r for r in recipes if not any(tag in blocked for tag in r.tags)]

    shuffle(recipes)
    plan = MealPlan(
        user_id=user.id,
        start_date=today,
        end_date=end,
        target_calories=macros.calories,
        target_protein=macros.protein,
        target_fat=macros.fat,
        target_carbs=macros.carbs,
    )

    recipe_cycle = recipes or []
    for offset in range(safe_days):
        day_date = today + timedelta(days=offset)
        day = MealDay(
            date=day_date,
            total_calories=0,
            total_protein=0,
            total_fat=0,
            total_carbs=0,
        )
        meals = []
        for meal_index in range(user.meals_per_day):
            recipe = recipe_cycle[(offset + meal_index) % len(recipe_cycle)] if recipe_cycle else None
            meal = Meal(name=f"Meal {meal_index + 1}", calories=0, protein=0, fat=0, carbs=0)
            if recipe:
                meal_item = MealItem(recipe_id=recipe.id, servings=1)
                meal.items.append(meal_item)
                meal.calories = recipe.calories
                meal.protein = recipe.protein
                meal.fat = recipe.fat
                meal.carbs = recipe.carbs
            meals.append(meal)

        day.meals = meals
        day.total_calories = sum(m.calories for m in meals)
        day.total_protein = sum(m.protein for m in meals)
        day.total_fat = sum(m.fat for m in meals)
        day.total_carbs = sum(m.carbs for m in meals)
        plan.days.append(day)

    db.add(plan)
    db.commit()
    db.refresh(plan)

    bmi_current = calculate_bmi(user.current_weight_kg, user.height_cm)
    bmi_target = calculate_bmi(user.target_weight_kg, user.height_cm)
    weight_range = recommended_weight_range(user.height_cm)

    return {
        "plan": plan,
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "bmi_current": round(bmi_current, 1),
        "bmi_target": round(bmi_target, 1),
        "recommended_weight_range": weight_range,
        "disclaimer": "Рекомендации носят информационный характер и не являются медицинскими советами.",
    }

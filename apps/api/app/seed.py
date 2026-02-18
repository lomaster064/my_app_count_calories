from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.recipe import Recipe, RecipeIngredient
from app.models.workout import Exercise

RECIPES = [
    {
        "name": "Овсянка с ягодами",
        "description": "Сытная каша на завтрак.",
        "instructions": ["Сварить овсянку", "Добавить ягоды", "Подать"],
        "tags": ["vegetarian"],
        "calories": 320,
        "protein": 12,
        "fat": 8,
        "carbs": 48,
        "ingredients": [
            {"name": "Овсяные хлопья", "grams": 60},
            {"name": "Молоко", "grams": 150},
            {"name": "Ягоды", "grams": 80},
        ],
    },
    {
        "name": "Куриная грудка с киноа",
        "description": "Белковый обед.",
        "instructions": ["Запечь курицу", "Сварить киноа", "Смешать"],
        "tags": ["high-protein"],
        "calories": 420,
        "protein": 38,
        "fat": 10,
        "carbs": 45,
        "ingredients": [
            {"name": "Куриная грудка", "grams": 160},
            {"name": "Киноа", "grams": 80},
            {"name": "Овощи", "grams": 100},
        ],
    },
    {
        "name": "Лосось с овощами",
        "description": "Рыба с запеченными овощами.",
        "instructions": ["Запечь лосось", "Запечь овощи"],
        "tags": ["omega-3"],
        "calories": 450,
        "protein": 35,
        "fat": 22,
        "carbs": 25,
        "ingredients": [
            {"name": "Лосось", "grams": 150},
            {"name": "Брокколи", "grams": 120},
            {"name": "Морковь", "grams": 80},
        ],
    },
    {
        "name": "Тофу с овощным стир-фрай",
        "description": "Веганский ужин.",
        "instructions": ["Обжарить тофу", "Добавить овощи", "Добавить соус"],
        "tags": ["vegan"],
        "calories": 360,
        "protein": 20,
        "fat": 12,
        "carbs": 40,
        "ingredients": [
            {"name": "Тофу", "grams": 120},
            {"name": "Овощи", "grams": 150},
            {"name": "Соевый соус", "grams": 15},
        ],
    },
    {
        "name": "Греческий салат",
        "description": "Легкий салат с фетой.",
        "instructions": ["Нарезать овощи", "Добавить фету", "Заправить"],
        "tags": ["vegetarian"],
        "calories": 280,
        "protein": 9,
        "fat": 18,
        "carbs": 18,
        "ingredients": [
            {"name": "Огурцы", "grams": 100},
            {"name": "Помидоры", "grams": 100},
            {"name": "Фета", "grams": 50},
        ],
    },
    {
        "name": "Турецкий йогурт с орехами",
        "description": "Перекус с белком.",
        "instructions": ["Смешать йогурт и орехи"],
        "tags": ["vegetarian"],
        "calories": 230,
        "protein": 14,
        "fat": 12,
        "carbs": 16,
        "ingredients": [
            {"name": "Йогурт", "grams": 150},
            {"name": "Орехи", "grams": 20},
        ],
    },
    {
        "name": "Яичный омлет",
        "description": "Классический омлет.",
        "instructions": ["Взбить яйца", "Обжарить"],
        "tags": ["high-protein"],
        "calories": 260,
        "protein": 18,
        "fat": 18,
        "carbs": 4,
        "ingredients": [
            {"name": "Яйца", "grams": 120},
            {"name": "Молоко", "grams": 30},
        ],
    },
    {
        "name": "Буррито боул",
        "description": "Рис, фасоль и курица.",
        "instructions": ["Сварить рис", "Добавить фасоль и курицу"],
        "tags": ["high-protein"],
        "calories": 520,
        "protein": 35,
        "fat": 14,
        "carbs": 60,
        "ingredients": [
            {"name": "Рис", "grams": 120},
            {"name": "Фасоль", "grams": 100},
            {"name": "Курица", "grams": 120},
        ],
    },
    {
        "name": "Салат с тунцом",
        "description": "Салат с высоким белком.",
        "instructions": ["Смешать ингредиенты", "Заправить"],
        "tags": ["high-protein"],
        "calories": 310,
        "protein": 28,
        "fat": 12,
        "carbs": 18,
        "ingredients": [
            {"name": "Тунец", "grams": 120},
            {"name": "Листья салата", "grams": 60},
        ],
    },
    {
        "name": "Паста с индейкой",
        "description": "Паста с томатным соусом.",
        "instructions": ["Сварить пасту", "Приготовить индейку", "Смешать"],
        "tags": ["high-protein"],
        "calories": 540,
        "protein": 36,
        "fat": 12,
        "carbs": 72,
        "ingredients": [
            {"name": "Паста", "grams": 100},
            {"name": "Индейка", "grams": 140},
        ],
    },
    {
        "name": "Смузи протеиновый",
        "description": "Смузи с бананом и протеином.",
        "instructions": ["Смешать в блендере"],
        "tags": ["high-protein"],
        "calories": 300,
        "protein": 25,
        "fat": 5,
        "carbs": 40,
        "ingredients": [
            {"name": "Банан", "grams": 120},
            {"name": "Протеин", "grams": 30},
        ],
    },
    {
        "name": "Суп чечевичный",
        "description": "Сытный суп с чечевицей.",
        "instructions": ["Сварить чечевицу", "Добавить овощи"],
        "tags": ["vegan"],
        "calories": 350,
        "protein": 20,
        "fat": 6,
        "carbs": 52,
        "ingredients": [
            {"name": "Чечевица", "grams": 100},
            {"name": "Овощи", "grams": 150},
        ],
    },
    {
        "name": "Рис с овощами",
        "description": "Легкий гарнир.",
        "instructions": ["Сварить рис", "Добавить овощи"],
        "tags": ["vegan"],
        "calories": 280,
        "protein": 6,
        "fat": 4,
        "carbs": 56,
        "ingredients": [
            {"name": "Рис", "grams": 100},
            {"name": "Овощи", "grams": 120},
        ],
    },
    {
        "name": "Боул с нутом",
        "description": "Боул с нутом и овощами.",
        "instructions": ["Смешать нут и овощи", "Добавить соус"],
        "tags": ["vegan"],
        "calories": 390,
        "protein": 16,
        "fat": 10,
        "carbs": 58,
        "ingredients": [
            {"name": "Нут", "grams": 120},
            {"name": "Овощи", "grams": 140},
        ],
    },
    {
        "name": "Тост с авокадо",
        "description": "Завтрак с полезными жирами.",
        "instructions": ["Поджарить хлеб", "Намазать авокадо"],
        "tags": ["vegetarian"],
        "calories": 260,
        "protein": 7,
        "fat": 14,
        "carbs": 28,
        "ingredients": [
            {"name": "Хлеб", "grams": 60},
            {"name": "Авокадо", "grams": 70},
        ],
    },
    {
        "name": "Творог с фруктами",
        "description": "Белковый перекус.",
        "instructions": ["Смешать творог и фрукты"],
        "tags": ["vegetarian"],
        "calories": 220,
        "protein": 20,
        "fat": 6,
        "carbs": 18,
        "ingredients": [
            {"name": "Творог", "grams": 150},
            {"name": "Фрукты", "grams": 80},
        ],
    },
    {
        "name": "Салат с индейкой",
        "description": "Легкий салат с индейкой.",
        "instructions": ["Смешать ингредиенты"],
        "tags": ["high-protein"],
        "calories": 310,
        "protein": 30,
        "fat": 8,
        "carbs": 22,
        "ingredients": [
            {"name": "Индейка", "grams": 120},
            {"name": "Салат", "grams": 80},
        ],
    },
    {
        "name": "Банановый панкейк",
        "description": "Панкейк без сахара.",
        "instructions": ["Смешать ингредиенты", "Обжарить"],
        "tags": ["vegetarian"],
        "calories": 280,
        "protein": 10,
        "fat": 6,
        "carbs": 48,
        "ingredients": [
            {"name": "Банан", "grams": 100},
            {"name": "Яйцо", "grams": 50},
            {"name": "Овсяные хлопья", "grams": 40},
        ],
    },
    {
        "name": "Хумус с овощами",
        "description": "Перекус с растительным белком.",
        "instructions": ["Подать хумус с овощами"],
        "tags": ["vegan"],
        "calories": 240,
        "protein": 8,
        "fat": 10,
        "carbs": 28,
        "ingredients": [
            {"name": "Хумус", "grams": 80},
            {"name": "Овощи", "grams": 120},
        ],
    },
    {
        "name": "Чили с фасолью",
        "description": "Острый обед.",
        "instructions": ["Сварить фасоль", "Добавить томаты"],
        "tags": ["vegan"],
        "calories": 420,
        "protein": 18,
        "fat": 8,
        "carbs": 65,
        "ingredients": [
            {"name": "Фасоль", "grams": 150},
            {"name": "Томаты", "grams": 120},
        ],
    },
    {
        "name": "Ролл с лососем",
        "description": "Ролл с рыбой.",
        "instructions": ["Свернуть ролл"],
        "tags": ["omega-3"],
        "calories": 360,
        "protein": 22,
        "fat": 12,
        "carbs": 42,
        "ingredients": [
            {"name": "Лосось", "grams": 90},
            {"name": "Рис", "grams": 80},
            {"name": "Нори", "grams": 5},
        ],
    },
]

EXERCISES = [
    {
        "name": "Приседания",
        "description": "Базовое упражнение на ноги.",
        "muscle_group": "legs",
        "contraindications": ["knee"],
    },
    {
        "name": "Жим лежа",
        "description": "Упражнение на грудные мышцы.",
        "muscle_group": "chest",
        "contraindications": ["shoulder"],
    },
    {
        "name": "Тяга в наклоне",
        "description": "Упражнение на спину.",
        "muscle_group": "back",
        "contraindications": ["back"],
    },
    {
        "name": "Планка",
        "description": "Укрепление кора.",
        "muscle_group": "core",
        "contraindications": [],
    },
    {
        "name": "Выпады",
        "description": "Упражнение на ноги и ягодицы.",
        "muscle_group": "legs",
        "contraindications": ["knee"],
    },
    {
        "name": "Отжимания",
        "description": "Упражнение на грудь и трицепс.",
        "muscle_group": "chest",
        "contraindications": ["wrist"],
    },
]


def seed() -> None:
    db: Session = SessionLocal()
    try:
        if db.query(Recipe).count() == 0:
            for recipe_data in RECIPES:
                recipe = Recipe(
                    name=recipe_data["name"],
                    description=recipe_data["description"],
                    instructions=recipe_data["instructions"],
                    tags=recipe_data["tags"],
                    calories=recipe_data["calories"],
                    protein=recipe_data["protein"],
                    fat=recipe_data["fat"],
                    carbs=recipe_data["carbs"],
                )
                for ingredient in recipe_data["ingredients"]:
                    recipe.ingredients.append(RecipeIngredient(**ingredient))
                db.add(recipe)

        if db.query(Exercise).count() == 0:
            for exercise_data in EXERCISES:
                db.add(Exercise(**exercise_data))

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()

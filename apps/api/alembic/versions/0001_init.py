"""init

Revision ID: 0001
Revises: 
Create Date: 2024-01-01
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("gender", sa.String(length=20), nullable=True),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("height_cm", sa.Float(), nullable=False),
        sa.Column("current_weight_kg", sa.Float(), nullable=False),
        sa.Column("target_weight_kg", sa.Float(), nullable=False),
        sa.Column("goal", sa.Enum("cut", "bulk", name="goal_enum"), nullable=False),
        sa.Column("activity_level", sa.Enum("low", "medium", "high", name="activity_enum"), nullable=False),
        sa.Column("training_level", sa.Enum("beginner", "intermediate", "advanced", name="training_enum"), nullable=False),
        sa.Column("allergies", postgresql.JSONB(), nullable=False),
        sa.Column("intolerances", postgresql.JSONB(), nullable=False),
        sa.Column("diet_type", sa.String(length=50), nullable=True),
        sa.Column("dislikes", postgresql.JSONB(), nullable=False),
        sa.Column("meals_per_day", sa.Integer(), nullable=False),
        sa.Column("meal_time_preferences", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "injuries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("injury_type", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("restricted_exercises", postgresql.JSONB(), nullable=False),
    )
    op.create_index("ix_injuries_user_id", "injuries", ["user_id"], unique=False)

    op.create_table(
        "recipes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("instructions", postgresql.JSONB(), nullable=False),
        sa.Column("tags", postgresql.JSONB(), nullable=False),
        sa.Column("calories", sa.Float(), nullable=False),
        sa.Column("protein", sa.Float(), nullable=False),
        sa.Column("fat", sa.Float(), nullable=False),
        sa.Column("carbs", sa.Float(), nullable=False),
    )

    op.create_table(
        "recipe_ingredients",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("recipe_id", sa.Integer(), sa.ForeignKey("recipes.id"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("grams", sa.Float(), nullable=False),
    )

    op.create_table(
        "meal_plans",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("target_calories", sa.Float(), nullable=False),
        sa.Column("target_protein", sa.Float(), nullable=False),
        sa.Column("target_fat", sa.Float(), nullable=False),
        sa.Column("target_carbs", sa.Float(), nullable=False),
    )

    op.create_table(
        "meal_days",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("plan_id", sa.Integer(), sa.ForeignKey("meal_plans.id"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("total_calories", sa.Float(), nullable=False),
        sa.Column("total_protein", sa.Float(), nullable=False),
        sa.Column("total_fat", sa.Float(), nullable=False),
        sa.Column("total_carbs", sa.Float(), nullable=False),
    )

    op.create_table(
        "meals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("day_id", sa.Integer(), sa.ForeignKey("meal_days.id"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("calories", sa.Float(), nullable=False),
        sa.Column("protein", sa.Float(), nullable=False),
        sa.Column("fat", sa.Float(), nullable=False),
        sa.Column("carbs", sa.Float(), nullable=False),
    )

    op.create_table(
        "meal_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("meal_id", sa.Integer(), sa.ForeignKey("meals.id"), nullable=False),
        sa.Column("recipe_id", sa.Integer(), sa.ForeignKey("recipes.id"), nullable=False),
        sa.Column("servings", sa.Float(), nullable=False),
    )

    op.create_table(
        "workout_plans",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("template", sa.String(length=50), nullable=False),
    )

    op.create_table(
        "workout_days",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("plan_id", sa.Integer(), sa.ForeignKey("workout_plans.id"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
    )

    op.create_table(
        "workout_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("day_id", sa.Integer(), sa.ForeignKey("workout_days.id"), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
    )

    op.create_table(
        "exercises",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("muscle_group", sa.String(length=100), nullable=False),
        sa.Column("contraindications", postgresql.JSONB(), nullable=False),
    )

    op.create_table(
        "workout_exercises",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.Integer(), sa.ForeignKey("workout_sessions.id"), nullable=False),
        sa.Column("exercise_id", sa.Integer(), sa.ForeignKey("exercises.id"), nullable=False),
        sa.Column("sets", sa.Integer(), nullable=False),
        sa.Column("reps", sa.Integer(), nullable=False),
        sa.Column("rest_seconds", sa.Integer(), nullable=False),
        sa.Column("rpe", sa.Float(), nullable=False),
    )

    op.create_table(
        "meal_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("logged_date", sa.Date(), nullable=False),
        sa.Column("notes", sa.String(length=255), nullable=False),
        sa.Column("total_calories", sa.Float(), nullable=False),
        sa.Column("total_protein", sa.Float(), nullable=False),
        sa.Column("total_fat", sa.Float(), nullable=False),
        sa.Column("total_carbs", sa.Float(), nullable=False),
        sa.Column("photo_url", sa.String(length=255), nullable=True),
        sa.Column("ai_raw", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "meal_log_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("meal_log_id", sa.Integer(), sa.ForeignKey("meal_logs.id"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("grams_estimate", sa.Float(), nullable=False),
        sa.Column("calories", sa.Float(), nullable=False),
        sa.Column("protein", sa.Float(), nullable=False),
        sa.Column("fat", sa.Float(), nullable=False),
        sa.Column("carbs", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("meal_log_items")
    op.drop_table("meal_logs")
    op.drop_table("workout_exercises")
    op.drop_table("exercises")
    op.drop_table("workout_sessions")
    op.drop_table("workout_days")
    op.drop_table("workout_plans")
    op.drop_table("meal_items")
    op.drop_table("meals")
    op.drop_table("meal_days")
    op.drop_table("meal_plans")
    op.drop_table("recipe_ingredients")
    op.drop_table("recipes")
    op.drop_table("injuries")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.execute("DROP TYPE goal_enum")
    op.execute("DROP TYPE activity_enum")
    op.execute("DROP TYPE training_enum")

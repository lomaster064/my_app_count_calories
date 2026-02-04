"""water logs

Revision ID: 0002
Revises: 0001
Create Date: 2024-01-02
"""

from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "water_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("logged_date", sa.Date(), nullable=False),
        sa.Column("amount_ml", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_water_logs_user_id", "water_logs", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_water_logs_user_id", table_name="water_logs")
    op.drop_table("water_logs")

"""refactor_user_model

Revision ID: c2e46272f317
Revises: daab5986593e
Create Date: 2026-07-20 11:20:55.795578

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "c2e46272f317"
down_revision: Union[str, Sequence[str], None] = "daab5986593e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


user_role = postgresql.ENUM(
    "USER",
    "ADMIN",
    name="user_role",
    create_type=False,
)


def upgrade() -> None:
    """Upgrade schema."""

    # Create PostgreSQL enum type
    user_role.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role,
            nullable=False,
            server_default="USER",
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "is_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "last_login_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.drop_column("users", "name")

    op.alter_column("users", "role", server_default=None)
    op.alter_column("users", "is_active", server_default=None)
    op.alter_column("users", "is_verified", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""

    op.add_column(
        "users",
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),
    )

    op.drop_column("users", "last_login_at")
    op.drop_column("users", "is_verified")
    op.drop_column("users", "is_active")
    op.drop_column("users", "role")

    # Drop PostgreSQL enum type
    user_role.drop(op.get_bind(), checkfirst=True)
"""add sellers and seller applications

Revision ID: fdf4c94b022f
Revises: cd3ef6afccac
Create Date: 2026-07-24 23:54:49.750999
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fdf4c94b022f"
down_revision: Union[str, Sequence[str], None] = "cd3ef6afccac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "seller_applications",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "APPROVED",
                "REJECTED",
                name="sellerapplicationstatus",
            ),
            server_default="PENDING",
            nullable=False,
        ),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("phone", sa.String(length=30), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.Column("reviewed_by", sa.UUID(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["reviewed_by"],
            ["users.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_seller_applications_status"),
        "seller_applications",
        ["status"],
        unique=False,
    )

    op.create_index(
        op.f("ix_seller_applications_user_id"),
        "seller_applications",
        ["user_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_seller_applications_reviewed_by"),
        "seller_applications",
        ["reviewed_by"],
        unique=False,
    )

    op.create_table(
        "sellers",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("application_id", sa.UUID(), nullable=True),
        sa.Column(
            "seller_type",
            sa.Enum(
                "INDIVIDUAL",
                "RETAILER",
                name="sellertype",
            ),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "ACTIVE",
                "SUSPENDED",
                "BANNED",
                name="sellerstatus",
            ),
            nullable=False,
        ),
        sa.Column("display_name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("logo_key", sa.String(length=255), nullable=True),
        sa.Column("banner_key", sa.String(length=255), nullable=True),
        sa.Column("support_email", sa.String(length=255), nullable=True),
        sa.Column("support_phone", sa.String(length=30), nullable=True),
        sa.Column(
            "average_rating",
            sa.Float(),
            server_default="0",
            nullable=False,
        ),
        sa.Column(
            "total_reviews",
            sa.Integer(),
            server_default="0",
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["seller_applications.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("application_id"),
    )

    op.create_index(
        op.f("ix_sellers_user_id"),
        "sellers",
        ["user_id"],
        unique=True,
    )

    op.create_index(
        op.f("ix_sellers_application_id"),
        "sellers",
        ["application_id"],
        unique=True,
    )

    op.create_index(
        op.f("ix_sellers_seller_type"),
        "sellers",
        ["seller_type"],
        unique=False,
    )

    op.create_index(
        op.f("ix_sellers_status"),
        "sellers",
        ["status"],
        unique=False,
    )

    # Soft delete rollout
    op.add_column(
        "brands",
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "categories",
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "products",
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "user_profiles",
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "variant_options",
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "variant_types",
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("variant_types", "deleted_at")
    op.drop_column("variant_options", "deleted_at")
    op.drop_column("users", "deleted_at")
    op.drop_column("user_profiles", "deleted_at")
    op.drop_column("products", "deleted_at")
    op.drop_column("categories", "deleted_at")
    op.drop_column("brands", "deleted_at")

    op.drop_index(
        op.f("ix_sellers_status"),
        table_name="sellers",
    )

    op.drop_index(
        op.f("ix_sellers_seller_type"),
        table_name="sellers",
    )

    op.drop_index(
        op.f("ix_sellers_application_id"),
        table_name="sellers",
    )

    op.drop_index(
        op.f("ix_sellers_user_id"),
        table_name="sellers",
    )

    op.drop_table("sellers")

    op.drop_index(
        op.f("ix_seller_applications_reviewed_by"),
        table_name="seller_applications",
    )

    op.drop_index(
        op.f("ix_seller_applications_user_id"),
        table_name="seller_applications",
    )

    op.drop_index(
        op.f("ix_seller_applications_status"),
        table_name="seller_applications",
    )

    op.drop_table("seller_applications")
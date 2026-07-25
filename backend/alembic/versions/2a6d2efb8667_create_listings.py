"""create listings

Revision ID: 2a6d2efb8667
Revises: fdf4c94b022f
Create Date: 2026-07-25 11:31:20.518720

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2a6d2efb8667"
down_revision: Union[str, Sequence[str], None] = "fdf4c94b022f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "listings",
        sa.Column("seller_id", sa.UUID(), nullable=False),
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("variant_option_id", sa.UUID(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "ACTIVE",
                "INACTIVE",
                "SUSPENDED",
                name="listingstatus",
            ),
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
            ["seller_id"],
            ["sellers.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["variant_option_id"],
            ["variant_options.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_listings_price"),
        "listings",
        ["price"],
        unique=False,
    )

    op.create_index(
        op.f("ix_listings_product_id"),
        "listings",
        ["product_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_listings_seller_id"),
        "listings",
        ["seller_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_listings_status"),
        "listings",
        ["status"],
        unique=False,
    )

    op.create_index(
        op.f("ix_listings_variant_option_id"),
        "listings",
        ["variant_option_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_listings_variant_option_id"),
        table_name="listings",
    )

    op.drop_index(
        op.f("ix_listings_status"),
        table_name="listings",
    )

    op.drop_index(
        op.f("ix_listings_seller_id"),
        table_name="listings",
    )

    op.drop_index(
        op.f("ix_listings_product_id"),
        table_name="listings",
    )

    op.drop_index(
        op.f("ix_listings_price"),
        table_name="listings",
    )

    op.drop_table("listings")
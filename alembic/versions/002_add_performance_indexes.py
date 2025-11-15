"""Add performance indexes

Revision ID: 002
Revises: 001
Create Date: 2024-11-16

"""

from alembic import op


revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Performance indexes for users table
    op.create_index("ix_users_email_active", "users", ["email", "is_active"])
    op.create_index("ix_users_created_at", "users", ["created_at"])

    # Performance indexes for subscriptions
    op.create_index(
        "ix_subscriptions_user_active",
        "subscriptions",
        ["user_id", "is_active"],
    )
    op.create_index("ix_subscriptions_tier", "subscriptions", ["tier"])
    op.create_index(
        "ix_subscriptions_expires_at",
        "subscriptions",
        ["expires_at"],
    )

    # Performance indexes for payments
    op.create_index(
        "ix_payments_user_status",
        "payments",
        ["user_id", "status"],
    )
    op.create_index("ix_payments_created_at", "payments", ["created_at"])

    # Composite indexes for common queries
    op.create_index(
        "ix_users_faceit_active",
        "users",
        ["faceit_id", "is_active"],
    )


def downgrade() -> None:
    op.drop_index("ix_users_faceit_active", table_name="users")
    op.drop_index("ix_payments_created_at", table_name="payments")
    op.drop_index("ix_payments_user_status", table_name="payments")
    op.drop_index("ix_subscriptions_expires_at", table_name="subscriptions")
    op.drop_index("ix_subscriptions_tier", table_name="subscriptions")
    op.drop_index("ix_subscriptions_user_active", table_name="subscriptions")
    op.drop_index("ix_users_created_at", table_name="users")
    op.drop_index("ix_users_email_active", table_name="users")

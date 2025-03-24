"""Add uuid as primary key

Revision ID: 904d65f42e0e
Revises: 
Create Date: 2025-03-23 22:14:57.325450

"""
from typing import Sequence, Union
from alembic import op
import uuid
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '904d65f42e0e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Step 1: Add the uuid column without the NOT NULL constraint
    op.add_column('users', sa.Column('uuid', sa.UUID(), nullable=True, unique=True))

    # Step 2: Populate the uuid column with random UUIDs
    op.execute('UPDATE users SET uuid = gen_random_uuid()')

    # Step 3: Alter the column to add the NOT NULL constraint
    op.alter_column('users', 'uuid', nullable=False)


def downgrade():
    # Revert changes in the downgrade method
    op.add_column('users', sa.Column('id', sa.Integer(), nullable=False))
    op.create_primary_key('users_pkey', 'users', ['id'])  # Restore original primary key

    op.drop_column('users', 'uuid')

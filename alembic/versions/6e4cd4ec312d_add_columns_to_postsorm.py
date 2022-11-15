"""add columns to postsorm

Revision ID: 6e4cd4ec312d
Revises: cfcc4fd02d18
Create Date: 2022-11-14 20:46:33.400361

"""
from alembic import op
import sqlalchemy as sa

# alembic --help
# alembic heads TO CHECK NEW VERSION
# alembic current TO CHECK CURRENT VERSION
# revision identifiers, used by Alembic.
revision = '6e4cd4ec312d'
down_revision = 'cfcc4fd02d18'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('postorm', sa.Column('content', sa.String(), nullable=False))
    pass
# alembic upgrade head / code / +1


def downgrade() -> None:
    op.drop_column('postorm', 'content')
    pass
# alembic downgrade head / code / +1

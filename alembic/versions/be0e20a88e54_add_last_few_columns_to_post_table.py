"""add last few columns to post table

Revision ID: be0e20a88e54
Revises: d3c47a6ea19e
Create Date: 2022-11-14 20:53:50.744085

"""
from alembic import op
import sqlalchemy as sa

# alembic --help
# alembic heads TO CHECK NEW VERSION
# alembic current TO CHECK CURRENT VERSION
# revision identifiers, used by Alembic.
revision = 'be0e20a88e54'
down_revision = 'd3c47a6ea19e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('postorm',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('postorm',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                            server_default=sa.text('NOW()')),)
    pass
# alembic upgrade head / code / +1


def downgrade() -> None:
    op.drop_column('postorm', 'published')
    op.drop_column('postorm', 'created_at')
    pass
# alembic downgrade head / code / +1

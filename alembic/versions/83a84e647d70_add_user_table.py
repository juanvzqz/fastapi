"""add user table

Revision ID: 83a84e647d70
Revises: 6e4cd4ec312d
Create Date: 2022-11-14 20:50:02.399559

"""
from alembic import op
import sqlalchemy as sa

# alembic --help
# alembic heads TO CHECK NEW VERSION
# alembic current TO CHECK CURRENT VERSION
# revision identifiers, used by Alembic.
revision = '83a84e647d70'
down_revision = '6e4cd4ec312d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass
# alembic upgrade head / code / +1


def downgrade() -> None:
    op.drop_table('users')
    pass
# alembic downgrade head / code / +1

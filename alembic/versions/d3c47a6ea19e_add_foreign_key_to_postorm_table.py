"""add foreign key to postorm table

Revision ID: d3c47a6ea19e
Revises: 83a84e647d70
Create Date: 2022-11-14 20:51:47.022306

"""
from alembic import op
import sqlalchemy as sa

# alembic --help
# alembic heads TO CHECK NEW VERSION
# alembic current TO CHECK CURRENT VERSION
# revision identifiers, used by Alembic.
revision = 'd3c47a6ea19e'
down_revision = '83a84e647d70'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('postorm', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('postorm_users_fk',
                          source_table="postorm",
                          referent_table="users",
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete="CASCADE")
    pass
# alembic upgrade head / code / +1


def downgrade() -> None:
    op.drop_constraint('postorm_users_fk', table_name="posts")
    op.drop_column('postorm', 'owner_id')
    pass
# alembic downgrade head / code / +1

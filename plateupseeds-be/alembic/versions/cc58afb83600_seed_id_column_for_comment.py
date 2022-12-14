"""seed_id column for Comment

Revision ID: cc58afb83600
Revises: b94fb79e6463
Create Date: 2022-10-14 22:32:48.191188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc58afb83600'
down_revision = 'b94fb79e6463'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('seed_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comments', 'seeds', ['seed_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_column('comments', 'seed_id')
    # ### end Alembic commands ###

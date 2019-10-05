"""empty message

Revision ID: 95c7d24825d1
Revises: 7eada82314d7
Create Date: 2019-09-30 22:33:34.332048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95c7d24825d1'
down_revision = '7eada82314d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'seeking_description')
    # ### end Alembic commands ###

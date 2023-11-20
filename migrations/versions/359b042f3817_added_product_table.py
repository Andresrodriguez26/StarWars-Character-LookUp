"""added product table

Revision ID: 359b042f3817
Revises: e5c780d1a680
Create Date: 2023-11-19 21:13:37.189190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '359b042f3817'
down_revision = 'e5c780d1a680'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('prod_id', sa.String(), nullable=False),
    sa.Column('character_name', sa.String(length=50), nullable=False),
    sa.Column('character_image', sa.String(), nullable=True),
    sa.Column('homeworld', sa.String(length=200), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('prod_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    # ### end Alembic commands ###
"""empty message

Revision ID: 74cd7b5ca920
Revises: 
Create Date: 2020-01-08 21:38:19.367668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74cd7b5ca920'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=True),
    sa.Column('password_hash', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###

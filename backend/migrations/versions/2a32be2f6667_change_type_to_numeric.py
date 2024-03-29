"""change type to numeric

Revision ID: 2a32be2f6667
Revises: ce0a164a74cf
Create Date: 2024-02-07 16:44:33.661975

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2a32be2f6667'
down_revision = 'ce0a164a74cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('budget', schema=None) as batch_op:
        batch_op.alter_column('amount',
               existing_type=mysql.DECIMAL(precision=10, scale=2),
               type_=sa.Numeric(precision=20, scale=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('budget', schema=None) as batch_op:
        batch_op.alter_column('amount',
               existing_type=sa.Numeric(precision=20, scale=2),
               type_=mysql.DECIMAL(precision=10, scale=2),
               existing_nullable=False)

    # ### end Alembic commands ###

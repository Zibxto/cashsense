"""change type

Revision ID: 89b260cb92ca
Revises: b03c0097e3c1
Create Date: 2024-02-07 13:29:29.530184

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '89b260cb92ca'
down_revision = 'b03c0097e3c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('budget', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=300),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('start_date',
               existing_type=mysql.DATETIME(),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('end_date',
               existing_type=mysql.DATETIME(),
               type_=sa.String(length=120),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('budget', schema=None) as batch_op:
        batch_op.alter_column('end_date',
               existing_type=sa.String(length=120),
               type_=mysql.DATETIME(),
               existing_nullable=False)
        batch_op.alter_column('start_date',
               existing_type=sa.String(length=120),
               type_=mysql.DATETIME(),
               existing_nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.String(length=120),
               type_=mysql.VARCHAR(length=300),
               existing_nullable=False)

    # ### end Alembic commands ###

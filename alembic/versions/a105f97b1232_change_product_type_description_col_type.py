"""change product type description col type

Revision ID: a105f97b1232
Revises: f31621de7252
Create Date: 2020-01-03 11:36:13.470040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a105f97b1232'
down_revision = 'f31621de7252'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('product_type_description', 'value', type_=sa.UnicodeText(), nullable=False)


def downgrade():
    op.alter_column('product_type_description', 'value', type_=sa.String(50), nullable=False)


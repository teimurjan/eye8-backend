"""create groups

Revision ID: e0cf3ab3c3e5
Revises: 3c5032794b44
Create Date: 2019-06-11 17:29:07.457463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0cf3ab3c3e5'
down_revision = '3c5032794b44'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    conn.execute("""INSERT INTO "group" (id,name) VALUES (1,'client'),(2,'manager'),(3,'admin');""")


def downgrade():
    conn = op.get_bind()

    conn.execute("""
        DELETE FROM "group"
        WHERE name IN ('client','manager','admin');
    """)

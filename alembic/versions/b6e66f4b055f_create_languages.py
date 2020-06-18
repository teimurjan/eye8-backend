"""create languages

Revision ID: b6e66f4b055f
Revises: e0cf3ab3c3e5
Create Date: 2019-06-12 11:01:55.205096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6e66f4b055f'
down_revision = 'e0cf3ab3c3e5'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    conn.execute("""INSERT INTO "language" (name) VALUES ('en-US'),('ru-RU');""")


def downgrade():
    conn = op.get_bind()

    conn.execute("""
        DELETE FROM "language"
        WHERE name IN ('en-US','ru-RU');
    """)

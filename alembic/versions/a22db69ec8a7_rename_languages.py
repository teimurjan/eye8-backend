"""rename languages

Revision ID: a22db69ec8a7
Revises: 990992000458
Create Date: 2020-04-06 16:07:11.918761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a22db69ec8a7'
down_revision = '990992000458'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    conn.execute("""UPDATE "language" SET name='en' WHERE name='en-US';""")
    conn.execute("""UPDATE "language" SET name='ru' WHERE name='ru-RU';""")


def downgrade():
    conn = op.get_bind()

    conn.execute("""UPDATE "language" SET name='en-US' WHERE name='en';""")
    conn.execute("""UPDATE "language" SET name='ru-RU' WHERE name='ru';""")

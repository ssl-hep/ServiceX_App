"""multipath support

Revision ID: 79d404108ebe
Revises: 5893086ec440
Create Date: 2022-01-25 10:12:23.947313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79d404108ebe'
down_revision = '5893086ec440'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('files', 'file_path')
    op.add_column('files', sa.Column('paths', sa.Text()))
    op.execute(
        'UPDATE "files" SET paths = "old"'
    )
    op.alter_column('files', 'paths', nullable=False)


def downgrade():
    op.drop_column('files', 'paths')
    op.add_column('files', sa.Column('file_path', sa.String(length=512), nullable=False))

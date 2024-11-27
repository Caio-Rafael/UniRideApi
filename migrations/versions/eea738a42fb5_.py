"""empty message

Revision ID: eea738a42fb5
Revises: 
Create Date: 2024-11-25 22:53:42.088481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eea738a42fb5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carona',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('motorista_id', sa.Integer(), nullable=False),
    sa.Column('destino', sa.String(length=255), nullable=False),
    sa.Column('horario', sa.String(length=255), nullable=False),
    sa.Column('vagas', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('carona')
    # ### end Alembic commands ###

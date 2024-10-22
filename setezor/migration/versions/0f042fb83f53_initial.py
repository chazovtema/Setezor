"""initial

Revision ID: 0f042fb83f53
Revises: 
Create Date: 2023-01-28 12:18:02.981161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f042fb83f53'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('object_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('object_type', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('objects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('object_type', sa.String(length=100), nullable=True),
    sa.Column('os', sa.String(length=150), nullable=True),
    sa.Column('status', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.Column('created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('started', sa.DateTime(), nullable=True),
    sa.Column('finished', sa.DateTime(), nullable=True),
    sa.Column('params', sa.Text(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mac_addresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mac', sa.String(length=17), nullable=True),
    sa.Column('object', sa.Integer(), nullable=False),
    sa.Column('vendor', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['object'], ['objects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ip_addresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mac', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=15), nullable=False),
    sa.Column('domain_name', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['mac'], ['mac_addresses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('l3_link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('child_ip', sa.Integer(), nullable=False),
    sa.Column('parent_ip', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['child_ip'], ['ip_addresses.id'], ),
    sa.ForeignKeyConstraint(['parent_ip'], ['ip_addresses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip', sa.Integer(), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('protocol', sa.String(length=10), nullable=True),
    sa.Column('service_name', sa.String(length=100), nullable=True),
    sa.Column('state', sa.String(length=15), nullable=True),
    sa.Column('product', sa.String(length=100), nullable=True),
    sa.Column('extra_info', sa.String(length=150), nullable=True),
    sa.Column('version', sa.String(length=100), nullable=True),
    sa.Column('os_type', sa.String(length=100), nullable=True),
    sa.Column('cpe', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['ip'], ['ip_addresses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('screenshots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.Column('screenshot_path', sa.String(length=100), nullable=True),
    sa.Column('task', sa.Integer(), nullable=True),
    sa.Column('domain', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['port'], ['ports.id'], ),
    sa.ForeignKeyConstraint(['task'], ['tasks.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('screenshot_path')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('screenshots')
    op.drop_table('ports')
    op.drop_table('l3_link')
    op.drop_table('ip_addresses')
    op.drop_table('mac_addresses')
    op.drop_table('tasks')
    op.drop_table('objects')
    op.drop_table('object_types')
    # ### end Alembic commands ###
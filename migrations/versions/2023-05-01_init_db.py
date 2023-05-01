"""Init db

Revision ID: 10591ffe4527
Revises: 
Create Date: 2023-05-01 23:50:31.101572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10591ffe4527'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feed',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('last_built_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.String(), nullable=True),
    sa.Column('is_update_enabled', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feed_id'), 'feed', ['id'], unique=False)
    op.create_index(op.f('ix_feed_url'), 'feed', ['url'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_full_name'), 'user', ['full_name'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('guid', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('published_at', sa.DateTime(), nullable=True),
    sa.Column('feed_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_guid'), 'item', ['guid'], unique=False)
    op.create_index(op.f('ix_item_id'), 'item', ['id'], unique=False)
    op.create_index(op.f('ix_item_url'), 'item', ['url'], unique=False)
    op.create_table('subscription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('feed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'feed_id', name='unique_user_feed')
    )
    op.create_index(op.f('ix_subscription_id'), 'subscription', ['id'], unique=False)
    op.create_table('read_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_read_status_id'), 'read_status', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_read_status_id'), table_name='read_status')
    op.drop_table('read_status')
    op.drop_index(op.f('ix_subscription_id'), table_name='subscription')
    op.drop_table('subscription')
    op.drop_index(op.f('ix_item_url'), table_name='item')
    op.drop_index(op.f('ix_item_id'), table_name='item')
    op.drop_index(op.f('ix_item_guid'), table_name='item')
    op.drop_table('item')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_full_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_feed_url'), table_name='feed')
    op.drop_index(op.f('ix_feed_id'), table_name='feed')
    op.drop_table('feed')
    # ### end Alembic commands ###

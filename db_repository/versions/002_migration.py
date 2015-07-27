from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=64), nullable=False),
    Column('password', VARCHAR(length=255), nullable=False),
    Column('reset_password_token', VARCHAR(length=100), nullable=False),
    Column('email', VARCHAR(length=120), nullable=False),
    Column('created', DATETIME),
    Column('deleted', DATETIME),
    Column('is_enabled', BOOLEAN, nullable=False),
    Column('first_name', VARCHAR(length=100), nullable=False),
    Column('last_name', VARCHAR(length=100), nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['is_enabled'].drop()
    pre_meta.tables['user'].columns['username'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['is_enabled'].create()
    pre_meta.tables['user'].columns['username'].create()

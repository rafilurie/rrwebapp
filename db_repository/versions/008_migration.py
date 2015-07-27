from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('first_name', VARCHAR(length=120), nullable=False),
    Column('last_name', VARCHAR(length=120), nullable=False),
    Column('username', VARCHAR(length=120), nullable=False),
    Column('password', VARCHAR(length=255), nullable=False),
    Column('created', DATETIME),
    Column('reset_password_token', VARCHAR(length=100), nullable=False),
    Column('deleted', DATETIME),
    Column('is_enabled', BOOLEAN, nullable=False),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=120), nullable=False),
    Column('last_name', String(length=120), nullable=False),
    Column('email', String(length=120), nullable=False),
    Column('password', String(length=255), nullable=False),
    Column('created', DateTime),
    Column('reset_password_token', String(length=100), nullable=False),
    Column('deleted', DateTime),
    Column('is_enabled', Boolean, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['username'].drop()
    post_meta.tables['user'].columns['email'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['username'].create()
    post_meta.tables['user'].columns['email'].drop()

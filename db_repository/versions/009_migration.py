from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=120), nullable=False),
    Column('last_name', String(length=120), nullable=False),
    Column('email', String(length=120), nullable=False),
    Column('password', String(length=255), nullable=False),
    Column('created', DateTime),
    Column('about_me', String(length=140)),
    Column('job_title', String(length=120)),
    Column('company', String(length=64)),
    Column('linkedin_url', String(length=140)),
    Column('reset_password_token', String(length=100), nullable=False),
    Column('deleted', DateTime),
    Column('is_enabled', Boolean, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['about_me'].create()
    post_meta.tables['user'].columns['company'].create()
    post_meta.tables['user'].columns['job_title'].create()
    post_meta.tables['user'].columns['linkedin_url'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['about_me'].drop()
    post_meta.tables['user'].columns['company'].drop()
    post_meta.tables['user'].columns['job_title'].drop()
    post_meta.tables['user'].columns['linkedin_url'].drop()

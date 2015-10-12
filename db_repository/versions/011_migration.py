from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
comment = Table('comment', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('content', VARCHAR(length=100000)),
    Column('created', DATETIME),
    Column('deleted', DATETIME),
    Column('photo_id', INTEGER),
)

perpetrator = Table('perpetrator', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('created', DATETIME),
    Column('deleted', DATETIME),
    Column('name', VARCHAR(length=40), nullable=False),
    Column('display_name', VARCHAR(length=40)),
    Column('user_id', INTEGER),
)

photo = Table('photo', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('created', DATETIME),
    Column('when', DATETIME),
    Column('deleted', DATETIME),
    Column('extension', VARCHAR(length=1000)),
    Column('user_id', INTEGER),
    Column('perpetrator_id', INTEGER),
)

likers = Table('likers', post_meta,
    Column('liker_id', Integer),
    Column('liked_article_id', Integer),
    Column('created', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['comment'].drop()
    pre_meta.tables['perpetrator'].drop()
    pre_meta.tables['photo'].drop()
    post_meta.tables['likers'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['comment'].create()
    pre_meta.tables['perpetrator'].create()
    pre_meta.tables['photo'].create()
    post_meta.tables['likers'].drop()

from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
comment = Table('comment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=255)),
    Column('text', Text),
    Column('date', DateTime),
    Column('post_id', Integer),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=255)),
    Column('text', Text),
    Column('publish_date', DateTime),
    Column('user_id', Integer),
)

post_tags = Table('post_tags', post_meta,
    Column('post_id', Integer),
    Column('tag_id', Integer),
)

tag = Table('tag', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=255)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=255)),
    Column('password', String(length=255)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comment'].create()
    post_meta.tables['post'].create()
    post_meta.tables['post_tags'].create()
    post_meta.tables['tag'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comment'].drop()
    post_meta.tables['post'].drop()
    post_meta.tables['post_tags'].drop()
    post_meta.tables['tag'].drop()
    post_meta.tables['user'].drop()

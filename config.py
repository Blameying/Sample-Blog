import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


CSRF_ENABLED  = True
SECRET_KEY = "\x1a\xaf\xe4\xe8\x81536\xd4m\x8a\xd4GeK\xf3\x8f\xda[\xdc\x95\xd2rV"
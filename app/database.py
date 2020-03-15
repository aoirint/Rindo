import os
from sqlalchemy import *
from sqlalchemy.orm import *
from common import *

def asint(val):
    try: return int(val)
    except: return None

DATABASE_HOST = os.environ.get('APP_DATABASE_HOST')
DATABASE_PORT = asint(os.environ.get('APP_DATABASE_PORT'))
DATABASE_NAME = os.environ.get('APP_DATABASE_NAME')
DATABASE_USER = os.environ.get('APP_DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('APP_DATABASE_PASSWORD')
DATABASE_CHARSET = os.environ.get('APP_DATABASE_CHARSET')

DATABASE_URL = 'mysql://%s:%s@%s:%d/%s?charset=%s' % (
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
    DATABASE_CHARSET,
)
DATABASE_URL = 'sqlite:///db.sqlite3'

ENGINE = create_engine(
    DATABASE_URL,
    echo=True,
)
Session = sessionmaker(bind=ENGINE)

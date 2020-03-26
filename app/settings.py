import os
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from passlib.apache import HtpasswdFile

def asint(val):
    try: return int(val)
    except: return None

DEBUG = os.environ.get('APP_DEBUG') == '1'
SECRET_KEY = os.environ['SECRET_KEY']

HTPASSWD_PATH = '.htpasswd'
HTPASSWD = HtpasswdFile(HTPASSWD_PATH)

DATABASE_URL = os.environ.get('APP_DATABASE_URL', 'sqlite:///db.sqlite3')

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_recycle=3600, # https://blog.amedama.jp/entry/2015/08/15/133322
)
Session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        bind=engine,
    )
)

BaseModel = declarative_base()
BaseModel.query = Session.query_property()

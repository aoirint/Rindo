import os
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

def asint(val):
    try: return int(val)
    except: return None

DEBUG = os.environ.get('APP_DEBUG') == '1'

DATABASE_URL = os.environ.get('APP_DATABASE_URL', 'sqlite:///db.sqlite3')

engine = create_engine(
    DATABASE_URL,
    echo=True,
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

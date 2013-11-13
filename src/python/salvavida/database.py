import config

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

config = config.Config().cfg
DATABASE_URI = config.get('db', 'uri')
engine = create_engine(DATABASE_URI, convert_unicode=True, pool_size=10)
Base = declarative_base()

def get_session():
    return  scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))

def init_db():
    import svmodels
    db_session = get_session()
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    

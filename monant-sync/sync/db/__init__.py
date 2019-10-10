from db.entities import Base
from db.entities import Article
from db.entities import Source
from db.entities import Media

_engine = None
_session_conf = None


def setup_db_engine(uri):
    global _engine

    from sqlalchemy import create_engine
    _engine = create_engine(uri)

    return _engine


def create_all_tables():
    Base.metadata.create_all(_engine)


def get_session():
    global _session_conf

    from sqlalchemy.orm import sessionmaker
    if _session_conf is None:
        _session_conf = sessionmaker()
        _session_conf.configure(bind=_engine)

    return _session_conf()

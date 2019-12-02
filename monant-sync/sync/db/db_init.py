from db import Base
from contextlib import contextmanager
import sys

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


@contextmanager
def session_scope():
    session = get_session()
    try:
        yield session
        session.commit()
        print('commited', file=sys.stderr)
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_engine():
    return _engine
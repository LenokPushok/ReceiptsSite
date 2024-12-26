from contextlib import contextmanager

from api.orm.base import session_factory


@contextmanager
def get_session():
    session = session_factory()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

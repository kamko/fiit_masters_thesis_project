from db import session_scope
from db import Article
from .mapper import map_engagement


def _get_urls(session, last_id, max_count):
    urls = session.query(Article.url) \
        .filter(Article.id > last_id) \
        .limit(max_count) \
        .all()

    return [i[0] for i in urls]


def find_last_id_with_engagement():
    with session_scope() as session:
        id = session.query(Article.id) \
            .join(Article.fb_engagement) \
            .order_by(Article.id.desc()) \
            .limit(1) \
            .scalar()

    if id is None:
        return 0

    return id


def get_engagement(fb_client, last_id, max_count):
    with session_scope() as session:
        urls = _get_urls(session, last_id, max_count)
        if len(urls) == 0:
            return

        engagements = fb_client.get_engagement(urls=urls)
        for e in engagements:
            session.add(map_engagement(e))

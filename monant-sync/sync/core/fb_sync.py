from db import session_scope
from db import Article
from .mapper import map_engagement


def _get_urls(session, last_id, max_count):
    urls = session.query(Article.id, Article.url) \
        .filter(Article.id > last_id) \
        .order_by(Article.id.asc()) \
        .limit(max_count) \
        .all()

    return urls


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


def sync_engagement(fb_client, last_id, max_count):
    with session_scope() as session:
        for i in range(0, max_count, 50):
            urls = _get_urls(session, last_id, 50)

            if len(urls) == 0:
                return

            engagements, next_req = fb_client.get_objects(urls=[u[1] for u in urls],
                                                          fields='engagement')

            for e in engagements:
                session.add(map_engagement(e))

            if len(urls) < 50:
                return

            if i % 1000 == 0:
                session.flush()

            last_id = urls[-1][0]

            print(next_req)
            if next_req == False:
                print('[fb] interrupting next request due to API rate limits!')
                return

from datetime import datetime

from .monant_sync import new_articles_iterator, sources_iterator
from .mapper import map_article, map_engagement, map_source
from db import run_action
from db import session_scope
from db import MonitoredArticle, MonitorJobRunLog
from util import flatten_iterable, chunks

from sqlalchemy import func


def _should_fetch_new_articles(session):    
    total_monitored = session.query(func.count(MonitoredArticle.id)) \
        .scalar()

    print(total_monitored)
    return total_monitored < 3500


def _refresh_sources_list(session, monant_client):
    print(f'[_refresh_sources_list - {datetime.now()}]')
    for source in map(map_source, flatten_iterable(sources_iterator(monant_client))):
        session.merge(source)


def _fetch_new_articles(session, monant_client):
    print(f'[_fetch_new_articles - {datetime.now()}]')
    last_id = run_action('last-id') + 1  # todo: bug
    it = flatten_iterable(new_articles_iterator(monant_client, last_id, 500))

    res = []
    for api_article in it:
        article = map_article(api_article)
        session.add(article)
        res.append(article)

    return res


def _mark_articles_as_monitored(session, articles):
    print(f'[_mark_articles_as_monitored - {datetime.now()}]')
    for article in articles:
        monitored_article = MonitoredArticle(article)
        session.add(monitored_article)
    session.flush()


def _fetch_engagement_for_monitored_articles(session, fb_client):
    print(f'[_fetch_engagement_for_monitored_articles - {datetime.now()}]')
    mas = session.query(MonitoredArticle) \
        .order_by(MonitoredArticle.article_id.asc()) \
        .all()

    urls = [m.article.url for m in mas]

    total = 0
    for chunk in chunks(urls, 50):
        engagements, next_req = fb_client.get_objects(
            urls=chunk, fields='engagement')

        for e in engagements:
            session.add(map_engagement(e))

        total += len(chunk)

        if next_req == False:
            print('[fb] interrupting next request due to API rate limits!')
            return

    return total


def run(monant_client, fb_client_provider):
    with session_scope() as session:
        start_time = datetime.now()
        print(f'[monitor] started at {start_time}')

        if _should_fetch_new_articles(session):
            _refresh_sources_list(session, monant_client)
            articles = _fetch_new_articles(session, monant_client)
            _mark_articles_as_monitored(session, articles)
        total = _fetch_engagement_for_monitored_articles(
            session, fb_client=fb_client_provider())

        end_time = datetime.now()
        print(f'[monitor] finished at {end_time}')
        session.add(MonitorJobRunLog(start_time, end_time, total))

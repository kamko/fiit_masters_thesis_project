import datetime as dt
from sqlalchemy import func

from db import MonitoredArticle, MonitorJobRunLog
from db import run_action
from db import session_scope, merge_if_not_none
from util import flatten_iterable, chunks
from .mapper import map_article, map_engagement, map_source
from .monant_sync import new_articles_iterator, sources_iterator

date_threshold = dt.datetime(
    2019, 10, 21, 0, 0, 0, 0, tzinfo=dt.timezone(dt.timedelta(seconds=3600)))


def _should_fetch_new_articles(session):
    total_monitored = session.query(func.count(MonitoredArticle.id)) \
        .scalar()

    return total_monitored < 10000


def _refresh_sources_list(session, monant_client):
    print(f'[_refresh_sources_list - {dt.datetime.now()}]')
    for source in map(map_source, flatten_iterable(sources_iterator(monant_client))):
        session.merge(source)


def _fetch_new_articles(session, monant_client):
    print(f'[_fetch_new_articles - {dt.datetime.now()}]')
    last_id = run_action('last-id')
    it = flatten_iterable(new_articles_iterator(monant_client, last_id, 5000))

    res = []
    for i, api_article in enumerate(it):
        print(i)
        article = map_article(api_article)

        article.source = merge_if_not_none(session, article.source)
        article.author = merge_if_not_none(session, article.author)
        session.add(article)

        if article.published_at is not None and dt.datetime.strptime(article.published_at,
                                                                     '%Y-%m-%dT%H:%M:%S.%f%z') > date_threshold:
            res.append(article)

    return res


def _mark_articles_as_monitored(session, articles):
    print(f'[_mark_articles_as_monitored - {dt.datetime.now()}]')
    for article in articles:
        monitored_article = MonitoredArticle(article)
        session.add(monitored_article)
    session.flush()


def _fetch_engagement_for_monitored_articles(session, fb_client):
    print(f'[_fetch_engagement_for_monitored_articles - {dt.datetime.now()}]')
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
            return total

    return total


def run(monant_client_provider, fb_client_provider):
    with session_scope() as session:
        start_time = dt.datetime.now()
        print(f'[monitor] started at {start_time}')

        try:
            monant_client = monant_client_provider()
            _refresh_sources_list(session, monant_client)
            articles = _fetch_new_articles(session, monant_client)
            _mark_articles_as_monitored(session, articles)
        except ConnectionError as err:
            print(f'[monitor] - monant fetch failed! reason={err}')
        total = _fetch_engagement_for_monitored_articles(
            session, fb_client=fb_client_provider())

        end_time = dt.datetime.now()
        print(f'[monitor] finished at {end_time}')
        session.add(MonitorJobRunLog(start_time, end_time, total))

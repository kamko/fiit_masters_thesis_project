import os
from .mapper import map_source, map_article, map_media
from db import get_session
from util import flatten_iterable, sleeping_iterable


@sleeping_iterable(min=0.1, max=3)
def articles_iterator(api_client, start_from=1, until=None, size=100):
    return api_client.get_paginated(
        url='v1/articles',
        content_key="articles",
        start_from=start_from,
        until=until,
        size=size
    )


def sources_iterator(api_client):
    yield api_client.get(url='v1/sources', content_key='sources')


def map_and_save(iterable, mapper, flatten=True):
    session = get_session()

    if flatten:
        iterable = flatten_iterable(iterable)

    for i, j in enumerate(iterable):
        print(f'[map_and_save] item {i+1} of unknown')

        m = mapper(j)
        session.add(m)

        if i % 2500 == 0:
            session.flush()

    session.commit()


def fetch_sources(api_client):
    map_and_save(sources_iterator(api_client), map_source)


def fetch_articles(api_client):
    map_and_save(articles_iterator(api_client=api_client,
                                   start_from=1, until=None, size=100), map_article)


def fetch_all_data(api_client):
    fetch_sources(api_client)
    fetch_articles(api_client)


def fetch(api_client, entity):
    choices = {
        'all': fetch_all_data,
        'source': fetch_sources,
        'article': fetch_articles
    }

    choices[entity](api_client)

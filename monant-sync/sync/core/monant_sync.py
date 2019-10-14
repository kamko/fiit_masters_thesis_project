import os
from .mapper import map_source, map_article, map_media
from db import session_scope
from util import flatten_iterable, sleeping_iterable


@sleeping_iterable(min=0.1, max=3)
def articles_iterator(api_client, start_from=1, until=None, size=100):
    return api_client.get_paginated(
        url='v1/articles',
        content_key='articles',
        start_from=start_from,
        until=until,
        size=size
    )


@sleeping_iterable(min=0.1, max=3)
def new_articles_iterator(api_client, last_id, max_count, size=100):
    return api_client.get_newest(
        url='v1/articles',
        content_key='articles',
        last_id=last_id,
        max_count=max_count,
        size=size
    )


def sources_iterator(api_client):
    yield api_client.get(url='v1/sources', content_key='sources')


def map_and_save(iterable, mapper, flatten=True):
    with session_scope() as session:
        if flatten:
            iterable = flatten_iterable(iterable)

        for i, j in enumerate(iterable):
            print(f'[map_and_save] item {i+1} of unknown')

            m = mapper(j)
            session.add(m)

            if i % 2500 == 0:
                session.flush()


def fetch_all_sources(api_client):
    map_and_save(sources_iterator(api_client), map_source)


def fetch_all_articles(api_client):
    map_and_save(new_articles_iterator(api_client=api_client,
                                       last_id=0, max_count=9999999), map_article)


def fetch_all_entities(api_client):
    fetch_all_sources(api_client)
    fetch_all_articles(api_client)


def fetch_all(api_client, entity):
    choices = {
        'all': fetch_all_entities,
        'source': fetch_all_sources,
        'article': fetch_all_articles
    }

    choices[entity](api_client)


def fetch_new_articles(api_client, last_id, max_count):
    map_and_save(new_articles_iterator(api_client=api_client,
                                       last_id=last_id, max_count=max_count), map_article)


def fetch_new(api_client, entity, last_id, max_count):
    choices = {
        'article': fetch_new_articles
    }

    choices[entity](api_client, last_id, max_count)

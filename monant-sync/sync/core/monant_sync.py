import os
from .mapper import map_source, map_article, map_media
from db import session_scope, Source, merge_if_not_none
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


def map_and_save(iterable, mapper, flatten=True, merge=True, hook_before_save=None):
    with session_scope() as session:
        with session.no_autoflush:
            if flatten:
                iterable = flatten_iterable(iterable)

            for i, j in enumerate(iterable):
                print(f'[map_and_save] item {i+1} of unknown')

                m = mapper(j)

                if hook_before_save is not None:
                    m = hook_before_save(session, m)

                if merge:
                    session.merge(m)
                else:
                    session.add(m)

                if i % 2500 == 0:
                    session.flush()


def fetch_all_sources(api_client):
    with session_scope() as session:
        for source in map(map_source, flatten_iterable(sources_iterator(api_client))):
            session.merge(source)


def fetch_source_reliability(api_client):

    iterable = api_client.get_paginated(
        url='v1/entity-annotations',
        content_key='entity_annotations',
        size=100,
        extra_params={
            'annotation_category': 'label',
            'annotation_type': 'Source reliability (binary)',
            'method': 'Expert-based source reliability evaluation'
        }
    )

    iterable = flatten_iterable(iterable)

    maping = {
        'reliable': True,
        'unreliable': False
    }

    with session_scope() as session:
        for i in iterable:
            source_id = i['entity_id']
            value = i['value']['value']

            source = session.query(Source) \
                .filter(Source.id == source_id) \
                .one()

            source.is_reliable = maping[value]

            session.merge(source)


def fetch_all_articles(api_client):
    def hook(session, article):
        article.source = merge_if_not_none(session, article.source)
        article.author = merge_if_not_none(session, article.author)

        return article

    map_and_save(new_articles_iterator(api_client=api_client,
                                       last_id=0, max_count=999999999), map_article,
                 hook_before_save=hook)


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

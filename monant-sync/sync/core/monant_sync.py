import os
from .mapper import map_source, map_article, map_media, map_author
from db import session_scope, Source, merge_if_not_none, get_engine
from util import flatten_iterable, sleeping_iterable


@sleeping_iterable(min=0.1, max=2)
def articles_iterator(api_client, start_from=1, until=None, size=100):
    return api_client.get_paginated(
        url='v1/articles',
        content_key='articles',
        start_from=start_from,
        until=until,
        size=size
    )


@sleeping_iterable(min=0.1, max=2)
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


def map_and_save(iterable, mapper, merge=True):
    for i, batch in enumerate(iterable):
        print(f'[map_and_save] batch (size={len(batch)}) {i+1} of unknown')
        _save_all((mapper(item) for item in batch), merge)


def _save_all(batch, merge):
    with session_scope() as session:
        with session.no_autoflush:
            for item in batch:
                if merge:
                    session.merge(item)
                else:
                    session.add(item)


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
    from sqlalchemy.dialects.postgresql import insert
    from db import Author, Source

    iter = new_articles_iterator(api_client=api_client,
                                 last_id=0, max_count=999999999)

    for i, batch in enumerate(iter):
        print(f'batch_no={i}')
        batch = [map_article(a) for a in batch]
        with get_engine().begin() as engine:
            engine.execute(insert(Source).on_conflict_do_nothing(),
                           [art.source.__dict__ for art in batch if art.source is not None])
            engine.execute(insert(Author).on_conflict_do_nothing(),
                           [art.author.__dict__ for art in batch if art.author is not None])
        
        _save_all(batch, merge=True)


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

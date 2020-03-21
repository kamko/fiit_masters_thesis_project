from sqlalchemy.dialects.postgresql import insert

from db import session_scope, get_engine, Source
from db.entities import ArticleVeracity
from util import flatten_iterable, sleeping_iterable
from .mapper import map_source, map_article


@sleeping_iterable(min=0.1, max=2)
def new_articles_iterator(api_client, last_id, max_count, size=100):
    return api_client.get_newest(
        url='v1/articles',
        content_key='articles',
        last_id=last_id,
        max_count=max_count,
        size=size
    )


def annotations_iterable(api_client,
                         annotation_type,
                         annotation_category,
                         method=None,
                         size=100, flatten=True,
                         extractor=None):
    params = {
        'annotation_category': annotation_category,
        'annotation_type': annotation_type,
        'method': method
    }

    res = api_client.get_newest(
        url='v1/entity-annotations',
        content_key='entity_annotations',
        last_id=0,
        size=size,
        extra_params={k: v for k, v in params.items() if v is not None},
        max_count=9999999999
    )

    if flatten:
        res = flatten_iterable(res)

    if flatten and extractor is not None:
        res = map(extractor, res)
    elif not flatten and extractor is not None:
        res = (map(extractor, i) for i in res)
    return res


def sources_iterator(api_client):
    yield api_client.get(url='v1/sources', content_key='sources')


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
    def extractor(item):
        mapping = {
            'reliable': True,
            'unreliable': False
        }

        i_id = item['entity_id']
        i_val = item['value']['value']

        return i_id, mapping[i_val]

    iterable = annotations_iterable(api_client,
                                    annotation_category='label',
                                    annotation_type='Source reliability (binary)',
                                    method='Expert-based source reliability evaluation',
                                    extractor=extractor)

    with session_scope() as session:
        for i in iterable:
            source_id, value = i

            source = session.query(Source) \
                .filter(Source.id == source_id) \
                .one()

            source.is_reliable = value

            session.merge(source)


def fetch_article_veracity(api_client):
    def extractor(item):
        article_id = item['entity_id']
        claims = item['value']['claims']
        veracity = item['value']['value']

        return ArticleVeracity(
            article_id=article_id,
            veracity=veracity,
            claims=claims
        )

    iterable = annotations_iterable(api_client,
                                    annotation_category='prediction',
                                    annotation_type='Article veracity',
                                    extractor=extractor, flatten=False)

    for i, batch in enumerate(iterable):
        print(f'[article-veracity] batch #{i}')
        with get_engine().begin() as engine:
            engine.execute(insert(ArticleVeracity), [av.__dict__ for av in batch])


def fetch_all_articles(api_client):
    fetch_new_articles(api_client=api_client, last_id=0, max_count=999999999)


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
    from db import Author, Source

    iter = new_articles_iterator(api_client=api_client,
                                 last_id=last_id, max_count=max_count)

    for i, batch in enumerate(iter):
        print(f'batch_no={i}')
        batch = [map_article(a) for a in batch]
        with get_engine().begin() as engine:
            s_insert = insert(Source)
            s_insert = s_insert.on_conflict_do_update(index_elements=['id'], set_={
                'name': s_insert.excluded.name,
                'url': s_insert.excluded.url,
                'stype': s_insert.excluded.stype,
                'is_reliable': s_insert.excluded.is_reliable})
            engine.execute(
                s_insert, [art.source.__dict__ for art in batch if art.source is not None])

            a_insert = insert(Author)
            a_insert = a_insert.on_conflict_do_update(index_elements=['id'], set_={
                'name': a_insert.excluded.name,
                'source_id': a_insert.excluded.source_id})
            engine.execute(
                a_insert, [art.author.__dict__ for art in batch if art.author is not None])

        _save_all(batch, merge=True)


def fetch_new(api_client, entity, last_id, max_count):
    choices = {
        'article': fetch_new_articles
    }

    choices[entity](api_client, last_id, max_count)

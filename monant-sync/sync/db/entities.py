import datetime

from sqlalchemy.dialects.postgresql import JSONB, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import Text, BigInteger, DateTime, Integer, Boolean

Base = declarative_base()

media_article_table = Table('article_media',
                            Base.metadata,
                            Column('article_id', BigInteger,
                                   ForeignKey('article.id')),
                            Column('media_id', BigInteger,
                                   ForeignKey('media.id')))


class Article(Base):
    __tablename__ = 'article'

    id = Column(BigInteger, primary_key=True)

    url = Column(Text, unique=True)
    title = Column(Text)
    perex = Column(Text)
    body = Column(Text)
    raw_body = Column(Text)
    published_at = Column(DateTime)
    extracted_at = Column(DateTime)

    source_id = Column(BigInteger, ForeignKey('source.id'))
    source = relationship("Source", uselist=False)

    author_id = Column(BigInteger, ForeignKey('author.id'))
    author = relationship("Author", uselist=False, cascade='save-update, merge')

    media = relationship(
        'Media', secondary=media_article_table, cascade='save-update, merge')

    fb_engagement = relationship('FacebookEngagement', uselist=False)

    category = Column(JSONB)
    other_info = Column(JSONB)
    veracity = Column(Text)

    monitor_name = Column(Text)
    monitor_id = Column(BigInteger)

    def __init__(self, id, author, title, perex, body, raw_body, published_at, extracted_at,
                 url, source_id, media, category, other_info, veracity, monitor_name, monitor_id):
        self.id = id
        self.author = author
        self.title = title
        self.perex = perex
        self.body = body
        self.raw_body = raw_body
        self.published_at = published_at
        self.extracted_at = extracted_at
        self.url = url
        self.source_id = source_id
        self.media = media
        self.category = category
        self.other_info = other_info
        self.veracity = veracity
        self.monitor_id = monitor_id
        self.monitor_name = monitor_name


class Author(Base):
    __tablename__ = 'author'

    id = Column(BigInteger, primary_key=True)

    name = Column(Text)

    source_id = Column(BigInteger, ForeignKey('source.id'))

    def __init__(self, id, name, source_id):
        self.id = id
        self.name = name
        self.source_id = source_id

    @staticmethod
    def upsert_query(index_elements=None):
        if index_elements is None:
            index_elements = ['id']

        odo_insert = insert(Author)
        return odo_insert.on_conflict_do_update(index_elements=index_elements, set_={
            'name': odo_insert.excluded.name,
            'source_id': odo_insert.excluded.source_id})


class Source(Base):
    __tablename__ = 'source'

    id = Column(BigInteger, primary_key=True)

    name = Column(Text)
    url = Column(Text)
    stype = Column(Text)
    is_reliable = Column(Boolean)

    veracity = Column(Text)

    def __init__(self, id, name, url, stype, veracity):
        self.id = id
        self.name = name
        self.url = url,
        self.stype = stype
        self.veracity = veracity

    @staticmethod
    def upsert_query(index_elements=None):
        if index_elements is None:
            index_elements = ['id']

        odo_insert = insert(Source)
        return odo_insert.on_conflict_do_update(index_elements=index_elements, set_={
            'name': odo_insert.excluded.name,
            'url': odo_insert.excluded.url,
            'stype': odo_insert.excluded.stype,
            'is_reliable': odo_insert.excluded.is_reliable})


class Media(Base):
    __tablename__ = 'media'

    id = Column(BigInteger, primary_key=True)

    article_id = Column(BigInteger)
    url = Column(Text)
    caption = Column(Text)
    media_type = Column(Text)

    def __init__(self, id, article_id, caption, media_type, url):
        self.id = id
        self.article_id = article_id
        self.caption = caption
        self.media_type = media_type,
        self.url = url


class FacebookEngagement(Base):
    __tablename__ = 'article_fb_engagement'

    id = Column(BigInteger, primary_key=True)

    url = Column(Text, ForeignKey('article.url'))

    reaction_count = Column(Integer)
    comment_count = Column(Integer)
    share_count = Column(Integer)
    comment_plugin_count = Column(Integer)

    sync_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, url, reaction_count, comment_count, share_count, comment_plugin_count):
        self.url = url
        self.reaction_count = reaction_count
        self.comment_count = comment_count
        self.share_count = share_count
        self.comment_plugin_count = comment_plugin_count


class MonitoredArticle(Base):
    __tablename__ = "monitored_article"

    id = Column(BigInteger, primary_key=True)

    article_id = Column(BigInteger, ForeignKey('article.id'))
    article = relationship("Article")

    def __init__(self, article):
        self.article = article


class MonitorJobRunLog(Base):
    __tablename__ = "monitor_job_run_log"

    id = Column(BigInteger, primary_key=True)

    run_started = Column(DateTime)
    run_finished = Column(DateTime)

    articles_processed = Column(Integer)

    def __init__(self, run_started, run_finished, articles_processed):
        self.run_started = run_started
        self.run_finished = run_finished
        self.articles_processed = articles_processed


class ArticleVeracity(Base):
    __tablename__ = "article_veracity"

    article_id = Column(BigInteger, ForeignKey('article.id'), primary_key=True)

    veracity = Column(Text)

    claims_false = Column(Integer)
    claims_mixture = Column(Integer)
    claims_mostly_false = Column(Integer)
    claims_mostly_true = Column(Integer)
    claims_true = Column(Integer)
    claims_unknown = Column(Integer)

    def __init__(self, article_id, veracity, claims):
        self.article_id = article_id

        self.veracity = veracity

        self.claims_false = claims['false']
        self.claims_mixture = claims['mixture']
        self.claims_mostly_false = claims['mostly-false']
        self.claims_mostly_true = claims['mostly-true']
        self.claims_true = claims['true']
        self.claims_unknown = claims['unknown']

    @staticmethod
    def upsert_query(index_elements=None):
        if index_elements is None:
            index_elements = ['article_id']

        odo_insert = insert(ArticleVeracity)
        return odo_insert.on_conflict_do_update(index_elements=index_elements, set_={
            'article_id': odo_insert.excluded.article_id,
            'veracity': odo_insert.excluded.veracity,
            'claims_false': odo_insert.excluded.claims_false,
            'claims_mixture': odo_insert.excluded.claims_mixture,
            'claims_mostly_false': odo_insert.excluded.claims_mostly_false,
            'claims_mostly_true': odo_insert.excluded.claims_mostly_true,
            'claims_true': odo_insert.excluded.claims_true,
            'claims_unknown': odo_insert.excluded.claims_unknown,
        })

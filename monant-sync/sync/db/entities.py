import datetime

from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import Text, BigInteger, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

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
    published_at = Column(DateTime)
    extracted_at = Column(DateTime)

    source_id = Column(BigInteger, ForeignKey('source.id'))
    source = relationship("Source", uselist=False)

    author_id = Column(BigInteger, ForeignKey('author.id'))
    author = relationship("Author", uselist=False, cascade='save-update')

    media = relationship(
        'Media', secondary=media_article_table, cascade='save-update)

    fb_engagement = relationship('FacebookEngagement', uselist=False)

    category = Column(Text)

    other_info = Column(JSONB)

    def __init__(self, id, author, title, perex, body, published_at, extracted_at,
                 url, source, media, category, other_info):
        self.id = id
        self.author = author
        self.title = title
        self.perex = perex
        self.body = body
        self.published_at = published_at
        self.extracted_at = extracted_at
        self.url = url
        self.source_id = source.id
        self.media = media
        self.category = category
        self.other_info = other_info


class Author(Base):
    __tablename__ = 'author'

    id = Column(BigInteger, primary_key=True)

    name = Column(Text)

    source_id = Column(BigInteger, ForeignKey('source.id'))

    def __init__(self, id, name, source_id):
        self.id = id
        self.name = name
        self.source_id = source_id


class Source(Base):
    __tablename__ = 'source'

    id = Column(BigInteger, primary_key=True)

    name = Column(Text)
    url = Column(Text)
    stype = Column(Text)
    is_reliable = Column(Boolean)

    def __init__(self, id, name, url, stype):
        self.id = id
        self.name = name
        self.url = url,
        self.stype = stype


class Media(Base):
    __tablename__ = 'media'

    id = Column(BigInteger, primary_key=True)

    url = Column(Text)
    caption = Column(Text)
    media_type = Column(Text)

    def __init__(self, id, caption, media_type, url):
        self.id = id
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

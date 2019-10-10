from sqlalchemy import create_engine
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import Text, BigInteger, DateTime
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

    title = Column(Text)
    perex = Column(Text)
    body = Column(Text)
    published_at = Column(DateTime)
    url = Column(Text)

    source_id = Column(BigInteger)
    source = relationship("Source", uselist=False)

    media = relationship("Media", secondary=media_article_table)

    category = Column(Text)

    other_info = Column(JSONB)


class Source(Base):
    __tablename__ = 'source'

    id = Column(BigInteger, primary_key=True)

    name = Column(Text)
    url = Column(Text)


class Media(Base):
    __tablename__ = 'media'

    id = Column(BigInteger, primary_key=True)

    caption = Column(Text)
    media_type = Column(Text)
    url = Column(Text)


def engine():
    from os import environ
    return create_engine(os.environ['POSTGRESQL_URI'])


def create_all_tables(engine):
    Base.metadata.create_all(engine)

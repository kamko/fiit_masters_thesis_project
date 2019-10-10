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

    source_id = Column(BigInteger, ForeignKey('source.id'))
    source = relationship("Source", uselist=False, cascade='save-update')

    media = relationship(
        "Media", secondary=media_article_table, cascade='save-update')

    category = Column(Text)

    other_info = Column(JSONB)


class Source(Base):
    __tablename__ = 'source'

    id = Column(BigInteger, primary_key=True)

    name = Column(Text)
    url = Column(Text)
    stype = Column(Text)

    def __init__(self, id, name, url, stype):
        self.id = id
        self.name = name
        self.url = url,
        self.stype = stype


class Media(Base):
    __tablename__ = 'media'

    id = Column(BigInteger, primary_key=True)

    caption = Column(Text)
    media_type = Column(Text)
    url = Column(Text)

    def __init__(self, id, caption, media_type, url):
        self.id = id
        self.caption = caption
        self.media_type = media_type,
        self.url = url

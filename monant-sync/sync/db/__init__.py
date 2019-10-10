from entities import Article
from entities import Source
from entities import Media


def create_all_tables(engine):
    Base.metadata.create_all(engine)

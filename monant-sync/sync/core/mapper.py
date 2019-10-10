from db import Article, Source, Media


def map_article(article):
    pass


def map_source(source):
    return Source(
        id=source['id'],
        name=source['name'],
        url=source['url'],
        stype=source.get('source_type', {}).get('name', None)
    )


def map_media(media):
    return Media(
        id=media['id'],
        caption=media['caption'],
        media_type=media.get('media_type', {}).get('name', None),
        url=media['url']
    )

from db import Article, Source, Media


def map_article(article):
    return Article(
        id = article['id'],
        title = article['title'],
        perex=article['perex'],
        body=article['body'],
        published_at=article['published_at'],
        url=article['url'],
        source=map_source(article['source']),
        media=list(map(map_media, article['media'])),
        category=article['category'],
        other_info=article['other_info']
    )


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

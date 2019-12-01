from db import Article, Author, Source, Media, FacebookEngagement


def map_article(article):
    source = map_source(article['source'])
    return Article(
        id=article['id'],
        author=map_author(article['author'], source),
        title=article['title'],
        perex=article['perex'],
        body=article['body'],
        published_at=article['published_at'],
        extracted_at=article['extracted_at'],
        url=article['url'],
        source=source,
        media=list(map(map_media, article['media'])),
        category=article['category'],
        other_info=article['other_info']
    )


def map_author(author, source):
    return Author(
        id=author['id'],
        name=author['name'],
        source=source
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


def map_engagement(engagement):
    ne = engagement['engagement']
    return FacebookEngagement(
        url=engagement['id'],
        reaction_count=ne['reaction_count'],
        comment_count=ne['comment_count'],
        share_count=ne['share_count'],
        comment_plugin_count=ne['comment_plugin_count'],
    )

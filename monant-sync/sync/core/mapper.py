from db import Article, Author, Source, Media, FacebookEngagement


def map_article(article):
    source = map_source(article['source'])
    return Article(
        id=article['id'],
        author=map_author(article['author'], source),
        title=article['title'],
        perex=article['perex'],
        body=article['body'],
        raw_body=article['raw_body'],
        published_at=article['published_at'],
        extracted_at=article['extracted_at'],
        url=article['url'],
        source_id=source.id,
        media=[map_media(article['id'], m) for m in article['media']],
        category=article['category'],
        other_info=article['other_info'],
        veracity=article['veracity']
    )


def map_author(author, source):
    if author is None:
        return None

    return Author(
        id=author['id'],
        name=author['name'],
        source_id=source.id
    )


def map_source(source):
    return Source(
        id=source['id'],
        name=source['name'],
        url=source['url'],
        stype=source.get('source_type', {}).get('name', None),
        veracity=source['veracity']
    )


def map_media(aid, media):
    return Media(
        id=media['id'],
        article_id=aid,
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

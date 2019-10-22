from . import session_scope
from . import Article


def get_last_article_id():

    with session_scope() as session:
        article = session \
            .query(Article) \
            .order_by(Article.id.desc()) \
            .first()
        return article.id


def run_action(action):
    choices = {
        'last-id': get_last_article_id
    }

    return choices[action]()

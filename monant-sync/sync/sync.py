import os
from api.client import client
from db.mapper import *
from util import foreach


def articles_iterator(api_client, start_from=1, until=None, size=100):
    return api_client.get_paginated(
        url='v1/articles',
        content_key="articles",
        start_from=start_from,
        until=until,
        size=size
    )


def sources_iterator(api_client):
    yield api_client.get(url='v1/sources', content_key='sources')


def fetch_all_data(api_client):

    # Sources
    foreach(sources_iterator(api_client), map_source)

    # Articles
    foreach(articles_iterator(api_client=api_client,
                              start_from=1, until=None, size=100), map_article)


if __name__ == '__main__':
    api_client = client(username=os.environ['MONANT_AUTH_USERNAME'],
                        password=os.environ['MONANT_AUTH_PASSWORD'])

import os
from api.client import client
from db import save_article
from util import foreach


def articles_iterator(api_client, start_from=1, until=None, size=100):
    return api_client.get_paginated(
        url='https://api.monant.fiit.stuba.sk/v1/articles',
        content_key="articles",
        start_from=start_from,
        until=until,
        size=size
    )


def sync_data(api_client):
    foreach(articles_iterator(api_client=api_client,
                              start_from=1, until=10, size=1), save_article)


if __name__ == '__main__':
    api_client = client(username=os.environ['MONANT_AUTH_USERNAME'],
                        password=os.environ['MONANT_AUTH_PASSWORD'])
    sync_data(api_client)

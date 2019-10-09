import requests as rq
import itertools
from .auth import MonantAuth


class MonantClient:

    def __init__(self, base_url, auth):
        self.auth = auth
        self.base_url = base_url

    def get(self, url, params=None):
        if params is None:
            params = {}

        return rq.get(self.base_url + url, params=params, auth=self.auth).json()

    def post(self, url, json=None):
        if json is None:
            json = {}

        return rq.post(self.base_url + url, json=json, auth=self.auth).json()

    def get_paginated(self, url, content_key, start_from=1, until=None, size=10):
        for i in itertools.count(start_from):
            page = self.get(url, params={
                'page': i,
                'size': size
            })

            yield page[content_key]

            if page['pagination']['has_next'] is False:
                break

            if until is not None and i >= until:
                break


def client(username, password):
    auth = MonantAuth(username=username, password=password)
    return MonantClient(base_url='https://api.monant.fiit.stuba.sk/', auth=auth)

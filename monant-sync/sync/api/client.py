import requests as rq
import itertools
from .auth import MonantAuth


class MonantClient:

    def __init__(self, auth):
        self.auth = auth

    def get(self, url, params=None):
        if params is None:
            params = {}

        return rq.get(url, params=params, auth=self.auth).json()

    def post(self, url, json=None):
        if json is None:
            json = {}

        return rq.post(url, json=json, auth=self.auth).json()

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
    return MonantClient(auth)

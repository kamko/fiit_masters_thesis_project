import itertools
import requests as rq

from .auth import MonantAuth


class ApiClient:

    def __init__(self, base_url, auth):
        self.auth = auth
        self.base_url = base_url

    def get(self, url, content_key=None, params=None):
        if params is None:
            params = {}

        res = rq.get(self.base_url + url, params=params, auth=self.auth).json()

        if content_key is not None:
            return res[content_key]

        return res

    def post(self, url, json=None):
        if json is None:
            json = {}

        return rq.post(self.base_url + url, json=json, auth=self.auth).json()

    def get_paginated(self, url, content_key, start_from=1, until=None, size=10, extra_params=None):
        if extra_params is None:
            extra_params = {}
        for i in itertools.count(start_from):
            page = self.get(url, params={
                'page': i,
                'size': size,
                **extra_params
            })

            yield page[content_key]

            if page['pagination']['has_next'] is False:
                break

            if until is not None and i >= until:
                break

    def get_newest(self, url, content_key, last_id, max_count, size=10, extra_params=None):
        if extra_params is None:
            extra_params = {}

        i = 0
        while i < max_count:
            page = self.get(url, params={
                'last_id': last_id,
                'count': size,
                **extra_params
            })

            content = page[content_key]

            yield content

            i = i + len(content)

            if len(content) < size:
                break

            last_id = content[-1]['id']


def create_client(username, password):
    base_url = 'https://api.monant.fiit.stuba.sk/'

    auth = MonantAuth(base_url, username, password)

    return ApiClient(base_url, auth)

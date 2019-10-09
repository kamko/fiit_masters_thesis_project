import requests as rq
from requests.auth import AuthBase
import itertools


class MonantAuth(AuthBase):

    def __init__(self, username, password):
        self.token = self._get_token(username, password)

    def _get_token(self, username, password):
        res = rq.post('https://api.monant.fiit.stuba.sk/auth',
                      json={
                          'username': username,
                          'password': password
                      })

        json_res = res.json()
        return json_res['access_token']

    def __call__(self, r):
        r.headers['Authorization'] = f'JWT {self.token}'
        return r


class MonantClient:

    def __init__(self, auth):
        self.auth = auth

    def get(self, url, params=None):
        if params is None:
            params = {}

        return rq.get(url, params=params, auth=self.auth)

    def post(self, url, json=None):
        if json is None:
            json = {}

        return rq.post(url, json=json, auth=self.auth)

    def get_paginated(self, url, content_key, start_from=1, until=None, size=10):
        for i in itertools.count(start_from):
            page = self.get(url, params={
                'page': i,
                'size': size
            }).json()

            yield page[content_key]

            if page['pagination']['has_next'] is False:
                break

            if until is not None and i >= until:
                break


def client(username, password):
    auth = MonantAuth(username=username, password=password)
    return MonantClient(auth)

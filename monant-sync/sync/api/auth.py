import requests as rq
from requests.auth import AuthBase


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

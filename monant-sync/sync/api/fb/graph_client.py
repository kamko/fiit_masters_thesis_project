import requests


class FbApiClient:

    def __init__(self, app_id, app_secret):
        self.url = 'https://graph.facebook.com/v4.0/'
        self.token = self._get_token(app_id, app_secret)

    def _get_token(self, app_id, app_secret):
        print('[fb] getting access token')
        res = requests.get('https://graph.facebook.com/oauth/access_token',
                           params={
                               'client_id': app_id,
                               'client_secret': app_secret,
                               'grant_type': 'client_credentials'
                           })
        print('[fb] access token acquired')
        return res.json()['access_token']

    def get_objects(self, urls, fields):
        print(f'[fb] getting engagement for {len(urls)} urls')
        res = requests.get(self.url,
                            params={
                                'ids': ','.join(urls),
                                'fields': fields,
                                'access_token': self.token
                            })
        
        print(f'[debug] {res.headers["x-app-usage"]}')
        return [k for i, k in res.json().items()]


def create_client(app_id, app_secret):
    return FbApiClient(app_id, app_secret)

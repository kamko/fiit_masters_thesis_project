import os
from auth import client

r = client(username=os.environ['MONANT_AUTH_USERNAME'],
           password=os.environ['MONANT_AUTH_PASSWORD'])

for i in r.get_paginated('https://api.monant.fiit.stuba.sk/v1/articles', content_key="articles",start_from=1,until=3,size=1):
    print(i)

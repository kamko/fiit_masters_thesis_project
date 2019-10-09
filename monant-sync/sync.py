import os
from auth import client

r = client(username=os.environ['MONANT_AUTH_USERNAME'],
           password=os.environ['MONANT_AUTH_PASSWORD'])

x = r.get('https://api.monant.fiit.stuba.sk/v1/articles').json()

print(x)

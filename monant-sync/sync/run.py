# cli
import os
from db import create_all_tables, create_engine
from core.sync import fetch_all_data

db_engine = create_engine(uri=os.environ['POSTGRESQL_URI'])
api_client = api_client = client(username=os.environ['MONANT_AUTH_USERNAME'],
                                 password=os.environ['MONANT_AUTH_PASSWORD'])


def init_database():
    print('Creating all tables for given postgresql URI')
    create_all_tables(db_engine)


def fetch_all_data():
    print('[fetch_all_data] Starting downloading of all data')
    fetch_all_data(api_client)
    print('[fetch_all_data] finished')


def sync_new():
    pass

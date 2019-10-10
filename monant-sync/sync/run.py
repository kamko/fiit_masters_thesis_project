# cli
import os
from api.client import create_client
from db import create_all_tables, setup_db_engine
from core.sync import fetch_all_data as sync_fetch

db_engine = setup_db_engine(uri=os.environ['POSTGRESQL_URI'])
api_client = create_client(username=os.environ['MONANT_AUTH_USERNAME'],
                                 password=os.environ['MONANT_AUTH_PASSWORD'])


def init_database():
    print('Creating all tables for given postgresql URI')
    create_all_tables(db_engine)


def fetch_all_data():
    print('[fetch_all_data] Starting downloading of all data')
    sync_fetch(api_client)
    print('[fetch_all_data] finished')


def sync_new():
    pass

fetch_all_data()
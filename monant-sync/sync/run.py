import os
import click
from api.client import create_client
from db import create_all_tables, setup_db_engine
from core.sync import fetch_all_data as sync_fetch

db_engine = setup_db_engine(uri=os.environ['POSTGRESQL_URI'])
api_client = create_client(username=os.environ['MONANT_AUTH_USERNAME'],
                                 password=os.environ['MONANT_AUTH_PASSWORD'])

@click.group()
def cli():
    pass

@click.command()
def init_database():
    print('[init_database] Creating all tables for given postgresql URI')
    create_all_tables()
    print('[init_database] finished')

@click.command()
def fetch_all():
    print('[fetch_all] Starting downloading of all data')
    sync_fetch(api_client)
    print('[fetch_all] finished')


def sync_new():
    pass


cli.add_command(init_database)
cli.add_command(fetch_all)

if __name__ == '__main__':
    cli()
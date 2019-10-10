import os
import click
from api.client import create_client
from db import create_all_tables, setup_db_engine
from core.sync import fetch

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
@click.argument('entity')
def fetch_all(entity):
    print(f'[fetch_all] Starting downloading of all data for entity "{entity}""')
    fetch(api_client, entity)
    print('[fetch_all] finished')


@click.command()
def fetch_new():
    pass


cli.add_command(init_database)
cli.add_command(fetch_all)

if __name__ == '__main__':
    cli()

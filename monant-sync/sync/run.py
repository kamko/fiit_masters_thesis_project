import os
import click
from api.client import create_client
from db import create_all_tables, setup_db_engine
from db import run_action as db_run_action
from core.sync import fetch_all as sync_fetch_all
from core.sync import fetch_new as sync_fetch_new

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
    print(
        f'[fetch_all] Starting downloading of all data for entity "{entity}"')
    sync_fetch_all(api_client, entity)
    print('[fetch_all] finished')


@click.command()
@click.argument('entity')
@click.option('--last-id', required=True, type=int)
@click.option('--max-count', required=True, type=int)
def fetch_new(entity, last_id, max_count):
    print(f'[fetch_new] Starting downloading of all data for entity "{entity}"')
    sync_fetch_new(api_client, entity, last_id, max_count)
    print('[fetch_new] finished')

@click.command()
@click.argument('action')
def articles(action):
    res = db_run_action(action)
    print(f'[Articles action: {action}] = {res}')

cli.add_command(init_database)
cli.add_command(fetch_all)
cli.add_command(fetch_new)
cli.add_command(articles)

if __name__ == '__main__':
    cli()

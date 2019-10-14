import os
import click
from api.client import create_client as monant_create_client
from api.fb.graph_client import create_client as fb_create_client
from db import create_all_tables, setup_db_engine
from db import run_action as db_run_action
from core.monant_sync import fetch_all as sync_fetch_all
from core.monant_sync import fetch_new as sync_fetch_new
from core.fb_sync import sync_engagement as fb_get_engagement, find_last_id_with_engagement

db_engine = setup_db_engine(uri=os.environ['POSTGRESQL_URI'])


def monant_client(): return monant_create_client(username=os.environ['MONANT_AUTH_USERNAME'],
                                                 password=os.environ['MONANT_AUTH_PASSWORD'])


def fb_client(): return fb_create_client(app_id=os.environ['FACEBOOK_APP_ID'],
                                         app_secret=os.environ['FACEBOOK_APP_SECRET'])


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
    sync_fetch_all(monant_client(), entity)
    print('[fetch_all] finished')


@click.command()
@click.argument('entity')
@click.option('--last-id', required=True, type=int)
@click.option('--max-count', required=True, type=int)
def fetch_new(entity, last_id, max_count):
    print(
        f'[fetch_new] Starting downloading of new data for entity "{entity}"')

    if last_id == -1:
        print(f'[fetch_new] last_id set to -1 -> using last id in database')
        last_id = db_run_action('last-id')
        last_id = last_id + 1  # workaround due to bug in API

    sync_fetch_new(monant_client(), entity, last_id, max_count)
    print('[fetch_new] finished')


@click.command()
@click.argument('action')
@click.option('--verbose', default=False, is_flag=True)
def articles(action, verbose):
    res = db_run_action(action)
    if verbose:
        print(f'[Articles action: {action}] = {res}')
    else:
        print(res)


@click.command()
@click.argument('field')
@click.option('--last-id', required=True, type=int)
@click.option('--max-count', required=True, type=int)
def facebook(field, last_id, max_count):
    print(
        f'[facebook] fetch for field={field}, last_id={last_id}, max_count={max_count}')
    if field != 'engagement':
        print('unknown field')
        return
    if last_id == -1:
        print('[facebook] setting to last article id')
        last_id = find_last_id_with_engagement()

    fb_get_engagement(fb_client(), last_id, max_count)


cli.add_command(init_database)
cli.add_command(fetch_all)
cli.add_command(fetch_new)
cli.add_command(articles)
cli.add_command(facebook)

if __name__ == '__main__':
    cli()

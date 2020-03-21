import os

import click
import schedule
import time

from api.client import create_client as monant_create_client
from api.fb.graph_client import create_client as fb_create_client
from core.fb_sync import sync_engagement as fb_get_engagement, find_last_id_with_engagement
from core.monant_sync import fetch_new as sync_fetch_new
from core.monitoring import run as monitor_run
from db import create_all_tables, setup_db_engine
from db import run_action as db_run_action

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
    from core.monant_sync import fetch_all
    print(
        f'[fetch_all] Starting download of all data for entity "{entity}"')
    fetch_all(monant_client(), entity)
    print('[fetch_all] finished')


@click.command()
@click.argument('entity')
@click.option('--last-id', required=True, type=int)
@click.option('--max-count', required=True, type=int)
def fetch_new(entity, last_id, max_count):
    print(
        f'[fetch_new] Starting download of new data for entity "{entity}"')

    if last_id == -1:
        print(f'[fetch_new] last_id set to -1 -> using last id in database')
        last_id = db_run_action('last-id')
        last_id = last_id

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


@click.command()
def monitor():
    print("[monitor] scheduler started!")
    schedule.every(2).hours.do(
        monitor_run, monant_client_provider=monant_client, fb_client_provider=fb_client)

    schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(1)


@click.command()
@click.argument('type')
def annotation(type):
    from core.monant_sync import fetch_source_reliability
    from core.monant_sync import fetch_article_veracity

    print(f'[annotation] fetch annotations for type: {type}')

    if type == 'source-reliability':
        fetch_source_reliability(monant_client())
    elif type == 'article-veracity':
        fetch_article_veracity(monant_client())
    else:
        print(f'[annotation] Unknown-type {type} - ignoring')


cli.add_command(init_database)
cli.add_command(fetch_all)
cli.add_command(fetch_new)
cli.add_command(articles)
cli.add_command(facebook)
cli.add_command(monitor)
cli.add_command(annotation)

if __name__ == '__main__':
    cli()

from contextlib import contextmanager
def create_engine(conf_file, key):
    import json
    from sqlalchemy import create_engine

    with open(conf_file, 'r') as f:
        conf = json.load(f)
        return create_engine(conf[key]['uri'])

    
def display_all(df):
    import pandas as pd
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        display(df)

@contextmanager
def figsize(plt, x, y):
    try:
        plt.rcParams['figure.figsize'] = (x, y)
        yield
    finally:
        plt.rcParams['figure.figsize'] = (6.4, 4.8)

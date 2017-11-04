#!/usr/bin/env python
import os

import click

from app import create_app
from app.domain.errors import EmptyField

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.cli.command()
def init():
    from app import repository

    repository.init(app)
    click.echo('Initialized app! Database engine: {}.'.format(app.config['DB']))


@app.cli.command()
@click.option('--username')
@click.option('--password')
@click.option('--sign', default='')
@click.option('--tip', default='')
def set_admin(username, password, sign, tip):
    from app.domain.usecases import set_admin

    try:
        set_admin(username, password, sign, tip)
    except EmptyField as e:
        click.echo('!!!U should set {missed_field} for admin!'.format(missed_field=e.field))
    else:
        click.echo('Initialized db data.')


if __name__ == '__main__':
    app.run()

#!/usr/bin/env python
import os
import click
from flask_migrate import Migrate

from app import create_app, db
from app.domain.errors import EmptyField

# This is for flask db init
from app.models import AdminModel, HostModel, ServiceModel

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.cli.command()
@click.option('--username')
@click.option('--password')
@click.option('--sign', default='')
@click.option('--tip', default='')
def set_admin(username, password, sign, tip):
    from app.domain.usecases import set_admin
    from app.repos import AdminRepoImpl

    try:
        set_admin(AdminRepoImpl(), username, password, sign, tip)
    except EmptyField as e:
        click.echo('!!!U should set {missed_field} for admin!'.format(missed_field=e.field))
    else:
        click.echo('Initialized db data.')


if __name__ == '__main__':
    app.run()

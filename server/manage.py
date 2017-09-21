#!/usr/bin/env python
from app import create_app, db
from flask_migrate import Migrate
import click

# This is for flask db init
from app.models import AdminModel, HostModel, ServiceModel

app = create_app('dev')
migrate = Migrate(app, db)


@app.cli.command()
@click.option('--username')
@click.option('--password')
@click.option('--sign', default='')
@click.option('--tip', default='')
def set_admin(username, password, sign, tip):
    from app.domain.usecases import set_admin
    from app.repos import AdminRepoImpl

    set_admin(AdminRepoImpl(), username, password, sign, tip)
    click.echo('Initialized db data.')


if __name__ == '__main__':
    app.run(debug=True)

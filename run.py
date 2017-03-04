import click
from flask.helpers import get_debug_flag
from morgenmad.app import create_app
from morgenmad.config import DevConfig, ProdConfig
from morgenmad.extensions import db
from morgenmad.user.model import User
from morgenmad.utils import generate_dates, insert_dates_between_years, users_per_breakfast

import pathlib
import json

CONFIG = DevConfig if get_debug_flag() else ProdConfig
app = create_app(CONFIG)


@app.cli.command()
def initdb():
    db.create_all()


@app.cli.command()
@click.option('-f', '--file', default='seed_users.json', help="Path to users JSON file")
@click.option('-s', '--setup', is_flag=True, help="Setup the database matching dates and users")
def seedusers(file, setup):
    path = pathlib.Path(file)
    if not path.exists():
        raise FileNotFoundError(f"Invalid path to users_json: {str(path)}")
    with path.open(encoding='utf-8') as p:
        users = json.load(p)
    for user in users:
        new_user = User(**user)
        db.session.add(new_user)
        db.session.commit()

    if setup:
        insert_dates_between_years()
        users_per_breakfast()
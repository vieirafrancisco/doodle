import click

from sunflower.db import Database
from sunflower.db.models import models_list

db = Database().db

@click.group()
def database():
    pass

@click.command()
def migration():
    click.echo("Inside DB")

@click.command()
def create_tables():
    db.create_tables(models_list)

database.add_command(migration)
database.add_command(create_tables)

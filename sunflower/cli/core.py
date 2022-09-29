import click

from .db import database
from .api import api

@click.group()
def main():
    pass

main.add_command(database)
main.add_command(api)

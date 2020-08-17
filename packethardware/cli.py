import click
from .inventory import inventory
from .update import update


@click.group()
def cli():
    pass


cli.add_command(inventory)
cli.add_command(update)

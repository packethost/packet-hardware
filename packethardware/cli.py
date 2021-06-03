import click
from .inventory import inventory
from .inventorybios import inventorybios
from .update import update


@click.group()
def cli():
    pass


cli.add_command(inventory)
cli.add_command(inventorybios)
cli.add_command(update)

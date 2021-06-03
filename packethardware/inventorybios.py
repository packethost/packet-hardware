#!/usr/bin/env python3

import click

from . import utils


@click.command()
@click.option("--tinkerbell", "-u", help="Tinkerbell uri", required=True)
@click.option(
    "--verbose",
    "-v",
    default=False,
    help="Turn on verbose messages for debugging",
    is_flag=True,
)
@click.option(
    "--dry",
    "-d",
    default=False,
    help="Don't actually post anything to the database",
    is_flag=True,
)
@click.option(
    "--cache-file",
    "-c",
    default="/tmp/components.jsonpickle",
    help="Path to local json component store",
)
def inventorybios(tinkerbell, verbose, dry, cache_file):
    bios_features = utils.get_bios_features()

    if verbose:
        utils.log(name="biosfeatures", contents=bios_features)

    with open(cache_file, "w") as output:
        output.write(bios_features)

    if not dry:
        print("Writing to the database is not yet implemented")

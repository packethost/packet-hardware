#!/usr/bin/env python3

import click
import jsonpickle

from .component import *


@click.command()
@click.option(
    "--component-type",
    "-t",
    help="Component type(s) to check",
    multiple=True,
    default=[cls.__name__ for cls in vars()["Component"].__subclasses__()],
)
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
    help="Don't actually post anything to API",
    is_flag=True,
)
@click.option(
    "--cache-file",
    "-c",
    default="/tmp/components.jsonpickle",
    help="Path to local json component store",
)
def update(component_type, tinkerbell, verbose, dry, cache_file):
    component_types = [c + "Component" for c in component_type]

    with open(cache_file, "r") as pickle_file:
        components = jsonpickle.decode(pickle_file.read())

    post_components = [c for c in components if c.component_type in component_types]
    if not dry:
        Component.post_all(post_components, tinkerbell)


if __name__ == "__main__":
    update(auto_envvar_prefix="HARDWARE")

#!/usr/bin/env python3

import click
import jsonpickle

from .component import *


@click.command()
@click.option(
    "--component-type",
    "-t",
    help="Component type(s) to update",
    multiple=True,
    default=[cls.__name__ for cls in vars()["Component"].__subclasses__()],
)
@click.option(
    "--verbose",
    "-v",
    default=False,
    help="Turn on verbose messages for debugging",
    is_flag=True,
)
@click.option(
    "--dry", "-d", default=False, help="Don't actually update anything", is_flag=True
)
@click.option(
    "--cache-file",
    "-c",
    default="/tmp/components.jsonpickle",
    help="Path to local json component store",
)
@click.option("--facility", "-f", default="lab1", help="Packet facility code")
def update(component_type, verbose, dry, cache_file, facility):
    with open(cache_file, "r") as pickle_file:
        components = jsonpickle.decode(pickle_file.read())

    if not dry:
        for component in components:
            if component.component_type in [t + "Component" for t in component_type]:
                component.update()


if __name__ == "__main__":
    update(auto_envvar_prefix="HARDWARE")

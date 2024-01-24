#!/usr/bin/env python3

import click
from lxml import etree
import jsonpickle

from . import utils
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
def inventory(component_type, tinkerbell, verbose, dry, cache_file):
    lshw = etree.ElementTree(
        etree.fromstring(utils.lshw().replace('standalone="yes"', ""))
    )
    components = []

    for t in component_type:
        components.extend(eval(t).list(lshw))

    if verbose:
        for component in components:
            utils.log(name=component.name, contents=component)

    with open(cache_file, "w") as output:
        output.write(jsonpickle.encode(components))

    if not dry:
        post_ok = Component.post_all(components, tinkerbell)
        if not post_ok:
            raise Exception("POST to {} failed".format(tinkerbell))


if __name__ == "__main__":
    inventory(auto_envvar_prefix="HARDWARE")

#!/usr/bin/env python3

import click
from lxml import etree
import jsonpickle
import ssl

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
@click.option(
    "--cert",
    "-E",
    default=None,
    help="Path to local TLS certificate to use for HTTPS requests",
)
@click.option(
    "--key", "-k", default=None, help="Path to local TLS key to use for HTTPS requests"
)
def inventory(component_type, tinkerbell, verbose, dry, cache_file, cert, key):
    if (cert and not key) or (key and not cert):
        raise click.UsageError(
            "--cert and --key must be provided together or not at all"
        )

    ssl_context = None
    if cert:
        ssl_context = ssl.create_default_context()
        ssl_context.load_default_certs()
        ssl_context.load_cert_chain(cert, key)

    lshw = etree.ElementTree(etree.fromstring(utils.lshw()))
    components = []

    for t in component_type:
        components.extend(eval(t).list(lshw))

    if verbose:
        for component in components:
            utils.log(name=component.name, contents=component)

    with open(cache_file, "w") as output:
        output.write(jsonpickle.encode(components))

    if not dry:
        Component.post_all(components, tinkerbell, ssl_context)


if __name__ == "__main__":
    inventory(auto_envvar_prefix="HARDWARE")

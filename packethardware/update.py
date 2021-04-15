#!/usr/bin/env python3

import click
import jsonpickle
import ssl

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
def update(component_type, tinkerbell, verbose, dry, cache_file, cert, key):
    if (cert and not key) or (key and not cert):
        raise click.UsageError(
            "--cert and --key must be provided together or not at all"
        )

    ssl_context = None
    if cert:
        ssl_context = ssl.create_default_context()
        ssl_context.load_default_certs()
        ssl_context.load_cert_chain(cert, key)

    component_types = [c + "Component" for c in component_type]

    with open(cache_file, "r") as pickle_file:
        components = jsonpickle.decode(pickle_file.read())

    post_components = [c for c in components if c.component_type in component_types]
    if not dry:
        Component.post_all(post_components, tinkerbell, ssl_context)


if __name__ == "__main__":
    update(auto_envvar_prefix="HARDWARE")

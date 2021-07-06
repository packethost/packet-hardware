#!/usr/bin/env python3

import click
import json

from . import utils


@click.command()
@click.option("--uuid", help="Hardware UUID of server", required=True)
@click.option("--hollow", "-u", help="Hollow uri", required=True)
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
    help="Don't actually post anything to Hollow",
    is_flag=True,
)
@click.option(
    "--cache-file",
    "-c",
    default="/tmp/inventorybios.json",
    help="Path to local json bios features store",
)
def inventorybios(hollow, uuid, verbose, dry, cache_file):
    bios_features = utils.get_bios_features()

    if verbose:
        utils.log(name="biosfeatures", contents=bios_features)

    # Inject the hwuuid into the json
    bios_features_final = {"hardware_uuid": uuid, "values": bios_features}

    with open(cache_file, "w") as output:
        output.write(json.dumps(bios_features_final))

    if not dry:
        response = utils.http_request(hollow, json.dumps(bios_features_final), "POST")

        if response:
            utils.log(
                info="Posted BIOS feature inventory to Hollow", body=response.read()
            )
            return True
        return False


if __name__ == "__main__":
    inventorybios(auto_envvar_prefix="BIOS")

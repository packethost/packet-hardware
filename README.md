# Equinix Metal Hardware

![Continuous Integration](https://github.com/packethost/packet-hardware/actions/workflows/ci.yaml/badge.svg)

This is a tool which is used within [OSIE](https://github.com/tinkerbell/osie)
to audit hardware components to keep track of components that may need updating
or components that may be missing.

This repository is [Experimental](https://github.com/packethost/standards/blob/master/experimental-statement.md) meaning that it's based on untested ideas or techniques and not yet established or finalized or involves a radically new and innovative style! This means that support is best effort (at best!) and we strongly encourage you to NOT use this in production.

## Requirements

- `python` version `3.7` or higher
- `pip`
- `dmidecode`
- `hdparm`
- `ipmitool`
- `lsblk`
- `lshw`
- `smartctl`

Reference the Dockerfile for other dependency requirements.

## Installation

```shell
pip3 install git+https://github.com/packethost/packet-hardware.git@master
```

## Running inventory (docker)

The below command will run the script without posting the results.
```shell
# Build image
docker build -t packet-hardware:latest .

# Run tool
docker run --rm --privileged \
    -v /dev:/dev \
    -v /sys:/sys \
    -v /tmp:/tmp \
    --network host \
    packet-hardware inventory -u localhost --dry --cache-file /tmp/hardware.json
```

Here I've specified a cache file so I may look at the json pickled results.

## Usage (inventory)

```shell
# packet-hardware inventory --help
Usage: packet-hardware inventory [OPTIONS]

Options:
  -t, --component-type TEXT  Component type(s) to check
  -u, --tinkerbell TEXT      Tinkerbell uri  [required]
  -v, --verbose              Turn on verbose messages for debugging
  -d, --dry                  Don't actually post anything to API
  -c, --cache-file TEXT      Path to local json component store
  --help                     Show this message and exit.
```

## Usage (update)

```shell
# packet-hardware update --help
Usage: packet-hardware update [OPTIONS]

Options:
  -t, --component-type TEXT  Component type(s) to check
  -u, --tinkerbell TEXT      Tinkerbell uri  [required]
  -v, --verbose              Turn on verbose messages for debugging
  -d, --dry                  Don't actually post anything to API
  -c, --cache-file TEXT      Path to local json component store
  --help                     Show this message and exit.
```

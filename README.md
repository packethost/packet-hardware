# Packet Hardware

[![Build Status](https://drone.packet.net/api/badges/packethost/packet-hardware/status.svg)](https://drone.packet.net/packethost/packet-hardware)

This is a tool which is used within [OSIE](https://github.com/tinkerbell/osie)
to audit hardware components to keep track of components that may need updating
or components that may be missing.

## Requirements

- `python` version `3.5` or higher
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
docker build -t packet-hardware .

# Run tool
docker run --rm --privileged \
    -v /dev:/dev \
    -v /sys:/sys \
    -v /tmp:/tmp \
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

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
pip3 install git+https://github.com/packethost/packet-networking.git@master
```
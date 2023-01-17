#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="packet-hardware",
    version="1.3",
    description="Tool used to discover hardware components and update packet's api",
    author="James W. Brinkerhoff",
    author_email="jwb@packet.com",
    url="https://github.com/packethost/packet-hardware/",
    packages=find_packages(),
    install_requires=[
        "click",
        "jsonpickle",
        "lxml",
        "structlog",
        "urllib3",
    ],
    entry_points="""
        [console_scripts]
        packet-hardware=packethardware.cli:cli
    """,
)

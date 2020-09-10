#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="packet-hardware",
    version="1.1",
    description="Tool used to discover hardware components and update packet's api",
    author="James W. Brinkerhoff",
    author_email="jwb@packet.com",
    url="https://github.com/packethost/packet-hardware/",
    packages=find_packages(),
    install_requires=[
        "click >=6.0,<7.0",
        "jsonpickle >=0.9,<1.0",
        "lxml >=4.5,<4.6",
        "structlog >=17.2<18.0",
        "urllib3 >=1.24.2, <2",
    ],
    entry_points="""
        [console_scripts]
        packet-hardware=packethardware.cli:cli
    """,
)

#!/usr/bin/env python3

from setuptools import setup

setup(
    name = "pyms41",
    version = "0.1.0",
    description = "Library and CLI containing common utilities for flashing MS41 ECUs",
    url = "https://github.com/OpenMS41/pyms41",
    project_urls = {
        "Bug Tracker": "https://github.com/OpenMS41/pyms41/issues",
        "Source Code": "https://github.com/OpenMS41/pyms41",
    },
    license = "BSD",
    packages = ["pyms41"],
    entry_points = {
        "console_scripts": ["ms41-util=pyms41.cli:cli"],
    },
)

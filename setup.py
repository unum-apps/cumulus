#!/usr/bin/env python

import os
from setuptools import setup

version = os.environ.get("BUILD_VERSION")

if version is None:
    with open("VERSION", "r") as version_file:
        version = version_file.read().strip()

setup(
    name="unum-cumulus",
    version=version,
    package_dir = {'': 'api/lib'},
    py_modules = ['unum_cumulus'],
    install_requires=[
        'relations-unifist==0.4.1'
    ]
)

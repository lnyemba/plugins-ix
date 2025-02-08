from setuptools import setup, find_packages
import os
import sys

import meta

_args = {
    "name":meta.__app_name__,
    "version":meta.__version__,
    "author":meta.__author__,
    "packages": find_packages(include=['meta','plugins']),
    "scripts":["bin/plugin-ix"]

        }

setup(**_args)

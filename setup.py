#!/usr/bin/env python
from setuptools import find_packages, setup


project = "peetza"
version = "0.1.0"

setup(
    name=project,
    version=version,
    description="swimmio project",
    author="Pankaj Ghosh",
    author_email="pankaj.ghosh@globality.com",
    url="https://github.com/globality-corp/peetza",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "microcosm>=2.12.0",
        "microcosm-flask[metrics,spooky]>=1.20.0",
        "microcosm-logging>=1.3.0",
        "microcosm-postgres>=1.9.1",
        "microcosm-secretsmanager>=1.1.0",
        "pyOpenSSL>=18.0.0",
        "microcosm-eventsource>=2.0.0",
    ],
    setup_requires=[
        "nose>=1.3.7",
    ],
    entry_points={
        "console_scripts": [
            "createall = peetza.main:createall",
            "migrate = peetza.main:migrate",
            "runserver = peetza.main:runserver",
        ],
    },
    extras_require={
        "test": [
            "coverage>=4.0.3",
            "PyHamcrest>=1.9.0",
        ],
    },
)

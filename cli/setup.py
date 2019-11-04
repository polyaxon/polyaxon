#!/usr/bin/env python

import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


def read_readme():
    with open("README.md") as f:
        return f.read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name="polyaxon",
    version="0.5.6",
    description="Command Line Interface (CLI) and client to interact with Polyaxon API.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    maintainer="Polyaxon, Inc.",
    maintainer_email="contact@polyaxon.com",
    author="Polyaxon, Inc.",
    author_email="contact@polyaxon.com",
    url="https://github.com/polyaxon/polyaxon-cli",
    license="Apache 2.0",
    platforms="any",
    packages=find_packages(),
    keywords=[
        "polyaxon",
        "aws",
        "s3",
        "microsoft",
        "azure",
        "google cloud storage",
        "gcs",
        "deep-learning",
        "machine-learning",
        "data-science",
        "neural-networks",
        "artificial-intelligence",
        "ai",
        "reinforcement-learning",
        "kubernetes",
        "aws",
        "microsoft",
        "azure",
        "google cloud",
        "tensorFlow",
        "pytorch",
    ],
    install_requires=[
        "click==7.0",
        "click-completion==0.5.1",
        "pathlib==1.0.1",
        "sentry-sdk==0.12.3",
        "tabulate==0.8.2",
        "hestia==0.5.5",
        "Jinja2==2.10.3",
        "marshmallow==3.0.0rc5",
        "numpy>=1.15.2",
        "python-dateutil>=2.7.3",
        "pytz>=2019.2",
        "ujson>=1.35",
        "rhea==0.5.4",
        "ujson>=1.35",
        "polystores>=0.2.4",
        "psutil>=5.4.7",
        "requests>=2.20.1",
        "requests-toolbelt>=0.8.0",
        "websocket-client>=0.53.0",
    ],
    extras_require={
        "gcs": ["google-cloud-storage"],
        "s3": ["boto3", "botocore"],
        "azure": ["azure-storage"],
        "docker": ["docker"],
    },
    entry_points={"console_scripts": ["polyaxon = polyaxon.main:cli"]},
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    tests_require=["pytest"],
    cmdclass={"test": PyTest},
)

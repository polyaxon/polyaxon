#!/usr/bin/env python
import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


def read_readme():
    if not os.path.exists("../README.md"):
        return ""
    with open("../README.md") as f:
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


with open(os.path.join("./polyaxon/pkg.py"), encoding="utf8") as f:
    pkg = {}
    exec(f.read(), pkg)

setup(
    name=pkg["NAME"],
    version=pkg["VERSION"],
    description=pkg["DESC"],
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    maintainer=pkg["AUTHOR"],
    maintainer_email=pkg["EMAIL"],
    author=pkg["AUTHOR"],
    author_email=pkg["EMAIL"],
    url=pkg["URL"],
    license=pkg["LICENSE"],
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
        "click<8.0",
        "click-completion<0.6",
        "tabulate<0.9.0",
        "Jinja2>=2.10.3",
        "kubernetes>=10.0.1",
        "marshmallow<3.12.0",
        "polyaxon-sdk==1.9.1",
        "python-dateutil>=2.7.3",
        "pytz>=2019.2",
        "PyYAML>=5.1",
        "ujson>=1.35",
        "requests>=2.20.1",
        "requests-toolbelt>=0.8.0",
        "sentry-sdk>=0.12.3",
        "certifi>=2019.9.11",
        "psutil",
    ],
    extras_require={
        "gcs": ["google-cloud-storage"],
        "s3": ["boto3", "botocore"],
        "azure": ["azure-storage-blob>=12.3.1"],
        "docker": ["docker"],
        "git": ["gitpython"],
        "numpy": ["numpy"],
        "polytune": ["scikit-learn==0.24.2", "hyperopt==0.2.5"],
        "polyboard": [
            "Pillow",
            "matplotlib<3.3.3",
            "moviepy",
            "plotly",
            "bokeh",
            "pandas",
            "altair",
        ],
        "streams": [
            "kubernetes_asyncio==12.0.1",
            "starlette==0.14.1",
            "aiofiles==0.6.0",
            "uvicorn==0.13.3",
            "uvloop==0.14.0",
            "httptools==0.1.1",
            "python-multipart==0.0.5",
            "pandas",
        ],
    },
    entry_points={
        "console_scripts": ["polyaxon = polyaxon.main:cli", "plx = polyaxon.main:cli"]
    },
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    tests_require=["pytest"],
    cmdclass={"test": PyTest},
)

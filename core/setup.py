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

with open("requirements/requirements.txt") as requirements_file:
    requirements = requirements_file.read().splitlines()

if os.environ.get("USE_PROD_PACKAGES"):
    requirements += [
        "polyaxon-sdk=={}".format(pkg["VERSION"]),
        "traceml=={}".format(pkg["VERSION"]),
    ]

with open("requirements/dev.txt") as requirements_file:
    dev_requirements = requirements_file.read().splitlines()

extra = {
    "dev": dev_requirements,
    "gcs": ["gcsfs"],
    "s3": ["s3fs"],
    "azure": ["adlfs"],
    "docker": ["docker"],
    "git": ["gitpython"],
    "numpy": ["numpy"],
    "polytune": ["scikit-learn", "hyperopt"],
    "polyboard": [
        "Pillow",
        "matplotlib",
        "moviepy",
        "plotly",
        "bokeh",
        "pandas",
        "altair",
    ],
    "streams": [
        "kubernetes_asyncio>=12.1.1,<22.6.0",
        "starlette==0.18.0",
        "aiofiles==0.8.0",
        "uvicorn[standard]==0.17.4",
        "uvloop==0.16.0",
        "python-multipart==0.0.5",
        "pandas",
    ],
}

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
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
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
    install_requires=requirements,
    extras_require=extra,
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

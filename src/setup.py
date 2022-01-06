#!/usr/bin/env python

import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(name='datatile',
      version='0.2.0',
      description='A data catalog, summary, viz, and profiling package.',
      maintainer='Polyaxon, Inc',
      maintainer_email='contact@polyaxon.com',
      url='https://github.com/polyaxon/datatile',
      license='Apache 2.0',
      platforms='any',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      keywords=['pandas', 'data analysis', 'machine learning'],
      install_requires=[
          'numpy',
          'pandas',
      ],
      classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering'
      ],
      tests_require=['pytest'],
      cmdclass={'test': PyTest})

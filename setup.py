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


setup(name='polyaxon-cli',
      version='0.1.6',
      description='Command Line Interface (CLI) for Polyaxon.',
      maintainer='Mourad Mourafiq',
      maintainer_email='mouradmourafiq@gmail.com',
      author='Mourad Mourafiq',
      author_email='mouradmourafiq@gmail.com',
      url='https://github.com/polyaxon/polyaxon-cli',
      license='MIT',
      platforms='any',
      packages=find_packages(),
      keywords=[
          'polyaxon',
          'tensorFlow',
          'deep-learning',
          'machine-learning',
          'data-science',
          'neural-networks',
          'artificial-intelligence',
          'ai',
          'reinforcement-learning',
          'kubernetes',
      ],
      install_requires=[
          "click==6.7",
          "pathlib==1.0.1",
          "polyaxon-client==0.1.6",
          "raven==6.7.0",
          "tabulate==0.8.2",
          "six==1.11.0",
      ],
      entry_points={
          "console_scripts": [
              "polyaxon = polyaxon_cli.main:cli",
          ],
      },
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence'
      ],
      tests_require=['pytest'],
      cmdclass={'test': PyTest})

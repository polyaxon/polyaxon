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


setup(name='polyaxon-client',
      version='0.2.8',
      description='Python client to interact with Polyaxon API.',
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
          'aws',
          's3',
          'microsoft',
          'azure',
          'google cloud storage',
          'gcs',
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
          "clint==0.5.1",
          "polyaxon-schemas==0.2.8",
          "psutil==5.4.7",
          "requests==2.19.1",
          "requests-toolbelt==0.8.0",
          "websocket-client==0.53.0",
      ],
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence'
      ],
      tests_require=[
          "pytest",
          "httpretty==0.8.14",
          "fake-factory==0.7.2"
      ],
      cmdclass={'test': PyTest})

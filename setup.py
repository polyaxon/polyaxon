#!/usr/bin/env python

import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


def read_readme():
    with open('README.md') as f:
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


setup(name='polyaxon-deploy',
      version='0.5.0',
      description='Tools to validate and deploy Polyaxon to one of the supported platforms.',
      long_description=read_readme(),
      long_description_content_type="text/markdown",
      maintainer='Mourad Mourafiq',
      maintainer_email='mourad@polyaxon.com',
      author='Mourad Mourafiq',
      author_email='mourad@polyaxon.com',
      url='https://github.com/polyaxon/polyaxon-deploy',
      license='MIT',
      platforms='any',
      packages=find_packages(),
      keywords=[
          'polyaxon',
          'aws',
          'microsoft',
          'azure',
          'google cloud',
          'tensorFlow',
          'pytorch',
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
          "polyaxon-schemas==0.5.0",
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
          "fake-factory==0.7.2",
          "mock",
      ],
      cmdclass={'test': PyTest})

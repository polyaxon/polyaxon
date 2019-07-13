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


setup(name='polystores',
      version='0.2.0',
      description='Polystores is an abstraction and a collection of clients '
                  'to interact with cloud storages.',
      long_description=read_readme(),
      long_description_content_type="text/markdown",
      maintainer='Mourad Mourafiq',
      maintainer_email='mourad@polyaxon.com',
      author='Mourad Mourafiq',
      author_email='mourad@polyaxon.com',
      url='https://github.com/polyaxon/polystores',
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
          'machine-learning',
          'data-science',
          'artificial-intelligence',
          'ai',
          'reinforcement-learning',
          'kubernetes',
          'docker'
      ],
      install_requires=[
          "rhea>=0.4.2",
      ],
      extras_require={
          "s3": [
              "boto3",
              "botocore",
          ],
          "gcs": [
              "google-cloud-storage",
          ],
          "azure": [
              "azure-storage",
          ],
      },
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence'
      ],
      tests_require=[
          "pytest",
      ],
      cmdclass={'test': PyTest})

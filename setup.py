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


setup(name='ocular',
      version='0.0.4',
      description="A tool for observing Kubernetes pods' statuses in real time.",
      maintainer='Mourad Mourafiq',
      maintainer_email='mourad@polyaxon.com',
      author='Mourad Mourafiq',
      author_email='mourad@polyaxon.com',
      url='https://github.com/polyaxon/ocular',
      license='MIT',
      platforms='any',
      packages=find_packages(),
      keywords=[
          'polyaxon',
          'aws',
          'azure',
          'google cloud storage',
          'k8s',
          'kubernetes',
          'docker'
      ],
      install_requires=[
          "hestia>=0.2.0",
          "kubernetes>=7.0.0",
          "six==1.11.0"
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
      ],
      cmdclass={'test': PyTest})

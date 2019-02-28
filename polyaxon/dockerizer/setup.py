#!/usr/bin/env python

# noqa


import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        # pylint:disable=attribute-defined-outside-init
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(name='polyaxon-dockerizer',
      version='0.4.1',
      description='Polyaxon dockerizer.',
      maintainer='Mourad Mourafiq',
      maintainer_email='mourad@polyaxon.com',
      author='Mourad Mourafiq',
      author_email='mourad@polyaxon.com',
      url='https://github.com/polyaxon/polyaxon',
      license='MPL-2.0',
      platforms='any',
      packages=find_packages(),
      keywords=[
          'polyaxon',
          'kubernetes',
          'containers',
          'docker'
          'instrumentation'
      ],
      install_requires=[
          'polyaxon-client==0.4.1',
          'Unipath==1.1'
      ],
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Programming Language :: Python :: 3',
          'Topic :: Internet :: WWW/HTTP',
      ],
      tests_require=[
          "pytest",
      ],
      cmdclass={'test': PyTest})

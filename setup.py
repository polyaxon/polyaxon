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


setup(name='rhea',
      version='0.5.4',
      description='Efficient environment variables management and typing for python.',
      long_description_content_type="text/markdown",
      long_description=read_readme(),
      maintainer='Mourad Mourafiq',
      maintainer_email='mourad.mourafiq@gmail.com',
      author='Mourad Mourafiq',
      author_email='mourad.mourafiq@gmail.com',
      url='https://github.com/polyaxon/rhea',
      license='MIT',
      platforms='any',
      packages=find_packages(),
      keywords=[
          'polyaxon',
          'dotenv',
          'environ',
          'environment',
          'env-vars',
          '.env',
          'django',
      ],
      install_requires=[
          'PyYAML>=5.1',
          'six==1.12.0',
      ],
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Internet :: WWW/HTTP',
      ],
      tests_require=[
          "pytest",
      ],
      cmdclass={'test': PyTest})

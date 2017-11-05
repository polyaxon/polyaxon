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


setup(name='polyaxon-api',
      version='0.0.1',
      description='Deep Learning library for TensorFlow for '
                  'building end to end models and experiments.',
      maintainer='Mourad Mourafiq',
      maintainer_email='mouradmourafiq@gmail.com',
      author='Mourad Mourafiq',
      author_email='mouradmourafiq@gmail.com',
      url='https://github.com/polyaxon/polyaxon-api',
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
          'reinforcement-learning'
      ],
      install_requires=[
          "celery==4.1.0",
          "Django==1.11.6",
          "django-cors-headers==2.1.0",
          "djangorestframework==3.7.0",
          "djangorestframework-camel-case==0.2.0",
          "django-registration==2.3",
          "pandas==0.20.3",
          "pandas-summary==0.0.41",
          "polyaxon-schemas==0.0.15",
          "psycopg2==2.7.3.1",
          "redis==2.10.6",
          "six==1.11.0",
          "tensorflow==1.3.0",
          "Unipath==1.1",
          "uWSGI==2.0.15",
      ],
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence'
      ],
      tests_require=['pytest'],
      cmdclass={'test': PyTest})

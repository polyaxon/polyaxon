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


setup(name='polyaxon',
      version='0.4.1',
      description='A platform for reproducible and scalable deep learning and machine learning.',
      long_description=read_readme(),
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
          'tensorFlow',
          'kubernetes',
          'deep-learning',
          'machine-learning',
          'data-science',
          'neural-networks',
          'artificial-intelligence',
          'ai',
          'reinforcement-learning'
      ],
      install_requires=[
          "celery==4.2.1",
          "Django==2.1.7",
          "django-cors-headers==2.4.0",
          "djangorestframework==3.8.2",
          "docker==3.5.1",
          "GitPython==2.1.11",
          "Jinja2==2.10",
          "pika==0.12.0",
          "psutil==5.4.7",
          "psycopg2-binary==2.7.5",
          "redis==2.10.6",
          "sanic==0.8.3",
          "Unipath==1.1",
          "uWSGI==2.0.17.1",
          "websockets==5.0.1",
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

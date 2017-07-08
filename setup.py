#!/usr/bin/env python

import sys
from setuptools import setup, find_packages
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


setup(name='polyaxon',
      version='0.0.27',
      description='Deep Learning library for TensorFlow for '
                  'building end to end models and experiments.',
      maintainer='Mourad Mourafiq',
      maintainer_email='mouradmourafiq@gmail.com',
      author='Mourad Mourafiq',
      author_email='mouradmourafiq@gmail.com',
      url='https://github.com/polyaxon/polyaxon',
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
          'numpy',
          'six',
          'Pillow',
          'pyyaml',
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

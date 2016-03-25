#!/usr/bin/env python

from setuptools import setup

setup(name='pandas-summary',
      version='0.0.3',
      description='An extension to pandas describe function.',
      maintainer='Mourad Mourafiq',
      maintainer_email='mouradmourafiq@gmail.com',
      url='https://github.com/mouradmourafiq/pandas-summary',
      license='MIT',
      platforms='any',
      packages=['pandas_summary'],
      keywords=['pandas', 'data analysis', 'machine learning'],
      install_requires=[
          'numpy',
          'pandas',
      ],
      classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering'
      ])

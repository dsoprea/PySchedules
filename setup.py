from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='pyschedules',
      version=version,
      description="Interface to Schedules Direct.",
      long_description="""\
A library to pull channel, schedules, actors, and QAM maps (channels.conf) data.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='dvb television tv cable schedules direct channel channels qam',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='https://github.com/dsoprea/PySchedules',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'xml',
          'mx',
          'urllib2', 
          'zlib',
          'parsedatetime',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )


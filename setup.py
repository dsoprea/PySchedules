from setuptools import setup, find_packages

version = '0.1.3'

setup(name='pyschedules',
      version=version,
      description="Interface to Schedules Direct.",
      long_description="""\
A complete library to pull channels, schedules, actors, lineups, and QAM-maps (channels.conf) data from Schedules Direct.""",
      classifiers=['Development Status :: 3 - Alpha', 
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                   'Programming Language :: Python',
                   'Topic :: Home Automation',
                   'Topic :: Multimedia :: Video :: Capture',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                  ],
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


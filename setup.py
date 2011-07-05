from setuptools import setup, find_packages
import sys, os

version = '0.1.1'

setup(name='filemover',
      version=version,
      description="Framework for movng files by different applications",
      long_description="""\
Framework for moving files from different applications""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Brent Hoover',
      author_email='brent@autoshepherd.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      data_files=[('/var/files/', ['cfg/filemover.ini']),],
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points= {'console_scripts': ['filemover = filemover.core:main']}
      )

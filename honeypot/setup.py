#!/usr/bin/env python

from __future__ import with_statement

import sys

from setuptools import setup, find_packages

from honeypot.honey_loader.version import get_version


with open('../README.md') as f:
    readme = f.read()

long_description = """
To find out what's new in this version of SuperHoneyPot, please see the changelog file

----

%s

----

The honey pot allows connections to be made to it, and mimics the appropriate protocols without actually allowing access.
It gathers information from whoever attempts the connection.`.
""" % (readme)

if sys.version_info[:2] < (2, 6):
    install_requires=['paramiko>=1.10,<1.13']
else:
    install_requires=['paramiko>=1.10,<2.0']


setup(
        name='SuperHoneyPot',
        version=get_version('short'),
        description='A plugin based honeypot that\'s easy to install and use.',
        long_description=long_description,
        author='Chris Benda, Stephen Chavez, Fred Montoya, Mikhail Batkalin, Brad Gill, William King',
        author_email='stephen.chavez12@gmail.com',
        url='https://github.com/redragonx/SuperHoneyPot',
        packages=find_packages(),
        test_suite='',
        tests_require=[],
        install_requires=install_requires,
        entry_points={
            'console_scripts': [
                'fab = fabric.main:main',
            ]
        },
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: AGPL License',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Unix',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.5',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Topic :: Software Development',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Clustering',
            'Topic :: System :: Software Distribution',
            'Topic :: System :: Systems Administration',
        ],
)
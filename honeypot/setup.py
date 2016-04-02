#!/usr/bin/env python

from __future__ import with_statement

import os
import sys

from setuptools import setup, find_packages



path = os.path.dirname(os.path.realpath(__file__))+ os.sep + "honey_loader"
sys.path.insert(0, path)

import version

path = os.path.dirname(os.path.realpath(__file__)).replace('honeypot','')

with open(path + 'README.md') as f:
    readme = f.read()

long_description = """
To find out what's new in this version of SuperHoneyPot, please see the changelog file

----

%s

----

The honey pot allows connections to be made to it, and mimics the appropriate protocols without actually allowing access.
It gathers information from whoever attempts the connection.`.
""" % (readme)

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
        name='SuperHoneyPot',
        version=version.get_version('short'),
        description='A plugin based honeypot that\'s easy to install and use.',
        long_description=long_description,
        author='Chris Benda, Stephen Chavez, Fred Montoya, Mikhail Batkalin, Brad Gill, William King',
        author_email='stephen.chavez12@gmail.com',
        url='https://github.com/redragonx/SuperHoneyPot',
        packages=find_packages(),
        package_data={
            'data_files':['*.txt','*.pem','*.key']
            },
        include_package_data = True,
        test_suite='nose.collector',
        tests_require=['nose'],
        install_requires=requirements,
        entry_points={
            'console_scripts': [
                'honeypot = honey_loader.loader:start_plugins'
            ]
        },
        classifiers=[
            'Development Status :: 2 - Beta',
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
            'Topic :: System :: Systems Administration',
            'Topic :: Networking :: Network Sniffer'
        ],
)
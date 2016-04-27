#!/usr/bin/env python
"""
    This file is part of SuperHoneyPot.

    SuperHoneyPot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SuperHoneyPot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with SuperHoneyPot.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import with_statement
import os
import sys
from setuptools import setup, find_packages

# Sets the path to locate the version.py file for import of version
path = os.path.dirname(os.path.realpath(__file__))+ os.sep + "honey_loader"
sys.path.insert(0, path)

import version

# Sets the path to locate the readme.txt file
path = os.path.dirname(os.path.realpath(__file__))
print(path)
path1 = path
readme_path = path + os.sep +'README.txt'
print(readme_path)

# Sets the path to the parent directory
path = os.path.dirname(os.path.realpath(__file__)).replace('honeypot','')
print(path)

with open(readme_path) as f:
    readme = f.read()

long_description = """
To find out what's new in this version of SuperHoneyPot, please see the changelog file

----

%s

----

The honey pot allows connections to be made to it, and mimics the appropriate protocols without actually allowing access.
It gathers information from whoever attempts the connection.`.
""" % (readme)

with open(path1 + os.sep + 'requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
        name='SuperHoneyPot',
        version=version.get_version('short'),
        description='A plugin based honeypot that\'s easy to install and use.',
        long_description=long_description,
        author='Chris Benda, Stephen Chavez, Fred Montoya, Mikhail Batkalin, Brad Gill, William King',
        author_email='stephen@dicesoft.net',
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
            'Programming Language :: Python :: 2.7',
            'Topic :: System :: Systems Administration',
            'Topic :: Networking :: Network Sniffer'
        ],
)

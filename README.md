# SuperHoneyPot

The honey pot allows connections to be made to it, and mimics the appropriate protocols that are defined as plugins without actually allowing access. It gathers information from whoever attempts the connection, and stores the information remotely in a MongoDB database.  This application was built around running on a RaspberryPi Zero to make it easy to deploy in any physical environment with a network. We wanted a cost effective solution that could be installed in a matter of minutes.


Text file Client Requirements are here: https://github.com/redragonx/HoneyPotExtras

[![Build Status](https://travis-ci.org/TheFixers/SuperHoneyPot.svg?branch=master)](https://travis-ci.org/TheFixers/SuperHoneyPot)


Navigation
----------
[SuperHoneyPot](#superhoneypot) |
[Requirements](#requirements) |
[Folder Structure](#folder-structure) |
[Installation](#installation) |
[Development](#development) |
[Deployment](#deployment) |
[Contributions](#contributions) |
[Team](#team) |
[Copyright](#copyright) |
[Licence](#licence) |
[Contact](#contact)


Requirements
------------
This project assumes you have some python know how.

Folder Structure
----------------
<pre>
.
├── blah.txt
├── honeypot
│   ├── CHANGELOG.md
│   ├── data_files
│   │   ├── __init__.py
│   │   ├── mail_info.txt
│   │   ├── mongoClient.txt
│   │   ├── plugins.txt
│   │   ├── privateSSHKey.key
│   │   └── ssl.pem
│   ├── db_interface
│   │   ├── honeypot_db_interface.py
│   │   ├── honeypot_db_interface.pyc
│   │   ├── __init__.py
│   │   └── python_mail.py
│   ├── demo_server.log
│   ├── honey_loader
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── loader.pyc
│   │   ├── __main__.py
│   │   ├── pluginsReader.py
│   │   └── version.py
│   ├── __init__.py
│   ├── LICENSE
│   ├── MANIFEST.in
│   ├── plugins
│   │   ├── http_reader.py
│   │   ├── http_reader.pyc
│   │   ├── https_reader.py
│   │   ├── https_reader.pyc
│   │   ├── __init__.py
│   │   ├── ssh_plugin.py
│   │   ├── ssh_plugin.pyc
│   │   ├── telnet_reader.py
│   │   └── telnet_reader.pyc
│   ├── README.txt
│   ├── requirements.txt
│   ├── requires.txt
│   ├── setup.py
│   └── tests
│       ├── http_reader_test.py
│       ├── https_reader_test.py
│       ├── loader_test.py
│       ├── plugin_test.py
│       ├── ssh_plugin_test.py
│       └── telnet_reader_test.py
└── README.md

6 directories, 42 files

</pre>

Installation
------------
<ul>
<li> Install Python 2.7.11</li>
<li>You will need to have an instance of MongoDB server installed remotely, and add the access details to the mongoClient.txt configuration file.</li>
<li> Install dependencies: go to your project directory and type <code>pip -r requirements.txt</code></li>
<li> Install nose tests if you want to run the tests</li>
</ul>

Development
-----------------------
put text here.

Deployment
----------
There are a few ways to run the app, but first edit the login details for the database and email (used for adminsterating) under data_files folder. Then run `sudo python honeypot/honey_loader/loader.py` to test your changes. Or you can create a package for your OS. 

For Debian: You'll need <a href="https://pypi.python.org/pypi/stdeb">stdeb</a> then run `python setup.py --command-packages=stdeb.command bdist_deb` in the honeypot folder. Install the .deb file. Then run `sudo honeypot`

For Pip: Run `python setup.py sdist` then run `sudo python setup.py install` To run it `sudo honeypot`

Please note that your config files in data_files will be whatever they are set to when building a package. You may need to change them after installing the package.

Contributions
-------------
We would love for other people to contribute to this. All work should be done on feature-specific branches and pull requests will be moderated by admins. :)

#### General workflow
* `Make a new fork`
* `git branch <new branch>`
* `git checkout <new branch>`
* `git push -u origin <new branch>`

Team
----

- Chris Benda
- Stephen Chavez
- Fred Montoya
- Mikhail Batkalin
- Brad Gill
- William King

Copyright
---------
&copy; 2016 Stephen Chavez 

Licence
-------
AGPL

Contact
-------
Email: <a href="mailto:stephen@dicesoft.net">stephen@dicesoft.net</a>

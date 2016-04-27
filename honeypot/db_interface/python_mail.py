#!/usr/bin/python2

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


import smtplib
import os

# Specifying the from and to addresses

class python_mail():

    path_to_mail_info = os.path.dirname(os.path.realpath(__file__)).replace("db_interface", "data_files")
    text_file = open(path_to_mail_info + os.path.sep + "mail_info.txt", "r")
    info = text_file.readlines()
    info = [x.strip('\n') for x in info]

    fromaddr = info[0]
    toaddrs  = info[1]

    # Writing the message (this message will appear in the email)

    msg = 'Failed a connection to MongoDB server. Please check database status.'

    # Gmail Login

    username = info[2]
    password = info[3]

    def __init__(self):
        pass

    # Sending the mail
    def send_mail(self):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(self.fromaddr, self.toaddrs, self.msg)
        server.quit()

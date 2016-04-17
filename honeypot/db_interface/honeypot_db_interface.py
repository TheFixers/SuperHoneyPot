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

## https://docs.mongodb.org/getting_started/python/client


from pymongo import MongoClient, errors
import python_mail
import json, bson
import os
import threading

path_to_mongoClient = os.path.dirname(os.path.realpath(__file__)).replace("db_interface", "data_files")
mongoClient = open(path_to_mongoClient + os.path.sep + "mongoClient.txt", "r").read() # get first line of file


class honeypot_database_interface():

    # this will contain the information needed to connect to the remote database
    db_host = MongoClient(mongoClient, socketTimeoutMS=10000)
    database = db_host.HoneyPot
    mail_server = python_mail.python_mail()

    def __init__(self):
        pass

    def create_db_connection(self):
        honeypot_database_interface.database = MongoClient(honeypot_database_interface.db_host)
        return

    def receive_data(self, json_dump_in):
        # receives data from the plugins
        result = None
        current_data = json.loads(json_dump_in)
        # data may need to be formatted here, prior to sending to database below

        try:
            honeypot_database_interface.database.clientInfo.insert_one(current_data).inserted_id
        except errors.ServerSelectionTimeoutError:
            self.mail_server.send_mail()
        return

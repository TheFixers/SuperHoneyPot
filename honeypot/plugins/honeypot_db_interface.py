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


from pymongo import MongoClient
import json, bson


class honeypot_database_interface():

    # this will contain the information needed to connect to the remote database
    db_host = MongoClient("mongodb://HoneyPot:TeddyBearFood123@54.200.61.193:27017/HoneyPot")
    database = db_host.HoneyPot

    def __init__(self):
        pass

    def create_db_connection(self):
        honeypot_database_interface.database = MongoClient(honeypot_database_interface.db_host)
        return

    def receive_data(self, json_dump_in):
        # receives data from the plugins
        current_data = json.loads(json_dump_in)
        # data may need to be formatted here, prior to sending to database below
        result = honeypot_database_interface.database.HoneyPot.insert_one(current_data)
        result.inserted_id
        return

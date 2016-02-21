## https://docs.mongodb.org/getting_started/python/client


from pymongo import MongoClient
import json


class honeypot_database_interface():

    # this will contain the information needed to connect to the remote database
    db_host = 'superhoneypot:password@<cloudhost>:<cloudhost_port>/honeypot'
    database = None

    def __init__(self):
        pass

    def create_db_connection(self):
        honeypot_database_interface.database = MongoClient(honeypot_database_interface.db_host)
        return

    def receive_data(json_dump_in):
        # receives data from the plugins
        current_data = json_dump_in
        # data may need to be formatted here, prior to sending to database below
        honeypot_database_interface.database.insert_one(current_data)
        return

## https://docs.mongodb.org/getting_started/python/client


from pymongo import MongoClient
import json


class honeypot_database_interface():

    # this will contain the information needed to connect to the remote database
    db_host = 'superhoneypot:password@<cloudhost>:<cloudhost_port>/honeypot'

    def __init__(self):
        pass

    def create_db_connection(self):
        database = MongoClient(honeypot_database_interface.db_host)
        return

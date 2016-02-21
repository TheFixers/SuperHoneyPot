## https://docs.mongodb.org/getting_started/python/client


from pymongo import MongoClient
import json


class widget_database_interface():

    # this will contain the information needed to connect to the remote database
    db_host = 'superhoneypot:password@<cloudhost>:<cloudhost_port>/honeypot'
    database = None

    def __init__(self):
        pass

    def create_db_connection(self):
        widget_database_interface.database = MongoClient(widget_database_interface.db_host)
        return

    def receive_query(request):
        # receives request from user browser client
        current_request = request
        widget_database_interface.database.find(current_request)
        return

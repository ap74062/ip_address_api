from pymongo import MongoClient


class Database:
    # Generic name Data because it's only collection with all the data.
    indexes = ['_id', 'ip_address']

    def __init__(self, host: str, port: str, db: str, collection: str):
        connection_string = 'mongodb://{}:{}'.format(host, port)
        self.client = MongoClient(connection_string)
        self.db = self.client[db]
        self.collection = self.db[collection]

        # It will ignore index creation if already exist
        self.collection.create_index("ip_address")

    def get_row(self, ip_address: str) -> dict:
        return self.collection.find_one({"ip_address": ip_address})

    def add_row(self, ip_address: str, ipstack_result: dict):
        self.collection.insert_one({"ip_address": ip_address,
                                           "ipstack_result": ipstack_result})

    def remove_row(self, ip_address: str):
        self.collection.delete_one({"ip_address": ip_address})

    def update_row(self, ip_address: str, ipstack_result: dict):
        self.remove_row(ip_address)
        self.add_row(ip_address, ipstack_result)

    def close(self):
        self.client.close()

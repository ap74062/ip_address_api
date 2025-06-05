import redis
import pickle

class Cache:
    def __init__(self, host, port):
        self.client = redis.Redis(host=host, port=port)
        self.client.ping()

    def set(self, key: str, value: dict):
        if type(value) not in [dict]:
            raise Exception("Cache is prepared to save key-value where value type is dict")

        pickled_value = pickle.dumps(value)
        self.client.set(key, pickled_value)

    def get(self, key: str) -> dict:
        pickled_value = self.client.get(key)
        if pickled_value:
            return pickle.loads(pickled_value)

        return pickled_value

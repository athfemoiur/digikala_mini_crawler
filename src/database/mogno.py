from pymongo import MongoClient
from decouple import config


class MongoDataBase:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.__client = MongoClient(config('mongo_uri'))
        self.database = self.__client[config('db_name')]

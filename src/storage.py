from database.mogno import MongoDataBase


class MongoStorage:
    @staticmethod
    def insert_phones(data):
        client = MongoDataBase()
        client.database['phone'].update_one(
            {'product_id': data['product_id']},
            {'$set': data},
            True
        )

    @staticmethod
    def insert_phones_history(data):
        client = MongoDataBase()
        client.database['phone-history'].insert_one(data)

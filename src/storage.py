from database.mogno import MongoDataBase


class MongoStorage:
    @staticmethod
    def insert_phones(data):
        """
        insert new doc or update the existing one
        """
        client = MongoDataBase()
        client.database['phone'].update_one(
            {'product_id': data['product_id']},
            {'$set': data},
            True
        )

    @staticmethod
    def insert_phones_history(data):
        """
        insert new doc
        """
        client = MongoDataBase()
        client.database['phone-history'].insert_one(data)

    @staticmethod
    def find_phone_by_object_id(object_id):
        client = MongoDataBase()
        return client.database['phone'].find_one({'_id': object_id})

    @staticmethod
    def delete_phone(filter):
        client = MongoDataBase()
        client.database['phone'].delete_one(filter)
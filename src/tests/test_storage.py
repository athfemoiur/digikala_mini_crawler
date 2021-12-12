from unittest import TestCase
from bson import ObjectId

from storage import MongoStorage


class StorageTestCase(TestCase):
    def setUp(self):
        self.data = {'product_id': '4958276', 'url': 'url', 'title': 'title', 'price': 'price',
                     'prev_price': 'prev_price', 'image_url': 'image_url',
                     'construction_quality': 'construction_quality',
                     'worth_buying': 'worth_buying', 'innovation': 'innovation', 'feature': 'feature',
                     'ease_of_use': 'ease_of_use', 'design': 'design'
                     }
        self.storage = MongoStorage()

    def test_insert_phones(self):
        instance_id = self.storage.insert_phones(self.data).inserted_id
        self.assertEqual(self.data, self.storage.find_phone_by_object_id(ObjectId(instance_id)))

    def tearDown(self):
        self.storage.delete_phone(self.data)

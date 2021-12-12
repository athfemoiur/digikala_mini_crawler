from unittest import TestCase
import requests

from parser import Parser


class ParserTest(TestCase):
    def test_get_all_data(self):
        main_doc = requests.get(
            'https://www.digikala.com/product/dkp-4958276/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9'
            '%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-poco-x3-pro-m2102j20sg-%D8%AF%D9%88'
            '-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7'
            '%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85').text
        ratings_doc = requests.get(
            'https://www.digikala.com/ajax/product/comments/4958276/?page=1&mode=newest_comment').text
        data = Parser().get_all_data(main_doc, ratings_doc)
        self.assertIsInstance(data, dict)
        self.assertTrue(all(
            x in data for x in
            ['title', 'price', 'prev_price', 'image_url''construction_quality', 'worth_buying', 'innovation', 'feature',
             'ease_of_use', 'design'])
        )
        self.assertEqual(data['title'],
                         'گوشی موبایل شیائومی مدل POCO X3 Pro M2102J20SG دو سیم‌ کارت ظرفیت 256 گیگابایت و 8 گیگابایت '
                         'رم')


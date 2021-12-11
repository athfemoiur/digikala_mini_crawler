import re
from queue import Queue
from threading import Thread
import grequests
import requests
from bs4 import BeautifulSoup

from config import LINKS_BASE_URL, BASE_URL, RATING_BASE_URL
from parser import Parser
from storage import MongoStorage


class DataCrawler:

    def __init__(self):
        self.storage = MongoStorage()
        self.parser = Parser()
        self.links = self.get_links(self.get(LINKS_BASE_URL).text)
        self.queue = self.create_queue()

    def create_queue(self):
        queue = Queue()
        for link in self.links:
            queue.put(link)
        return queue

    def start(self):
        for _ in range(10):
            thread = Thread(target=self.crawl)
            thread.start()
        self.queue.join()

    @staticmethod
    def get(url, header=None, proxy=None):
        try:
            response = requests.get(url, headers=header, proxies=proxy)
        except requests.HTTPError:
            return None
        return response

    @staticmethod
    def get_links(html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        return [BASE_URL + lnk.get('href') for lnk in soup.find_all('a', attrs={'class': 'js-product-item'})]

    @staticmethod
    def get_product_id(url):
        return re.search('[0-9]{7}', url).group()

    def crawl(self):
        while True:
            phone_link = self.queue.get()
            product_id = self.get_product_id(phone_link)
            urls = [phone_link, RATING_BASE_URL.format(product_id)]
            rs = (grequests.get(u) for u in urls)
            responses = grequests.map(rs)
            if not all(response.status_code == 200 for response in responses):
                self.queue.put(phone_link)
            else:
                html_docs = (response.text for response in responses)
                self.store(phone_link, product_id, self.parser.get_all_data(*html_docs))
            print('done')
            self.queue.task_done()
            if self.queue.empty():
                break

    def store(self, link, product_id, data):
        total_data = {'product_id': product_id, 'url': link, **data}
        self.storage.insert_phones(total_data)
        self.storage.insert_phones_history(total_data)

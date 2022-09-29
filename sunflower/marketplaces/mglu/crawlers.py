import time
import json
import logging
from sunflower.base import BaseCrawler
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer


class CategoryCrawler(BaseCrawler):
    def __init__(self, url):
        super().__init__(url, CategorySerializer)

    def load(self):
        categories = self.find_all("a", {"class": "link-of-menu"}, href=True)
        return list(filter(lambda x: x, categories))


class ProductCrawler(BaseCrawler):
    def __init__(self, url, page=1):
        url = f"{url}?page={page}"
        super().__init__(url, ProductSerializer)

    def load(self):
        products = self.find("ul", {"role": "main"})
        return list(filter(lambda x: x, products))


class ReviewCrawler(BaseCrawler):
    def __init__(self, url, page=1):
        url = f"{url}?page={page}"
        super().__init__(url, ReviewSerializer)
    
    def load(self):
        try:
            reviews = self.json_serialize()
        except Exception as e:
            logging.error(f"{e}, Sleeping for 60 seconds.")
            time.sleep(60)
        else:
            return list(filter(lambda x: x, reviews))
        return []

    def json_serialize(self, *args, **kwargs):
        raw_json = json.loads(self.response.text)
        items = map(self.serialize, raw_json["data"]["objects"])
        return list(items)

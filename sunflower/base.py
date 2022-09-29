import time
from abc import ABC, abstractmethod
from collections.abc import Iterable
from requests.exceptions import ConnectionError  # noqa

from bs4 import BeautifulSoup
from bs4.element import Tag

from sunflower.settings import session, logging


class BaseSunflower(ABC):
    def __init__(self, marketplace_url):
        self.marketplace_url = marketplace_url

    @abstractmethod
    def load_categories(self):
        pass

    @abstractmethod
    def load_products(self):
        pass
    
    @abstractmethod
    def load_product_reviews(self, product_id):
        pass


class BaseCrawler(ABC):
    def __init__(self, url, serializer):
        self.url = url
        self.serializer = serializer

    @property
    def html(self):
        return self.response.text

    @property
    def response(self):
        if self.url not in session.cache.urls:
            logging.info(f"Sleeping for 30 seconds before requesting {self.url}.")
            time.sleep(30)
        # TODO: solve ConnectionError
        return session.get(self.url)
    
    @abstractmethod
    def load(self):
        ...

    def find(self, *args, **kwargs):
        soup = BeautifulSoup(self.html, "html.parser")
        element = soup.find(*args, **kwargs)
        items = list()
        if isinstance(element, Tag):
            items = filter(
                lambda x: x is not None, map(self.serialize, element.contents)
            )
        return list(items)

    def find_all(self, *args, **kwargs):
        soup = BeautifulSoup(self.html, "html.parser")
        elements = soup.find_all(*args, **kwargs)
        items = filter(lambda x: x is not None, map(self.serialize, elements))
        return list(items)

    def serialize(self, item):
        return self.serializer(item, many=False).data


class BaseSerializer(ABC):
    def __init__(self, item, many=False):
        if many and not isinstance(item, Iterable):
            raise Exception("When 'many' is True, item must be an iterable.")
        self.item = item
        self.many = many
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = (
                list(map(self.serialize, self.item))
                if self.many
                else self.serialize(self.item)
            )
        return self._data

    @abstractmethod
    def serialize(self, item):
        ...

import os
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from sunflower import Sunflower
from sunflower.db.models import Category, Product, ProductCategory
from sunflower.db import IntegrityError
from sunflower.settings import logging

from .utils import (
    regex_categories,
    regex_products_by_category,
    regex_product_reviews,
)


class MagazineLuizaSunflower(Sunflower):
    def __init__(self):
        super().__init__(marketplace_url="https://www.magazineluiza.com.br/")

    def get_categories(self):
        categories = list()
        for category in regex_categories(self.marketplace_url):
            parent = None
            if category["parent"] is not None:
                parent = Category.select().where(
                    (Category.name == category["parent"]["name"])
                    & (Category.initials == category["parent"]["initials"])
                )
            try:
                c = Category.create(
                    name=category["name"],
                    initials=category["initials"],
                    url=category["url"],
                    parent=parent,
                )
            except IntegrityError as e:
                msg = str(e) + ": " + f"'{category['name']}', '{category['initials']}'"
                logging.warning(msg)
            else:
                categories.append(c)
        return categories

    def get_products(self):
        categories = set(Category.select().where(Category.parent == None).limit(10))
        products = list()
        for category in categories:
            page = 1
            while True:
                products_per_page = regex_products_by_category(category, page)
                if len(products_per_page) == 0:
                    break
                for product in products_per_page:
                    try:
                        p = Product.create(name=product["name"], url=product["url"])
                        ProductCategory.create(product=p, category=category)
                    except IntegrityError as e:
                        msg = str(e) + ": " + f"'{product['name']}', '{product['url']}'"
                        logging.warning(msg)
                    else:
                        products.append(p)
                page += 1
        return products

    def get_product_reviews(self, product_id):
        product = Product.select().where(Product.id == product_id).first()
        reviews = regex_product_reviews(product, page=1)
        pprint(reviews)
        # TODO: pagination
        return []

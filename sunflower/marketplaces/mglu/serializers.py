from datetime import datetime

from bs4.element import Tag

from sunflower.base import BaseSerializer
from sunflower.settings import logging

from .utils import search_category, tree


class CategorySerializer(BaseSerializer):
    def __init__(self, item, many=False):
        super().__init__(item, many=many)

    def serialize(self, item):
        category = search_category(item)
        if category:
            return {
                "name": category["name"],
                "initials": category["initials"],
                "url": item["href"],
                "parent": category["parent"],
            }
        return {}


class ProductSerializer(BaseSerializer):
    def __init__(self, item, many=False):
        super().__init__(item, many=many)

    def serialize(self, item):
        try:
            return {"name": item.contents[-1].h3["title"], "url": item["href"]}
        except Exception as e:
            logging.error(e)
        return {}


class ReviewSerializer(BaseSerializer):
    def __init__(self, item, many=False):
        super().__init__(item, many=many)

    def serialize(self, item):
        if item is None:
            return {}
        print(item)
        return {
            "rating": item["rating"],
            "customer_name": item["customer_name"],
            "date": datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S%z"),
            "delta": item["delta"],
            "web_id": item["id"],
            "title": item["title"],
            "text": item["review_text"],
            "is_recommended": item["is_recommended"],
            "likes": item["likes"],
            "dislikes": item["dislikes"],
            "location": item["location"],
        }


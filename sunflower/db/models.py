import re

from peewee import (
    DateTimeField,
    Model,
    TextField,
    CharField,
    ForeignKeyField,
    BooleanField,
    IntegerField,
    FloatField,
)

from sunflower.db import Database, IntegrityError
from sunflower.settings import logging

db = Database().db


class BaseModel(Model):
    class Meta:
        database = db


class Category(BaseModel):
    name = CharField()
    initials = CharField()
    url = CharField(unique=True)
    parent = ForeignKeyField("self", related_name="children", null=True)

    class Meta:
        indexes = ((("name", "initials"), True),)

    def __str__(self):
        return f"Category: {self.name} ({self.initials})"

    @classmethod
    def create_if_not_exist(cls, row):
        parent = row.get("parent", None)

        if parent is not None:
            parent = cls.select().where(
                (cls.name == parent["name"]) & (cls.initials == parent["initials"])
            )

        try:
            category = cls.create(
                name=row["name"],
                initials=row["initials"],
                url=row["url"],
                parent=parent,
            )
        except IntegrityError as e:
            msg = str(e) + ": " + f"'{row['name']}', '{row['initials']}'"
            logging.warning(msg)
            return None

        return category


class Product(BaseModel):
    name = CharField()
    url = TextField(unique=True)

    def __str__(self):
        return f"Product ({self.name})"

    @property
    def web_id(self):
        regex = re.search(r"p\/(.+?)\/", self.url)
        return regex.group(1)

    @classmethod
    def create_if_not_exist(cls, row):
        try:
            product = cls.create(name=row["name"], url=row["url"])
            ProductCategory.create(product=product, category=row["category"])
        except IntegrityError as e:
            msg = str(e) + ": " + f"'{row['name']}', '{row['url']}'"
            logging.warning(msg)
            return None
        return product


class ProductCategory(BaseModel):
    product = ForeignKeyField(Product)
    category = ForeignKeyField(Category)


class Review(BaseModel):
    product = ForeignKeyField(Product, related_name="reviews")
    rating = FloatField()
    customer_name = CharField(null=True)
    date = DateTimeField()
    delta = CharField()
    web_id = CharField(unique=True)
    title = CharField(null=True)
    text = TextField(null=True)
    is_recommended = BooleanField()
    likes = IntegerField(default=0)
    location = CharField(null=True)
    dislikes = IntegerField(default=0)

    @classmethod
    def create_if_not_exist(cls, row):
        try:
            review = cls.create(**row)
        except IntegrityError as e:
            msg = str(e)
            logging.warning(msg)
            return None
        return review


models_list = [Product, Category, ProductCategory, Review]

from pprint import pprint

from sunflower.base import BaseSunflower
from sunflower.db.models import Category, Product, Review

from sunflower.marketplaces.mglu.crawlers import (
    CategoryCrawler,
    ProductCrawler,
    ReviewCrawler,
)


class MagazineLuizaSunflower(BaseSunflower):
    def __init__(self):
        super().__init__(marketplace_url="https://www.magazineluiza.com.br/")

    def load_categories(self):
        crawler = CategoryCrawler(self.marketplace_url)
        categories = list()
        for row in crawler.load():
            category = Category.create_if_not_exist(row)
            if category is not None:
                categories.append(category)
        return categories

    def load_products(self, max_page=5):
        categories = set(Category.select().where(Category.parent == None).limit(10))
        products = list()
        for category in categories:
            page = 1
            while page <= max_page:
                crawler = ProductCrawler(category.url, page=page)
                products_per_page = crawler.load()
                if len(products_per_page) == 0:
                    break
                for row in products_per_page:
                    row["category"] = category
                    product = Product.create_if_not_exist(row)
                    if product is not None:
                        products.append(product)
                page += 1
        return products

    def load_product_reviews(self, product_id, max_page=5):
        product = Product.select().where(Product.id == product_id).first()
        reviews = list()
        if product is not None:
            url = f"https://www.magazineluiza.com.br/review/{product.web_id}/"
            page = 1
            while page <= max_page and page < 10:
                crawler = ReviewCrawler(url, page=page)
                reviews_per_page = crawler.load()
                for row in reviews_per_page:
                    row["product"] = product
                    review = Review.create_if_not_exist(row)
                    if review is not None:
                        reviews.append(review)
                page += 1
        return reviews

import click

from sunflower.settings import logging
from sunflower.marketplaces.mglu.core import MagazineLuizaSunflower

mglu = MagazineLuizaSunflower()

@click.group()
def api():
    pass

@click.command()
def load_categories():
    """Load categories from mglu marketplace."""
    categories = mglu.load_categories()
    logging.info(f"Loaded {len(categories)} categories.")

@click.command()
@click.option("--max-page", "-x", type=int, default=5)
def load_products(max_page):
    """Load products from categories."""
    products = mglu.load_products(max_page=max_page)
    logging.info(f"Loaded {len(products)} products.")

@click.command()
@click.option("--product", "-p", type=int, required=True)
@click.option("--max-page", "-x", type=int, default=5)
def load_reviews(product, max_page):
    """Load reviews from products."""
    reviews = mglu.load_product_reviews(product, max_page=max_page)
    logging.info(f"Loaded {len(reviews)} reviews.")

api.add_command(load_categories)
api.add_command(load_products)
api.add_command(load_reviews)

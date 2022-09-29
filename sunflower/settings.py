import os
import logging
from decouple import config
from requests_cache import CachedSession

# installed marketplaces
MARKETPLACES = [
    "mglu"
]

# directories
TMP_DIR = "sunflower/tmp"
CACHE_DIR = os.path.join(TMP_DIR, "cache")

# debug=True development only
DEBUG = config("DEBUG", cast=bool, default=False)

# logging
logging_level = logging.INFO
if DEBUG:
    logging_level = logging.DEBUG

logging.basicConfig(
    level=logging_level, format="[%(levelname)s: %(asctime)s] %(name)s - %(message)s"
)

# cache
session = CachedSession(
    backend="sqlite",  # TODO: use redis
    namespace="request-cache",
    allowable_codes=(200,),
    allowable_methods=("GET",),
    expire_after=300,
)

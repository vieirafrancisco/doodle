from urllib.parse import urlparse

from peewee import SqliteDatabase, PostgresqlDatabase

from sunflower.settings import logging


class DatabaseMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=DatabaseMeta):
    def __init__(self, database_url=None):
        self.database_url = database_url or ""
        self._db = None

    @property
    def parse(self):
        return urlparse(self.database_url)

    @property
    def db(self):
        if self._db is None:
            if self.parse.scheme == "postgresql":
                self._db = PostgresqlDatabase(
                    self.parse.path[1:],
                    user=self.parse.username,
                    password=self.parse.password,
                    host=self.parse.hostname,
                    port=self.parse.port
                )
            else:
                self._db = SqliteDatabase("sunflower/database.db")
        return self._db

    def create_tables(self, models):
        try:
            self.db.connect()
            self.db.create_tables(models)
        except Exception as e:
            logging.debug(e)
        finally:
            self.db.close()

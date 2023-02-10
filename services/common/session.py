from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from common.settings import project_settings
from common.utils import Singleton
from sqlalchemy.ext.declarative import declarative_base


def get_connection_string() -> str:
    settings = project_settings()
    host = settings.database.host
    password = settings.database.password
    name = settings.database.name
    user = settings.database.user
    return f"mysql://{user}:{password}@{host}/{name}"


def create_db_session():
    engine = create_engine(get_connection_string())
    factory = sessionmaker(bind=engine)
    return factory()


@Singleton
class DB:
    def __init__(self):
        self.session = create_db_session()


def db() -> Session:
    return DB.instance.session


Base = declarative_base()

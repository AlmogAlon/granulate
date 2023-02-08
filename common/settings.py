import os
from dataclasses import dataclass
from typing import Dict

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Server(object):
    addr: str = os.getenv("SERVER_HOST")
    port: int = int(os.getenv("SERVER_PORT"))


@dataclass
class Database(object):
    host: str = os.getenv("DB_HOST")
    port: int = os.getenv("DB_PORT")
    password: str = os.getenv("DB_PASSWORD")
    name: str = os.getenv("DB_NAME")
    user: str = os.getenv("DB_USER")


@dataclass
class Settings:
    server: Server = Server()
    database: Database = Database()


_DEFAULT_PROJECT = "granulate"

_project_settings: Dict[str, Settings] = {_DEFAULT_PROJECT: Settings()}


def project_settings(project: str = None) -> Settings:
    if project is None:
        project = _DEFAULT_PROJECT

    settings = _project_settings.get(project)
    if settings is None:
        settings = _project_settings.get(_DEFAULT_PROJECT)

    return settings

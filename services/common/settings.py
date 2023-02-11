import os
from dataclasses import dataclass
from typing import Dict

from dotenv import load_dotenv

load_dotenv()


@dataclass
class WebSocket(object):
    addr: str = os.getenv("WEBSOCKET_HOST")
    port: int = int(os.getenv("WEBSOCKET_PORT"))


@dataclass
class Notification(object):
    addr: str = os.getenv("NOTIFICATION_HOST")
    port: int = int(os.getenv("NOTIFICATION_PORT"))


@dataclass
class Database(object):
    host: str = os.getenv("DB_HOST")
    port: int = os.getenv("DB_PORT")
    password: str = os.getenv("DB_PASSWORD")
    name: str = os.getenv("DB_NAME")
    user: str = os.getenv("DB_USER")


@dataclass
class Redis(object):
    host: str = os.getenv("REDIS_HOST")
    port: int = os.getenv("REDIS_PORT")


@dataclass
class Settings:
    notification: Notification = Notification()
    websocket: WebSocket = WebSocket()
    database: Database = Database()
    redis: Redis = Redis()


_DEFAULT_PROJECT = "granulate"

_project_settings: Dict[str, Settings] = {_DEFAULT_PROJECT: Settings()}


def project_settings(project: str = None) -> Settings:
    if project is None:
        project = _DEFAULT_PROJECT

    settings = _project_settings.get(project)
    if settings is None:
        settings = _project_settings.get(_DEFAULT_PROJECT)

    return settings

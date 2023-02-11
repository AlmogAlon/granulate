import json
from typing import Any, Optional, Callable, Dict
import redis

from common.settings import project_settings

CLIENT = None


def get_client():
    global CLIENT

    if CLIENT:
        return CLIENT

    settings = project_settings().redis
    CLIENT = redis.StrictRedis(settings.host, settings.port, charset="utf-8", decode_responses=True)

    return CLIENT


def insert(topic_name: str, payload: Any):
    client = get_client()
    client.publish(topic_name, json.dumps(payload))


def subscribe(channel_name: str, callback: Callable[[Dict], None]) -> Optional[Any]:
    client = get_client().pubsub()
    client.subscribe(channel_name)
    for message in client.listen():
        if message is not None and isinstance(message, dict):
            if message.get("type") == "message":
                payload = json.loads(message.get("data"))
                return callback(payload)

import logging
import time
from typing import Dict, Callable

from common.redis_pubsub import subscribe, insert
from dataclasses import dataclass

CHANNEL = "notification"


@dataclass
class Message:
    message: str
    user_id: int

    def to_dict(self) -> Dict:
        return {
            "message": self.message,
            "user_id": self.user_id,
        }

    @staticmethod
    def from_dict(data: Dict):
        return Message(
            message=data["message"],
            user_id=data["user_id"],
        )


def send(message: Message):
    insert(CHANNEL, message.to_dict())


def get(_callback: Callable[[Dict], None]):
    while True:
        try:
            subscribe(CHANNEL, _callback)
        except Exception as e:
            logging.exception(f"exception caught in loop! {e}")
            time.sleep(1)

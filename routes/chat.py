from __future__ import annotations

import dataclasses
import json
import typing
from typing import Dict

import abort
from router import engine
from bottle import request
from dataclasses import dataclass

from utils.utils import pluck

app = engine.create_app()


@dataclass
class Message:
    message: str
    username: str

    @staticmethod
    def from_dict(obj: Dict) -> Message:
        allowed_keys = [*typing.get_type_hints(Message).keys()]
        plucked = pluck(obj, allowed_keys)
        return Message(**plucked)

    def to_dict(self) -> Dict:
        return dataclasses.asdict(self)


@dataclass
class Chat:
    messages: Dict[str, typing.List[Message]] = None

    def __post_init__(self):
        self.messages = {}

    def add_message(self, message: Message):
        if message.username not in self.messages.keys():
            self.messages[message.username] = [message]
        else:
            self.messages[message.username].append(message)

    def get_messages(self, username: str = None) -> typing.List[Dict]:
        if username:
            return [m.to_dict() for m in self.messages[username]]
        values = self.messages.values()
        return [message.to_dict() for messages in values for message in messages]


chat = Chat()


@app.route("/", method="POST")
def send_message():
    request_json = json.loads(request.body.read())
    if "username" not in request_json:
        abort.soft(code="MISSING_USERNAME", reason="Missing username in request.")
    if "message" not in request_json:
        abort.soft(code="MISSING_MESSAGE", reason="Missing message in request.")

    chat_message = Message.from_dict(request_json)
    chat.add_message(chat_message)


@app.route("/")
def get_message():
    messages = chat.get_messages()
    return {"messages": messages}

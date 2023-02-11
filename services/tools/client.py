import json
import logging
import time
from dataclasses import dataclass

from websocket import create_connection, WebSocket
from argparse import ArgumentParser

from common.mysql_db.models.user import User
from common.session import db
from common.settings import project_settings
from common import utils

settings = project_settings().websocket


@dataclass
class Connection:
    user_id: int
    ws: WebSocket = None

    def __post_init__(self):
        self.ws = create_connection(
            f"ws://{settings.addr}:{settings.port}/websocket?user_id={self.user_id}"
        )

    def send_message(self, message: str, username: str, room_name: str = None):
        json_message = {
            "username": username,
            "message": message,
        }
        self.ws.send(json.dumps(json_message))

    def get_messages(self):
        while True:
            result = self.ws.recv()
            logging.info("Received '%s'" % result)
            time.sleep(1)


def run(options):
    session = db()
    user = User.get_by(db=session, name=options.username)
    if not user:
        logging.error(f"User {options.username} not found!")
        return
    conn = Connection(user_id=user.id)

    if options.message:
        message = input(f"Enter message (will be sent to {options.username}): ")
        conn.send_message(message, options.username, options.room)

    conn.get_messages()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-u", "--username", dest="username", help="username to get messages for", required=True
    )
    parser.add_argument("-r", "--room", dest="room", help="room")
    parser.add_argument("-m", "--message", dest="message", action="store_true", help="send a message")
    args = parser.parse_args()

    utils.initialize_logging_to_stdout(logging.INFO)
    run(args)

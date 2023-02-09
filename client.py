import logging
import time
from argparse import ArgumentParser
from typing import Optional, Dict

import requests

from common.settings import project_settings
from common import utils


server = project_settings().server
CHAT_API = f"http://{server.addr}:{server.port}/chat"


def send_message(message: str, username: str, room_name: str = None):
    json_message = {
        "username": username,
        "message": message,
    }
    if room_name:
        json_message["room_name"] = room_name

    try:
        requests.post(CHAT_API, json=json_message)
    except Exception as e:
        logging.error(f"Failed to send message: {e}")
        return


def get_messages(username: str, room_name: str = None) -> Optional[Dict]:
    try:
        url = CHAT_API + f"?user={username}"
        if room_name:
            url += f"&room_name={room_name}"
        messages = requests.get(url).json()
    except Exception as e:
        logging.error(f"Failed to get messages: {e}")
        return

    return messages


def run(options):

    if options.message:
        message = input(f"Enter message (will be sent to {options.username}): ")
        send_message(message, options.username, options.room)

    while True:
        messages = get_messages(options.username, options.room)
        logging.info(messages)
        time.sleep(1)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-u", "--username", dest="username", help="username to get messages for", required=True
    )
    parser.add_argument("-r", "--room", dest="room", help="room")
    parser.add_argument("--message", dest="message", action="store_true", help="send a message")
    args = parser.parse_args()

    utils.initialize_logging_to_stdout(logging.INFO)
    run(args)

import logging
import time
from argparse import ArgumentParser
from typing import Optional, Dict

import requests

from routes.chat import Message
from utils import utils

CHAT_API = "http://127.0.0.1:1337/chat"


def send_message(message: str, username: str):
    chat_message = Message(message=message, username=username)
    try:
        requests.post(CHAT_API, json=chat_message.to_dict())
    except Exception as e:
        logging.error(f"Failed to send message: {e}")
        return


def get_messages(username: str = None) -> Optional[Dict]:
    try:
        messages = requests.get(CHAT_API + f"?user={username}").json()
    except Exception as e:
        logging.error(f"Failed to get messages: {e}")
        return

    return messages


def run(options):

    if options.message:
        message = input(f"Enter message (will be sent to {options.username}): ")
        send_message(message, options.username)

    while True:
        messages = get_messages(options.username)
        logging.info(messages)
        time.sleep(1)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-u", "--username", dest="username", help="username to get messages for", required=True
    )
    parser.add_argument("--message", dest="message", action="store_true", help="send a message")
    args = parser.parse_args()

    utils.initialize_logging_to_stdout(logging.INFO)
    run(args)

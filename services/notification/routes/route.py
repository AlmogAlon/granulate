from __future__ import annotations

import json
import logging

from bottle import request

from common import engine, abort
from common.mysql_db.models.message import Message
from common.mysql_db.models.room import Room
from common.mysql_db.models.user import User
from granulate.notification import Message as NotificationMessage, send
from common.session import db

app = engine.create_app()


@app.route("/notification", method="POST")
def send_notification():
    req_body = request.body.read()
    if not req_body:
        return

    body = json.loads(req_body)
    message_content = body.get("message")
    user_name = body.get("user_name")
    room_name = body.get("room_name")

    if not user_name:
        abort.soft(code="MISSING_USERNAME", reason="Missing username in request.")
    if not message_content:
        abort.soft(code="MISSING_MESSAGE", reason="Missing message in request.")

    session = db()
    user = User.get_by(db=session, name=user_name)
    if not user:
        abort.soft(code="USER_NOT_FOUND", reason="User not found.")

    room_filter = {}
    if room_name:
        room = Room.get_by(db=session, name=room_name)
        if not room:
            abort.soft(
                code="ROOM_NOT_EXIST",
                reason=f"Room name {room_name} does not exist",
            )
        room_filter = {"room": room}

    message = Message(
        to_user=user,
        user=User.get_by(db=session, name="test_user"),
        message=message_content,
        **room_filter,
    )
    session.add(message)
    session.commit()

    try:
        send(NotificationMessage(message_content, user.id))
    except Exception as e:
        logging.error(f"send_notification(): failed sending notification: {e}")

    return {
        "message_id": message.id,
    }


@app.route("/read", method="POST")
def read_message():
    return {}


@app.route("/sent", method="POST")
def read_message():
    return {}

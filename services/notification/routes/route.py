from __future__ import annotations

import json
import logging
from datetime import datetime

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
    user_id = body.get("user_id")
    room_name = body.get("room_name")

    if not user_id:
        abort.soft(code="MISSING_USER", reason="Missing user_id in request.")
    if not message_content:
        abort.soft(code="MISSING_MESSAGE", reason="Missing message in request.")

    session = db()
    user = User.get_by(db=session, id=user_id)
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
        send(NotificationMessage(message.id, message_content, user.id))
    except Exception as e:
        logging.error(f"send_notification(): failed sending notification: {e}")

    return {
        "message_id": message.id,
    }


@app.route("/read", method="POST")
def read_message():
    # TODO: implement
    abort.soft(code="NOT_IMPLEMENTED", reason="Not implemented yet.")


@app.route("/notification/sent", method="POST")
def read_message():
    message_id = request.json.get("message_id")
    sent_time = request.json.get("sent_time")
    session = db()
    msg = Message.get_by(db=session, id=message_id)
    if not msg:
        abort.soft(code="MESSAGE_NOT_FOUND", reason="Message not found.")
    if msg.sent:
        abort.soft(code="MESSAGE_ALREADY_SENT", reason="Message already sent.")

    msg.sent = datetime.fromisoformat(sent_time)
    session.commit()

    return {}

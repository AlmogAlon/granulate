from __future__ import annotations
import json
import abort
from common.session import db
from mysql_db.models.message import Message
from mysql_db.models.room import Room
from mysql_db.models.user import User
from router import engine
from bottle import request

app = engine.create_app()


@app.route("/", method="POST")
def send_message():
    request_json = json.loads(request.body.read())
    user_name = request_json.get("username", None)
    message = request_json.get("message", None)
    if not user_name:
        abort.soft(code="MISSING_USERNAME", reason="Missing username in request.")
    if not message:
        abort.soft(code="MISSING_MESSAGE", reason="Missing message in request.")

    session = db()
    user = User.get_by(db=session, name=user_name)
    if not user:
        abort.soft(code="USER_NOT_FOUND", reason="User not found.")

    room_name = request_json.get("room_name", None)
    room_filter = {}
    if room_name:
        room = Room.get_by(db=session, name=room_name)
        if not room:
            abort.soft(
                code="ROOM_NOT_EXIST",
                reason=f"Room name {request_json['room_name']} does not exist",
            )
        room_filter = {"room": room}

    message = Message(
        to_user=user,
        user=User.get_by(db=session, name="test_user"),
        message=message,
        **room_filter,
    )
    session.add(message)
    session.commit()


@app.route("/")
def get_message():
    user_name = request.query.get("user", None)
    room_name = request.query.get("room_name", None)
    session = db()

    message_filters = {}
    if room_name:
        room = Room.get_by(db=session, name=room_name)
        if not room:
            abort.soft(code="NOT_EXIST", reason=f"Room name {room_name} does not exist")
        message_filters["room"] = room

    if user_name:
        user = User.get_by(db=session, name=user_name)
        if not user:
            abort.soft(code="NOT_EXIST", reason=f"User name {user_name} does not exist")

        message_filters["to_user"] = user

    messages = Message.get_by(db=session, **message_filters)
    return {"messages": [message.view for message in messages]}

from __future__ import annotations

import dataclasses
import json
import typing
from typing import Dict

import abort
from common.session import db
from mysql_db.models.message import Message
from mysql_db.models.user import User
from router import engine
from bottle import request
from dataclasses import dataclass

from common.utils import pluck

app = engine.create_app()


@app.route("/", method="POST")
def send_message():
    request_json = json.loads(request.body.read())
    if "username" not in request_json:
        abort.soft(code="MISSING_USERNAME", reason="Missing username in request.")
    if "message" not in request_json:
        abort.soft(code="MISSING_MESSAGE", reason="Missing message in request.")

    session = db()
    user_name = request_json["username"]
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        abort.soft(code="USER_NOT_EXIST", reason=f"User name {user_name} does not exist")

    message = Message(
        to_uid=user.id,
        uid=user.id,
        message=request_json["message"],
    )
    session.add(message)
    session.commit()


@app.route("/")
def get_message():
    user_name = request.query.get("user", None)
    session = db()
    filters = {}
    if user_name:
        user = session.query(User).filter_by(name=user_name).first()
        if not user:
            abort.soft(code="USER_NOT_EXIST", reason=f"User name {user_name} does not exist")
        filters = {"to_uid": user.id}

    messages = Message.get_by(db=session, **filters)
    return {"messages": [message.view for message in messages]}

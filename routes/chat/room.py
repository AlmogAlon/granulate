from __future__ import annotations

from typing import List, Dict

from mysql_db.models.room import Room
from router import engine
from common.session import db

app = engine.create_app()


@app.route('/')
@app.route("/<room_id>", method="GET")
def get_room(room_id: int = None) -> Dict:
    session = db()
    if not room_id:
        rooms = Room.get_all(db=session)
    else:
        room = Room.get_by(db=session, id=room_id)
        rooms = [room] if room else []
    return {"rooms": [room.view for room in rooms]}

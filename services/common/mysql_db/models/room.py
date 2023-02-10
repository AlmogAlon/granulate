from __future__ import annotations

from typing import List, Dict, TypeVar

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Session
from common.session import Base


class RoomUser(Base):
    __tablename__ = "room_user"
    id = Column(Integer, primary_key=True, autoincrement=True)

    room_id = Column(Integer, ForeignKey("room.id"))
    uid = Column(Integer, ForeignKey("user.id"))
    user = relationship('User', foreign_keys=[uid])
    room = relationship('Room', foreign_keys=[room_id])


T = TypeVar("T")


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    messages = relationship('Message', foreign_keys="Message.room_id")
    room_users = relationship('RoomUser', foreign_keys="RoomUser.room_id", back_populates="room")

    @staticmethod
    def get_all(db: Session, **kwargs) -> List[T]:
        return db.query(Room).filter_by(**kwargs).all()

    @staticmethod
    def get_by(db: Session, **kwargs) -> Room | None:
        return db.query(Room).filter_by(**kwargs).first()

    @property
    def view(self) -> Dict:
        return {
            "name": self.name,
            "id": self.id,
            "users": [user.user.view for user in self.room_users],
        }

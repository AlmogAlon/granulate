from __future__ import annotations

from typing import List, Type

from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import Session, relationship
from common.session import Base


class Message(Base):
    __tablename__ = "message"

    # basic info
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String)
    uid = Column(Integer, ForeignKey("user.id"))
    to_uid = Column(Integer, ForeignKey("user.id"))
    message = Column(String)
    user = relationship('User', foreign_keys=[uid], back_populates='messages')
    to_user = relationship('User', foreign_keys=[to_uid], back_populates='messages')
    room_id = Column(Integer, ForeignKey("room.id"))
    room = relationship('Room', foreign_keys=[room_id], back_populates='messages')

    @staticmethod
    def get_by(db: Session, **kwargs) -> List[Type[Message]]:
        return db.query(Message).filter_by(**kwargs).all()

    @property
    def view(self):
        return {"message": self.message, "to_uid": self.to_uid, "uid": self.uid}

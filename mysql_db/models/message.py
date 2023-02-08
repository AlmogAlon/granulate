from __future__ import annotations

from typing import List, Type

from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import Session, relationship

from common.session import Base
from mysql_db.models.user import User


class Message(Base):
    __tablename__ = "message"

    # basic info
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String)
    uid = Column(Integer, ForeignKey("user.id"))
    to_uid = Column(Integer, ForeignKey("user.id"))
    message = Column(String)
    user = relationship('User', foreign_keys=[uid])
    to_user = relationship('User', foreign_keys=[to_uid])

    @staticmethod
    def get_by(db: Session, **kwargs) -> List[Type[Message]]:
        return db.query(Message).filter_by(**kwargs).all()

    @property
    def view(self):
        return {"message": self.message, "to_uid": self.to_uid, "uid": self.uid}

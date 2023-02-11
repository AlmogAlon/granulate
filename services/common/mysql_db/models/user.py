from __future__ import annotations

from typing import Dict

from sqlalchemy import Column, String
from sqlalchemy.orm import Session, relationship
from common.session import Base
from common.mysql_db.models.message import Message
from common.mysql_db.models.room import Room


class User(Base):
    __tablename__ = "user"

    # basic info
    id = Column(String, primary_key=True)
    name = Column(String)
    messages = relationship('Message', foreign_keys=Message.uid)

    @staticmethod
    def get_by(db: Session, **kwargs) -> User | None:
        return db.query(User).filter_by(**kwargs).first()

    @property
    def view(self) -> Dict:
        return {"name": self.name, "id": self.id}

from __future__ import annotations

from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from common.session import Base


class User(Base):
    __tablename__ = "user"

    # basic info
    id = Column(String, primary_key=True)
    name = Column(String)

    @staticmethod
    def get_by(db: Session, **kwargs) -> User | None:
        return db.query(User).filter_by(**kwargs).first()

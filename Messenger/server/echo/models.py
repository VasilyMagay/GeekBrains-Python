from sqlalchemy import (
    String, Integer, Column, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base, import_models

import_models()


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='messages')

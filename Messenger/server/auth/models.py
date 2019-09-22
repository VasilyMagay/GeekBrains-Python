from sqlalchemy import (
    String, Integer, Column, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship

from database import Base, import_models
from datetime import datetime

import_models()


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    info = Column(String)

    def __init__(self, login, info):
        self.login = str(login)
        self.info = str(info)

    def __repr__(self):
        return "<Client ('%s','%s')>" % (self.login, self.info)


class ClientHistory(Base):
    __tablename__ = 'clients_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer)
    time = Column(DateTime)
    ip = Column(String)

    def __init__(self, client_id, ip):
        self.client_id = int(client_id)
        self.ip = str(ip)
        self.time = datetime.now()

    def __repr__(self):
        return "<Client history ('%s','%s', '%s')>" % (self.client_id, self.ip, self.time)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    sessions = relationship('Session', back_populates='user')
    messages = relationship('Message', back_populates='user')


class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, nullable=False, unique=True)
    created = Column(DateTime, default=datetime.now())
    closed = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='sessions')

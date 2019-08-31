from sqlalchemy import (
    create_engine, String, Integer,
    Column, DateTime
)
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime


Base = declarative_base()
engine = create_engine('sqlite:///server.db')


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    info = Column(String)

    def __init__(self, login, info):
        self.login = str(login)
        self.info = str(info)

    def __repr__(self):
        return "<Client ('%s','%s')>" % (self.login, self.info)


class ClientHistory(Base):
    __tablename__ = 'clients_history'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    time = Column(DateTime)
    ip = Column(String)

    def __init__(self, client_id, ip):
        self.client_id = int(client_id)
        self.ip = str(ip)
        self.time = datetime.now()

    def __repr__(self):
        return "<Client history ('%s','%s', '%s')>" % (self.client_id, self.ip, self.time)

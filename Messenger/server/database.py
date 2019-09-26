from sqlalchemy import create_engine, String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from datetime import datetime
from contextlib import contextmanager

from settings import CONNECTION_STRING, BASE_DIR

Base = declarative_base()
engine = create_engine(CONNECTION_STRING)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    user_sessions = relationship('UserSession', back_populates='user')
    messages = relationship('Message', back_populates='user')

    def __init__(self, name, password):
        self.name = str(name)
        self.password = password

    def __repr__(self):
        return "<User ('%s','%s')>" % (self.id, self.name)


class UserSession(Base):
    __tablename__ = 'user_sessions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, nullable=False, unique=True)
    created = Column(DateTime, default=datetime.now())
    closed = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='user_sessions')

    def __repr__(self):
        return "<User Session ('%s','%s')>" % (self.token, self.user.name)


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='messages')


def create_tables():
    print(f'BASE_DIR = {BASE_DIR}')
    # Создаем все таблицы
    Base.metadata.create_all(engine)
    print('Database was created')


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

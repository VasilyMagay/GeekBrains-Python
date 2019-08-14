from sqlalchemy.orm import sessionmaker
from models import (
    Base, engine, Client, ClientHistory
)


def new_session():
    # начинаем новую сессию работы с БД
    Session = sessionmaker(bind=engine)
    return Session()


def create_tables():
    Base.metadata.create_all(engine)


def add_client(login, info):

    session = new_session()

    # добавить новый элемент
    new_element = Client(login, info)
    session.add(new_element)

    # совершаем транзакцию
    session.commit()


def print_clients():

    session = new_session()

    # посмотрим что уже есть в базе данных
    for instance in session.query(Client).order_by(Client.id):
        print(instance)


def add_history(client_id, ip):  # Для тестирования

    session = new_session()

    # добавить новый элемент
    new_element = ClientHistory(client_id, ip)
    session.add(new_element)

    # совершаем транзакцию
    session.commit()


def print_history():

    session = new_session()

    # посмотрим что уже есть в базе данных
    for instance in session.query(ClientHistory).order_by(ClientHistory.id):
        print(instance)

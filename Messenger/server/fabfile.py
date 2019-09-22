from database import Base, import_models, Session

import_models()


def add_client(login, info):

    session = Session()

    # добавить новый элемент
    new_element = Client(login, info)
    session.add(new_element)

    # совершаем транзакцию
    session.commit()


def print_clients():

    session = Session()

    # посмотрим что уже есть в базе данных
    for instance in session.query(Client).order_by(Client.id):
        print(instance)


def add_history(client_id, ip):  # Для тестирования

    session = Session()

    # добавить новый элемент
    new_element = ClientHistory(client_id, ip)
    session.add(new_element)

    # совершаем транзакцию
    session.commit()


def print_history():

    session = Session()

    # посмотрим что уже есть в базе данных
    for instance in session.query(ClientHistory).order_by(ClientHistory.id):
        print(instance)

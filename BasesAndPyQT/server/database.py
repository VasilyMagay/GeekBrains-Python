import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import CONNECTION_STRING, INSTALLED_MODULES, BASE_DIR


Base = declarative_base()
engine = create_engine(CONNECTION_STRING)
Session = sessionmaker(bind=engine)


def import_models():
    """
    Подключаем модели из всех приложений
    """
    module_name_list = [f'{item}.models' for item in INSTALLED_MODULES]
    module_path_list = (os.path.join(BASE_DIR, item, 'models.py') for item in INSTALLED_MODULES)
    for index, path in enumerate(module_path_list):
        if os.path.exists(path):
            __import__(module_name_list[index])


def create_tables():
    import_models()
    # Создаем все таблицы
    Base.metadata.create_all(engine)

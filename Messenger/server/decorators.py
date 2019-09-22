import logging
import sys

from functools import wraps
from datetime import datetime


logger = logging.getLogger('decorators')


def logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f'{datetime.now()} Функция {func.__name__}() вызвана из функции {func_name()}()')
        return func(*args, **kwargs)
    return wrapper


def func_name():
    return sys._getframe(1).f_code.co_name

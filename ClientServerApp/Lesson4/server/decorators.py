import logging
import sys

from functools import wraps
from datetime import datetime
from protocol import make_response


logger = logging.getLogger('decorators')


def logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f'{datetime.now()} Функция {func.__name__}() вызвана из функции {func_name()}()')
        return func(*args, **kwargs)
    return wrapper


def func_name():
    return sys._getframe(1).f_code.co_name


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'token' not in request:
            return make_response(request, 403, 'Access denied')
        return func(request, *args, **kwargs)
    return wrapper

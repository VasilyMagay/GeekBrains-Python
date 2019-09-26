"""The __controllers__ docstr"""

from protocol import make_response
from decorators import logged
from .decorators import login_required
from database import Base, Session, session_scope, User, UserSession
from functools import reduce
from .utils import authenticate, login

import hmac
from settings import SECRET_KEY
from datetime import datetime


@logged
@login_required
def get_users_controller(request):
    """Get Users Controller."""

    session = Session()
    data = reduce(
        lambda value, item: value + [{'id': item.id, 'name': item.name}],
        session.query(User).all(),
        []
    )
    return make_response(request, 202, data)


@logged
@login_required
def add_user_controller(request):
    name = request.get('name')
    password = request.get('password')
    session = Session()
    session.add(User(name=name, password=password))
    session.commit()
    return make_response(request, 200, f'User {name} created')


@logged
@login_required
def del_user_controller(request):
    user_id = int(request.get('id'))
    session = Session()
    for each_user in session.query(User).filter_by(id=user_id):
        session.delete(each_user)
    session.commit()
    return make_response(request, 200, f'User id {user_id} deleted')


def login_controller(request):
    errors = {}
    is_valid = True
    data = request.get('data')
    # print(f'request={request}')
    # print(f'data={data}')

    if not 'time' in request:
        errors.update({'time': 'Request attribute is required'})
        is_valid = False
    if not 'password' in data:
        errors.update({'password': 'Data attribute is required'})
        is_valid = False
    if not 'login' in data:
        errors.update({'login': 'Data attribute is required'})
        is_valid = False

    if not is_valid:
        return make_response(request, 400, {'errors': errors})

    user = authenticate(data.get('login'), data.get('password'))

    if user:
        token = login(request, user)
        return make_response(request, 200, {'token': token})

    return make_response(request, 400, 'Enter correct login or password')


def registration_controller(request):
    errors = {}
    is_valid = True
    data = request.get('data')
    # print(f'request={request}')
    # print(f'data={data}')

    if not 'password' in data:
        errors.update({'password': 'data attribute is required'})
        is_valid = False
    if not 'login' in data:
        errors.update({'login': 'data attribute is required'})
        is_valid = False

    if not is_valid:
        return make_response(request, 400, {'errors': errors})

    db_session = Session()
    user = db_session.query(User).filter_by(name=data.get('login')).first()
    if user:
        return make_response(request, 200, f'User "{data.get("login")}" already exists')
    else:
        # print(f'{SECRET_KEY}={SECRET_KEY.encode()}')
        # print(f'{request.get("password")}={request.get("password").encode()}')
        # сокрытие пароля для хранения на сервере
        hmac_obj = hmac.new(SECRET_KEY.encode(), data.get('password').encode())
        password_digest = hmac_obj.digest()
        user = User(name=data.get('login'), password=password_digest)
        db_session.add(user)
        db_session.commit()
        # print(f'user added {user}')
        # token = login(request, user)
        # print(f'return token {token}')
    return make_response(request, 200, f'User "{data.get("login")}" was registered')
    # return make_response(request, 200, {'token': token})


@login_required
def logout_controller(request):
    with session_scope() as db_session:
        user_session = db_session.query(UserSession).filter_by(token=request.get('token')).first()
        user_session.closed = datetime.now()
        return make_response(request, 200, 'Session closed')

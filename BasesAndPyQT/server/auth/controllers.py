from protocol import make_response
from decorators import logged
from .decorators import login_required
from database import Base, import_models, Session, session_scope
from functools import reduce
from .models import User
from .utils import authenticate, login

import hmac
from .settings import SECRET_KEY
from datetime import datetime

import_models()


@logged
@login_required
def get_users_controller(request):
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

    if not 'time' in request:
        errors.update({'time': 'Attribute is required'})
        is_valid = False
    if not 'password' in request:
        errors.update({'password': 'Attribute is required'})
        is_valid = False
    if not 'login' in request:
        errors.update({'login': 'Attribute is required'})
        is_valid = False

    if not is_valid:
        return make_response(request, 400, {'errors': errors})

    user = authenticate(request.get('login'), request.get('password'))

    if user:
        token = login(request, user)
        return make_response(request, 200, {'token': token})

    return make_response(request, 400, 'Enter correct login or password')


def registration_controller(request):
    errors = {}
    is_valid = True

    if not 'password' in request:
        errors.update({'password': 'Attribute is required'})
        is_valid = False
    if not 'login' in request:
        errors.update({'login': 'Attribute is required'})
        is_valid = False

    if not is_valid:
        return make_response(request, 400, {'errors': errors})

    hmac_obj = hmac.new(SECRET_KEY, request.get('password'))
    password_digest = hmac_obj.digest()

    with session_scope() as db_session:
        user = User(name=request.get('login'), password=password_digest)
        db_session.add(user)
        token = login(request, user)
        return make_response(request, 200, {'token': token})


@login_required
def logout_controller(request):
    with session_scope() as db_session:
        user_session = db_session.query(Session).filter_by(token=request.get('token')).first()
        user_session.closed = datetime.now()
        return make_response(request, 200, 'Session closed')

from protocol import make_response
from decorators import logged, login_required
from database import Base, import_models, Session
from functools import reduce
from .models import User

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

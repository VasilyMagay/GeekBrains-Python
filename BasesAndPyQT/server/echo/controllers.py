from protocol import make_response
from decorators import logged, login_required
from database import Base, import_models, Session
from functools import reduce
from .models import Message

import_models()


@logged
@login_required
def echo_controller(request):
    data = request.get('data')
    session = Session()
    message = Message(data=data)
    session.add(message)
    session.commit()
    return make_response(request, 200, data)


@logged
@login_required
def get_messages_controller(request):
    session = Session()
    messages = reduce(
        lambda value, item: value + [{'data': item.data, 'created': str(item.created)}],
        session.query(Message).all(),
        []
    )
    return make_response(request, 200, messages)

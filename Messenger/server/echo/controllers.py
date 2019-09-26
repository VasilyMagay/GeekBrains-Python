from protocol import make_response
from decorators import logged
from auth.decorators import login_required
from database import Base, Session, session_scope, Message
from functools import reduce


@logged
@login_required
def echo_controller(request):
    data = request.get('data')
    session = Session()
    message = Message(data=data)
    session.add(message)
    session.commit()
    session.close()
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


def delete_message_controller(request):
    data = request.get('data')
    message_id = data.get('message_id')
    with session_scope() as session:
        message = session.query(Message).filter_by(id=message_id).first()
        session.delete(message)
    return make_response(request, 200)


def update_message_controller(request):
    message_id = request.get('message_id')
    message_data = request.get('message_data')
    session = Session()
    message = session.query(Message).filter_by(id=message_id).first()
    message.data = message_data
    session.commit()
    session.close()
    return make_response(request, 200)

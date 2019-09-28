from database import session_scope, UserSession


def validate_request(raw):
    if 'action' in raw and 'time' in raw:
        return True
    return False


def make_response(request, code, data=None):

    action = request.get('action')
    token = request.get('token')

    result = {
        'action': action,
        'time': request.get('time'),
        'token': token,
        'data': data,
        'code': code
    }

    # print(f'action={action}')
    # print(f'token={token}')

    if action == 'echo' and token:
        with session_scope() as db_session:
            user_session = db_session.query(UserSession).filter_by(token=token).first()
            # print(f'user_session={user_session}')
            if user_session and not user_session.closed:
                result['username'] = user_session.user.name

    return result

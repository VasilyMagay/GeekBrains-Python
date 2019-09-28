import hmac
import hashlib
from database import session_scope, User, UserSession

from settings import SECRET_KEY


def authenticate(login, password):
    with session_scope() as db_session:
        user = db_session.query(User).filter_by(name=login).first()
        hmac_obj = hmac.new(SECRET_KEY.encode(), password.encode())
        password_digest = hmac_obj.digest()
        # print(f'login={login}, password={password}, digest={password_digest}')
        # print(f'user={user}')
        # print(f'user.password={user.password}')
        # print(f'user.password.encode()={user.password.encode()}')
        # print(f'compare_digest={hmac.compare_digest(password_digest, user.password)}')
        if user and hmac.compare_digest(password_digest, user.password):
            return user


def login(request, user):
    hash_obj = hashlib.sha256()
    hash_obj.update(SECRET_KEY.encode())
    hash_obj.update(str(request.get('time')).encode())
    token = hash_obj.hexdigest()
    with session_scope() as db_session:
        user_session = UserSession(user=user, token=token)
        db_session.add(user_session)
    return token

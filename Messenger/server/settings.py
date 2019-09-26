import os

INSTALLED_MODULES = (
    'auth',
    'echo',
)

CONNECTION_STRING = 'sqlite:///server.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = '1lRCqvUtnWaKkzrU'

MESSAGE_PATTERN = b'%(nonce)s%(key)s%(tag)s%(data)s'

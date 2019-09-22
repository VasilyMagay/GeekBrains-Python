import os

INSTALLED_MODULES = (
    'auth',
    'echo',
)

CONNECTION_STRING = 'sqlite:///server.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
